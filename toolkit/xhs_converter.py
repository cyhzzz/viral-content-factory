"""
小红书笔记 Converter — 将 Markdown 转为小红书格式。

仅处理格式转换：emoji 注入、标签提取、段落短化。
内容改写由 LLM 在 platform-adaptation 流程中完成。

Usage:
    from xhs_converter import XHSConverter
    converter = XHSConverter()
    result = converter.convert(markdown_text)
"""

from dataclasses import dataclass


@dataclass
class XHSResult:
    """Result of a Markdown → 小红书格式 conversion."""
    title: str
    body: str          # 带emoji和标签的正文
    tags: list[str]    # 提取的话题标签
    image_prompts: list[str]  # 配图提示词列表


class XHSConverter:
    """将 Markdown 转为小红书格式。"""

    def convert(self, markdown_text: str) -> XHSResult:
        """
        转换 Markdown 为小红书格式。

        注意：实际的内容改写（口语化、短段落、emoji注入）
        由 LLM 在 skills/platform-adaptation 流程中完成。
        本 Converter 仅处理结构化输出。
        """
        lines = markdown_text.strip().split("\n")

        title = ""
        body_lines = []
        tags = []
        image_prompts = []

        in_image_prompts = False
        for line in lines:
            line = line.strip()

            # 提取配图提示词区域
            if "配图提示词" in line or "## 配图" in line:
                in_image_prompts = True
                continue
            if in_image_prompts and line.startswith("### 图"):
                prompt = line.replace("### 图", "").strip()
                if prompt:
                    image_prompts.append(prompt)
                continue
            if in_image_prompts and line.startswith("#"):
                in_image_prompts = False

            # 提取标题
            if line.startswith("# ") and not title:
                title = line[2:].strip()
                continue

            # 提取标签
            if line.startswith("#"):
                # 处理 #标签1 #标签2 这种连续标签行
                parts = line.split("#")
                for part in parts:
                    tag = part.strip()
                    if tag and len(tag) > 1:
                        tags.append(tag)
                continue

            # 跳过图片路径
            if line.startswith("![]") or line.startswith("[图片"):
                continue

            # 跳过空行（保留结构）
            if not line:
                body_lines.append("")
                continue

            # 保留正文行
            body_lines.append(line)

        return XHSResult(
            title=title,
            body="\n".join(body_lines).strip(),
            tags=tags,
            image_prompts=image_prompts,
        )
