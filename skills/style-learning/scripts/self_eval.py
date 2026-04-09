#!/usr/bin/env python3
"""
爆款智坊 风格学习 - 自测评辅助脚本

【定位说明】
本脚本是风格学习的辅助工具，负责：
1. 格式校验：skill-creator 规范 + 爆款智坊 特有检查
2. IP名称一致性：按平台分别检查（仅当提取到时）
3. 内容标准：行数门槛 + 占位符检查
4. 提取完整性：8+11维度是否全部完成

【与 tougu 的区别】
tougu 自测评：对比"生成文章"vs"原始样本"的风格匹配度
爆款智坊 自测评：校验"风格档案"（style.yaml/style_manual.md/platform_styles/）的生成质量
（爆款智坊 不生成文章，只生成风格手册）

用法：
# 完整校验
python self_eval.py --style-dir ../..

# 格式校验（不含内容测试）
python self_eval.py --style-dir ../.. --format-only

# 输出JSON报告
python self_eval.py --style-dir ../.. --output eval_report.json
"""

import argparse
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any

# ============ 配置 ============

# 整体≥80%通过；任何维度<50%必须修复；最多3轮
ACCEPTANCE_THRESHOLD = 0.80
MIN_DIMENSION_SCORE = 0.50
MAX_ITERATIONS = 3

# 行数字符门槛（字符数，非行数）
MIN_STYLE_MANUAL_CHARS = 500
MIN_PLATFORM_STYLE_CHARS = 200

# 检查的维度
DIMENSION_NAMES = [
    "标题格式", "段落结构", "句式特征", "词汇特征",
    "分析逻辑", "数据规范", "固定表达", "数据需求",
    "段落强制开头语", "比喻体系", "图片使用",
]


# ============ 格式校验 ============

def validate_skill_md(skill_md_path: Path) -> Tuple[bool, List[str]]:
    """校验 style-learning/SKILL.md 自身格式"""
    issues = []
    if not skill_md_path.exists():
        return False, ["[FAIL] SKILL.md not found"]

    content = skill_md_path.read_text(encoding="utf-8")

    # 1. YAML frontmatter
    if not content.startswith("---"):
        issues.append("[FAIL] SKILL.md missing YAML frontmatter")
    else:
        parts = content.split("---", 2)
        if len(parts) < 3:
            issues.append("[FAIL] YAML frontmatter not properly closed")
        else:
            fm_text = parts[1]
            for field in ["name", "description"]:
                if field not in fm_text:
                    issues.append(f"[FAIL] frontmatter missing required field: {field}")

    # 2. name 字段（小写字母+数字+连字符）
    name_match = re.search(r"^name:\s*(.+)$", fm_text, re.MULTILINE)
    if name_match:
        name_value = name_match.group(1).strip()
        if not re.match(r"^[a-z0-9_-]+$", name_value):
            issues.append(f"[FAIL] name field invalid: '{name_value}'")

    # 3. description 不超过200字符
    desc_match = re.search(r"^description:\s*(.+)$", fm_text, re.MULTILINE)
    if desc_match:
        desc_value = desc_match.group(1).strip()
        if len(desc_value) > 200:
            issues.append(f"[WARN] description too long ({len(desc_value)} chars)")

    # 4. 必要章节
    for section in ["Phase 1", "Phase 2", "Phase 3", "Phase 4", "Phase 5"]:
        if section not in content:
            issues.append(f"[FAIL] SKILL.md missing required section: {section}")

    passed = not any(i.startswith("[FAIL]") for i in issues)
    return passed, issues


def validate_style_dir(style_dir: Path) -> Tuple[bool, List[str]]:
    """
    校验风格档案目录结构。
    注意：style.yaml、style_manual.md、platform_styles/ 是风格学习OUTPUT后才会生成的，
    对skill自身目录运行时只做结构存在性检查，文件缺失不FAIL。
    """
    issues = []

    # 这些是 OUTPUT 产物，缺失只 WARN
    output_files = ["style.yaml", "references/style_manual.md"]
    for rel in output_files:
        path = style_dir / rel
        if not path.exists():
            issues.append(f"[WARN] Output not ready (will exist after style learning): {rel}")

    # platform_styles/ 目录本身必须存在
    platform_dir = style_dir / "references/platform_styles/"
    if not platform_dir.exists():
        issues.append("[WARN] references/platform_styles/ does not exist yet (normal before onboarding)")

    # 如果目录存在但为空，只WARN
    if platform_dir.exists():
        platform_files = list(platform_dir.glob("*.md"))
        if len(platform_files) == 0:
            issues.append("[WARN] references/platform_styles/ is empty")

    passed = not any(i.startswith("[FAIL]") for i in issues)
    return passed, issues


# ============ IP名称一致性检查 ============

def extract_ip_name(text: str) -> List[str]:
    """从文本中提取疑似IP自称的词（人名/昵称/品牌名）"""
    # 常见自称模式
    patterns = [
        r"^#\s+(.+?)$",                    # Markdown H1
        r"^##\s+(.+?)$",                   # Markdown H2
        r"^\*\*(.+?)\*\*",                  # 粗体
        r"^-\s+(.+?)$",                    # 列表项
        r"作者[：:]\s*(.+)",               # "作者：XXX"
        r"我是\s+(.{2,8}?)(?:，|。|$)",    # "我是XXX，"
        r"^【(.+?)】",                     # 【】包裹
    ]
    candidates = set()
    for p in patterns:
        for m in re.finditer(p, text, re.MULTILINE):
            val = m.group(1).strip()
            if len(val) >= 2 and len(val) <= 10 and not val.startswith("http"):
                candidates.add(val)
    return list(candidates)


def check_ip_consistency(style_dir: Path) -> Tuple[bool, List[str]]:
    """
    检查IP名称一致性（按平台）。
    规则：IF 提取到了 → 全文件一致；IF 未提取到 → 跳过。
    """
    issues = []

    style_manual = style_dir / "references/style_manual.md"
    if not style_manual.exists():
        return True, ["[SKIP] references/style_manual.md not found"]

    content = style_manual.read_text(encoding="utf-8")
    ip_names = extract_ip_name(content)

    if not ip_names:
        return True, ["[SKIP] No IP name extracted from style_manual.md"]

    # 检查各平台手册中的IP名称一致性
    platform_dir = style_dir / "references/platform_styles/"
    if not platform_dir.exists():
        return True, ["[SKIP] references/platform_styles/ not found"]

    for pf in platform_dir.glob("*.md"):
        pcontent = pf.read_text(encoding="utf-8")
        pnames = extract_ip_name(pcontent)

        # 提取到的自称应该一致
        # 检查：style_manual 中出现的自称，在平台文件中是否也出现
        for name in ip_names:
            # 如果 IP 名在 style_manual 中出现频率高，但在平台文件中未出现
            style_count = content.count(name)
            platform_count = pcontent.count(name)
            if style_count >= 2 and platform_count == 0:
                issues.append(
                    f"[WARN] IP name '{name}' appears {style_count}x in style_manual.md "
                    f"but 0x in {pf.name} — possible inconsistency"
                )

    passed = len([i for i in issues if i.startswith("[FAIL]")]) == 0
    return passed, issues


# ============ 内容标准检查 ============

def check_content_standards(style_dir: Path) -> Tuple[bool, List[str]]:
    """
    检查内容标准：
    1. style_manual.md ≥500 字符
    2. platform_styles/*.md ≥200 字符
    3. 无未替换的 {} 占位符
    """
    issues = []

    # style_manual.md 字符数
    style_manual = style_dir / "references/style_manual.md"
    if style_manual.exists():
        content = style_manual.read_text(encoding="utf-8")
        char_count = len(content)
        if char_count < MIN_STYLE_MANUAL_CHARS:
            issues.append(
                f"[FAIL] references/style_manual.md has {char_count} chars "
                f"(minimum {MIN_STYLE_MANUAL_CHARS})"
            )
        else:
            issues.append(f"[PASS] style_manual.md: {char_count} chars")

    # platform_styles/*.md 字符数
    platform_dir = style_dir / "references/platform_styles/"
    if platform_dir.exists():
        for pf in sorted(platform_dir.glob("*.md")):
            pcontent = pf.read_text(encoding="utf-8")
            char_count = len(pcontent)
            if char_count < MIN_PLATFORM_STYLE_CHARS:
                issues.append(
                    f"[FAIL] {pf.name} has {char_count} chars "
                    f"(minimum {MIN_PLATFORM_STYLE_CHARS})"
                )
            else:
                issues.append(f"[PASS] {pf.name}: {char_count} chars")

    # {} 占位符检查（所有md文件）
    for md_file in style_dir.rglob("*.md"):
        mcontent = md_file.read_text(encoding="utf-8")
        # 查找未被转义的 {}
        placeholders = re.findall(r"(?<!\\)\{[^{}]+\}", mcontent)
        if placeholders:
            # 排除掉正常的正则等合法用途
            illegal = [p for p in placeholders if not re.match(r"^\{[^{:]+\}$", p)]
            # 宽松：只报告连续出现的未填充占位符
            if len(illegal) > 0:
                issues.append(
                    f"[WARN] {md_file.relative_to(style_dir)}: "
                    f"found {len(illegal)} potential unfilled placeholders: {illegal[:3]}"
                )

    passed = not any(i.startswith("[FAIL]") for i in issues)
    return passed, issues


# ============ 提取完整性检查 ============

def check_dimension_completeness(style_dir: Path) -> Tuple[bool, List[str]]:
    """检查8+11维度是否全部完成"""
    issues = []

    style_manual = style_dir / "references/style_manual.md"
    if not style_manual.exists():
        return False, ["[FAIL] references/style_manual.md not found"]

    content = style_manual.read_text(encoding="utf-8")

    # 检查维度关键词
    dimension_keywords = {
        "标题格式": ["标题", "标题格式"],
        "段落结构": ["段落", "段落结构"],
        "句式特征": ["句式", "句式特征"],
        "词汇特征": ["词汇", "词汇特征", "比喻词", "术语"],
        "分析逻辑": ["分析逻辑", "因果", "逻辑"],
        "数据规范": ["数据", "数据规范", "精确度"],
        "固定表达": ["固定表达", "开头语", "结尾格式"],
        "数据需求": ["数据需求", "必需数据"],
    }

    # 额外3个维度（小红书场景）
    extra_keywords = {
        "段落强制开头语": ["强制开头", "开头语"],
        "比喻体系": ["比喻", "比喻体系"],
        "图片使用": ["图片", "图片使用", "封面", "尾页"],
    }

    all_keywords = {**dimension_keywords, **extra_keywords}

    missing_dims = []
    for dim, keywords in all_keywords.items():
        if not any(kw in content for kw in keywords):
            missing_dims.append(dim)

    if missing_dims:
        issues.append(f"[FAIL] Missing dimensions: {', '.join(missing_dims)}")
    else:
        issues.append(f"[PASS] All {len(all_keywords)} dimensions present")

    passed = not any(i.startswith("[FAIL]") for i in issues)
    return passed, issues


# ============ 主流程 ============

def run_self_eval(style_dir: str, format_only: bool = False) -> Dict[str, Any]:
    style_dir = Path(style_dir)
    all_issues = {}
    all_passed = True

    print(f"\n{'='*50}")
    print(f"[CHECK] 爆款智坊 风格学习 自测评")
    print(f"{'='*50}")
    print(f"   Style dir: {style_dir}")

    # 1. SKILL.md 格式校验（style-learning 子技能的 SKILL.md）
    print(f"\n[1/4] SKILL.md 格式校验...")
    skill_md = style_dir / "skills/style-learning/SKILL.md"
    passed, issues = validate_skill_md(skill_md)
    all_issues["skill_md"] = issues
    all_passed = all_passed and passed
    for i in issues:
        print(f"   {i}")

    # 2. 风格档案目录结构
    print(f"\n[2/4] 风格档案目录结构...")
    passed, issues = validate_style_dir(style_dir)
    all_issues["style_dir"] = issues
    all_passed = all_passed and passed
    for i in issues:
        print(f"   {i}")

    if format_only:
        print("\n[SKIP] 内容标准/维度完整性（--format-only 模式）")
        print("\n" + "="*50)
        result = {
            "passed": all_passed,
            "issues": all_issues,
            "format_only": True,
        }
        print(f"   [{'PASS' if all_passed else 'FAIL'}]")
        return result

    # 3. 内容标准（行数 + 占位符）
    print(f"\n[3/4] 内容标准检查...")
    passed, issues = check_content_standards(style_dir)
    all_issues["content_standards"] = issues
    all_passed = all_passed and passed
    for i in issues:
        print(f"   {i}")

    # 4. 维度完整性
    print(f"\n[4/4] 维度完整性检查...")
    passed, issues = check_dimension_completeness(style_dir)
    all_issues["dimension_completeness"] = issues
    all_passed = all_passed and passed
    for i in issues:
        print(f"   {i}")

    # 5. IP名称一致性（可选）
    print(f"\n[5/5] IP名称一致性（按平台）...")
    passed, issues = check_ip_consistency(style_dir)
    all_issues["ip_consistency"] = issues
    for i in issues:
        print(f"   {i}")

    print("\n" + "="*50)
    if all_passed:
        print(f"   [PASS] All checks passed")
    else:
        fail_count = sum(1 for v in all_issues.values() for i in v if i.startswith("[FAIL]"))
        print(f"   [FAIL] {fail_count} issue(s) found")

    return {
        "passed": all_passed,
        "issues": all_issues,
        "format_only": format_only,
        "timestamp": datetime.now().isoformat(),
    }


# ============ CLI ============

def main():
    parser = argparse.ArgumentParser(
        description="爆款智坊 风格学习自测评工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python self_eval.py --style-dir ../../..
  python self_eval.py --style-dir ../../.. --format-only
  python self_eval.py --style-dir ../../.. --output eval_report.json
        """
    )
    parser.add_argument("--style-dir", required=True, help="风格档案根目录（向上追溯到爆款智坊根目录）")
    parser.add_argument("--format-only", action="store_true", help="仅格式校验，不检查内容标准")
    parser.add_argument("--output", default=None, help="JSON报告输出路径")

    args = parser.parse_args()

    result = run_self_eval(args.style_dir, format_only=args.format_only)

    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n[REPORT] saved: {args.output}")

    exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
