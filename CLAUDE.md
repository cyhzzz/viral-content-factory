# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

爆款智坊 v2 是一个多平台内容创作中枢，覆盖微信公众号 / 小红书图文笔记 / 微博短文案 / 知乎长文 / 今日头条 / 抖音短视频 / 哔哩哔哩中视频脚本。
支持两大入口：全新创作（热点抓取→选题→框架→素材→初稿）和拆解改写（长文/直播转录稿→格式整理→内容梳理→改写）。

**v2 核心升级**：两阶段初始化（工作空间创建 + 风格录入）、10文件结构化记忆库、Step 7 记忆沉淀、持续进化框架。

## 常用命令

### 多平台输出
```bash
# Markdown → 微信 HTML 预览
python3 toolkit/cli.py preview article.md --theme sspai

# 主题画廊（并排对比 + 一键复制）
python3 toolkit/cli.py gallery

# 小绿书/图片帖（横滑轮播）
python3 toolkit/cli.py image-post photo1.jpg photo2.jpg -t "标题" -c "描述"
```

### 数据采集与分析
```bash
# 多平台热点抓取
python3 scripts/fetch_hotspots.py --limit 20

# SEO 关键词分析
python3 scripts/seo_keywords.py --json "AI大模型" "科技股"

# 文章质量检查
python3 scripts/humanness_score.py article.md --verbose
```

### 风格学习
```bash
# 从公众号文章提取排版主题
python3 scripts/learn_theme.py https://mp.weixin.qq.com/s/xxxx --name my-style

# 从文章提取写作风格
python3 scripts/extract_exemplar.py article.md
python3 scripts/extract_exemplar.py --list  # 查看范文库
```

### 配置诊断
```bash
python3 scripts/diagnose.py  # 检查配置完备度
```

## 架构概览

```
爆款智坊/
├── SKILL.md                    # 主管道（v2: 两阶段初始化 + 记忆系统 + 进化机制）
├── WORKFLOW.md                 # v2新增：完整工作流架构文档
├── README.md                   # 用户入口文档
├── config.example.yaml         # API 配置模板
├── style.example.yaml          # 风格配置模板
├── requirements.txt
│
├── workspace/                  # ★ v2新增：规范工作空间（Init Round 1 自动创建）
│   ├── README.md               # 工作空间说明
│   ├── drafts/                 # 草稿区
│   ├── published/              # 已发布区
│   ├── assets/                 # 素材资源（covers/illustrations/charts/screenshots）
│   ├── research/               # 调研笔记（topics/competitors/hotspots）
│   ├── templates/              # 自定义模板库
│   └── archive/                # 历史归档
│
├── memory/                     # ★ v2新增：10文件结构化记忆库
│   ├── README.md              # 记忆库使用规范
│   ├── golden-sentences.md    # 金句库（风格标签+句式模式）
│   ├── viewpoints.md          # 观点立场库（7级强度）
│   ├── titles.md             # 标题自学习（效果档案→高效模式→偏好画像→AI备选库）
│   ├── topics.md             # 选题库（自动去重）
│   ├── performance.md        # 效果复盘+高效模式分析
│   ├── benchmarks.md         # 对标账号追踪
│   ├── calendar.md           # 内容日历+排期规则
│   ├── feedback.md           # 反馈记录（★最高优先级）
│   ├── materials.md         # 素材库（7分类索引）
│   └── audience.md           # 读者画像
│
├── skills/                      # 子技能模块（Skill tool 按需调用）
│   ├── content-type-framework/  # 内容类型路由 + 4类框架
│   │   ├── SKILL.md
│   │   └── frameworks/
│   │       ├── market-comment.md      # 市场评论
│   │       ├── hotspot-interpretation.md # 热点解读
│   │       ├── industry-analysis.md   # 行业分析
│   │       └── invest-edu.md         # 投教营销
│   ├── rewrite/                 # 拆解改写子技能
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── format-organize.md
│   │       ├── content-analyze.md
│   │       └── framework-map.md
│   ├── platform-adaptation/      # 多平台改写子技能
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── wechat-html.md       # 公众号深度方法论+HTML规范
│   │       ├── xhs-card.md          # 小红书CES算法+图文笔记方法论
│   │       ├── weibo-short.md       # 微博广场逻辑+140字爆款方法论
│   │       ├── zhihu-long.md        # 知乎SEO+盐值系统+长文方法论
│   │       ├── toutiao.md           # 今日头条算法+短段落规范
│   │       ├── douyin-script.md     # 抖音流量池+黄金3秒+脚本方法论
│   │       └── bilibili-script.md   # B站Z世代+分P策略+弹幕设计
│   ├── review/                   # 审校子技能
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── seo-rules.md
│   │       ├── quality-check.md
│   │       └── compliance.md
│   └── style-learning/           # 风格学习子技能
│       ├── SKILL.md
│       └── references/
│           ├── style-extract.md
│           ├── author-profile.md
│           └── platform-diff.md
│
├── scripts/                      # 数据采集 + 分析脚本
│   ├── fetch_hotspots.py          # 热点抓取
│   ├── seo_keywords.py            # SEO 评分
│   ├── humanness_score.py        # 质量检查
│   ├── extract_exemplar.py       # 风格提取
│   ├── learn_theme.py            # 排版主题学习
│   ├── learn_edits.py           # 风格飞轮
│   ├── fetch_article.py         # 文章抓取（支持公众号/知乎/微博）
│   └── diagnose.py              # 配置诊断
│
├── toolkit/                       # 多平台输出工具链
│   ├── cli.py                   # CLI（preview/gallery/image-post）
│   ├── converter.py              # 多平台 converter
│   ├── theme.py                 # YAML 主题引擎
│   ├── image_gen.py             # AI 图片生成
│   └── themes/                  # 16+ 排版主题
│
├── personas/                      # 5 套写作人格
│   ├── midnight-friend.yaml
│   ├── warm-editor.yaml
│   ├── industry-observer.yaml
│   ├── sharp-journalist.yaml
│   └── cold-analyst.yaml
│
└── references/                    # 通用参考文档
    ├── writing-guide.md          # 写作规范
    ├── topic-selection.md        # 选题评估
    ├── content-enhance.md       # 内容增强
    ├── effect-review.md          # 效果复盘
    ├── onboard.md               # 首次设置
    └── learn-edits.md           # 学习飞轮
```

## v2 两阶段初始化

### Init Round 1 — 项目空间创建（仅首次）

自动创建 workspace/ 目录，包含 7 个子目录：drafts/、published/、assets/（covers+illustrations+charts+screenshots）、research/（topics+competitors+hotspots）、templates/、archive/
每个子目录都有用途说明，自动生成 workspace/README.md 告诉用户每个文件夹干什么用。

### Init Round 2 — 风格录入（仅首次或 style.yaml 不存在时）

引导用户提供范文（≥3篇最佳），8维度风格拆解 → 展示摘要让用户确认 → 生成 style.yaml，同时初始化记忆库种子（观点/金句/读者画像/反馈偏好）。

## v2 多平台工作流

```
Step 0  Onboarding 检测 + 入口判断
          │
          ├── 无workspace → Init Round 1（自动创建工作空间）
          ├── 无style → Init Round 2（引导式风格录入）
          └── 有两者 → Step 0.5

【全新创作分支】
Step 1  环境检查 → 记忆扫描（10文件按优先级）→ 热点抓取 → 选题评分（去重）→ 框架选择
Step 2  素材采集（WebSearch真实数据）
Step 3  初稿写作（风格注入 + 记忆资产注入 + 编辑锚点）
Step 4  审校（SEO + 内容质量 + 合规）
Step 5  多平台输出选择
Step 6  多平台改写 → 文件输出
Step 7  记忆沉淀（金句/标题/素材/观点/选题自动入库）

【拆解改写分支】
Step 1R URL抓取/粘贴 → 格式整理 → 内容梳理 → 框架梳理 → 分析报告确认
         ↓ 汇入 Step 2
```

## v2 记忆系统

### 记忆文件（memory/ 目录下 10 个文件）

| 文件 | 用途 | 优先级 |
|------|------|--------|
| feedback.md | 用户偏好反馈 | ★★★ 最高 |
| viewpoints.md | 核心观点与立场 | ★★ 高 |
| golden-sentences.md | 金句库（风格标签+句式模式） | ★★ 高 |
| titles.md | 标题自学习（四级体系） | ★★ 高 |
| performance.md | 效果数据+高效模式 | ★★ 高 |
| topics.md | 选题库（自动去重） | ★ 中 |
| materials.md | 素材库（7分类索引） | ★ 中 |
| audience.md | 读者画像 | ★ 中 |
| benchmarks.md | 对标账号追踪 | ★ 中 |
| calendar.md | 内容日历+排期规则 | ★ 低 |

### 进化机制

- **风格飞轮**：初稿需改30% → 学习5次→15% → 学习20次→5%
- **标题自学习**：5篇初步偏好 → 20篇完整画像 → 50篇显著优于初始
- **人格微调**：每次学习后自动微调语气参数（±0.2~0.3），有上下限保护
- **防污染机制**：单次修改不超过30%、冲突规则需3次确认、临时调整不写入长期
- **冲突检测**：新旧偏好矛盾时主动展示让用户选择

### 记忆扫描时机（Step 1.2）

每次创作前按优先级读取10个记忆文件，为后续步骤提供上下文。

### 记忆沉淀时机（Step 7）

每篇文章完成后自动提取金句/标题/素材写入记忆库。

## 输出结构

```
workspace/
├── drafts/                    # 草稿
├── published/                 # 已发布
├── assets/                    # 素材
│   ├── covers/               # 封面图
│   ├── illustrations/        # 配图
│   ├── charts/               # 图表
│   └── screenshots/         # 截图
└── research/                 # 调研

output/platforms/{date}_{title}/   # 旧版兼容
├── draft.md               # 审校后初稿
├── wechat/
│   ├── article.html      # 内联样式 HTML
│   └── article.txt       # 纯文本
├── xhs/
│   ├── note.md           # 小红书笔记
│   └── cards.html        # 卡片 HTML（可选）
├── weibo/
│   └── post.md           # 140字 Markdown
├── zhihu/
│   └── article.md        # 知乎长文
├── toutiao/
│   └── article.md        # 今日头条
├── douyin/
│   └── script.md         # 抖音短视频脚本
└── bilibili/
    └── script.md         # B站中视频脚本
```

## 运行时生成的文件

以下文件由运行时自动生成（不入 git）：
- `style.yaml` - 用户风格配置
- `workspace/` - 工作空间（Init Round 1 创建）
- `references/exemplars/` - 范文风格库
- `references/style_manual.md` - 通用风格手册
- `references/platform_styles/` - 各平台风格手册
- `output/platforms/` - 多平台输出文件

## 微信兼容处理

toolkit/converter.py 自动修复：
- 外链 → 上标编号脚注
- CJK-Latin 自动加空格
- 标点移到 `</strong>` 外
- `<ul>/<ol>` 转样式化 `<section>`
- 暗黑模式颜色反转（`data-darkmode-*` 属性）
- `<style>` 被剥离 → CSS 内联注入
