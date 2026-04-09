# 爆款智坊 v2 (Viral Content Factory)

多平台新媒体内容创作套件 —— 从工作空间初始化到风格学习，从热点抓取到多平台稿件输出，从单次创作到持续进化。**一句话搞定，越用越像你。**

**核心升级（v2）**：
- 两阶段初始化：自动创建规范的工作空间 + 引导式风格录入
- 10 文件结构化记忆库：金句/标题/素材/观点/选题/效果/对标/日历/反馈/读者
- 持续进化框架：风格飞轮 + 标题自学习 + 人格微调 + 防污染机制

兼容 [Claude Code](https://docs.anthropic.com/en/docs/claude-code) 和 [OpenClaw](https://github.com/anthropics/openclaw) / [WorkBuddy](https://www.codebuddy.cn) 的 skill 格式。

## 一句话说明

安装后说「写一篇公众号文章」即可触发完整流程。首次使用会引导你设置工作空间和写作风格，之后每次只需一句话。

## 它能做什么

```
"写一篇公众号文章"
  → 初始化检查 → 热点抓取 → 选题评分(去重) → 框架选择
  → 素材采集(WebSearch真实数据) → 内容增强
  → 写作(风格注入+记忆资产+编辑锚点) → SEO优化
  → 多平台改写(7个平台原生适配) → 排版输出HTML
  → 记忆沉淀(金句/标题/素材自动入库)
```

## 核心能力矩阵

| 能力类别 | 能力 | 说明 | 实现 |
|---------|------|------|------|
| **初始化** | 工作空间创建 | 自动创建7个规范子目录+README | SKILL.md Init R1 |
| **初始化** | 风格学习 | 从范文提取8维度风格指纹 | skills/style-learning |
| **初始化** | 记忆种子 | 首次分析时自动填充记忆库 | memory/*.md |
| **热点** | 热点抓取 | 微博+头条+百度实时热搜 | scripts/fetch_hotspots.py |
| **选题** | 选题生成 | 10选题×3维度评分+历史去重 | references/topic-selection.md + memory/topics.md |
| **素材** | 素材采集 | WebSearch真实数据/引述/案例 | SKILL.md Step 2 + memory/materials.md |
| **框架** | 框架生成 | 7套写作骨架 | references/frameworks.md |
| **增强** | 内容增强 | 按框架类型匹配策略 | references/content-enhance.md |
| **写作** | 文章写作 | 风格注入+记忆资产+编辑锚点 | references/writing-guide.md |
| **SEO** | SEO优化 | 标题策略/摘要/关键词/标签 | references/seo-rules.md |
| **视觉** | 视觉AI | 封面3创意+内文3-6配图 | toolkit/image_gen.py |
| **排版** | 排版引擎 | 16+主题+微信兼容修复+暗黑模式 | toolkit/cli.py |
| **改写** | 多平台改写 | 7平台原生格式适配 | skills/platform-adaptation |
| **进化** | 风格飞轮 | 学习用户修改，更新playbook | references/learn-edits.md + playbook.md |
| **进化** | 标题自学习 | 效果档案→高效模式→偏好画像 | memory/titles.md |
| **进化** | 金句复用 | 风格标签化金句库+句式模式提炼 | memory/golden-sentences.md |
| **进化** | 人格微调 | 每次学习后微调语气参数±0.2~0.3 | SKILL.md 进化机制 |
| **进化** | 效果复盘 | 文章数据回填+高效模式分析 | memory/performance.md |
| **复盘** | 范文风格库 | SICO式few-shot：从你的文章提取风格指纹 | scripts/extract_exemplar.py |
| **工具** | 排版学习 | 从公众号URL提取排版主题 | scripts/learn_theme.py |
| **工具** | 文章采集 | 从公众号URL提取正文为Markdown | scripts/fetch_article.py |

## 写作人格

像选排版主题一样选写作风格。在 `style.yaml` 里一行配置：

```yaml
writing_persona: "midnight-friend"
```

| 人格 | 适合 | 风格特点 |
|------|------|---------|
| `midnight-friend` | 个人号/自媒体 | 极度口语化、高自我怀疑、每段第一人称 |
| `warm-editor` | 生活/文化/情感 | 温暖叙事、故事嵌套数据、柔和情绪弧 |
| `industry-observer` | 行业媒体/分析 | 中性分析、数据先行、稳中带刺 |
| `sharp-journalist` | 新闻/评论 | 犀利简洁、数据驱动、强观点 |
| `cold-analyst` | 财经/投研 | 冷静克制、逻辑链条、风险意识强 |

每个人格定义了语气浓度、数据呈现方式、情绪弧线、不确定性表达模板等参数。详见 `personas/` 目录。

## v2 新增：持续进化系统

### 记忆库架构

爆款智坊 v2 新增 10 个结构化记忆文件，每次创作后自动沉淀：

```
memory/
├── feedback.md            ★ 用户偏好（最高优先级）
├── viewpoints.md          核心观点与立场
├── performance.md         效果数据与高效模式
├── titles.md              标题自学习系统
├── topics.md              选题库（自动去重）
├── calendar.md            内容发布日历
├── benchmarks.md          对标账号追踪
├── audience.md            读者画像
├── golden-sentences.md    金句库（风格标签化）
└── materials.md           可复用素材库
```

### 进化机制

- **风格飞轮**：初稿需改30% → 学习5次→15% → 学习20次→5%
- **标题自学习**：5篇初步偏好 → 20篇完整画像 → 50篇显著优于初始
- **人格微调**：每次学习后自动微调语气参数（±0.2~0.3），有上下限保护
- **防污染机制**：单次修改不超过30%、冲突规则需3次确认、临时调整不写入长期
- **冲突检测**：新旧偏好矛盾时主动展示让用户选择

### 与原有系统的关系

| 原有系统 | 职责 | 与记忆库的关系 |
|---------|------|--------------|
| style.yaml | 写作风格配置 | 管理怎么写 |
| playbook.md | 学习飞轮产出的硬性规则 | 管理必须遵守的约束 |
| memory/ (新增) | 内容资产管理 | 管理写什么、写过什么、效果如何 |

三者互补，不互相替代。

## 工作空间

首次使用时自动创建规范的目录结构：

```
workspace/
├── README.md       # 工作空间说明
├── drafts/         # 草稿区
├── published/      # 已发布区
├── assets/         # 素材资源（封面/配图/图表/截图）
│   ├── covers/
│   ├── illustrations/
│   ├── charts/
│   └── screenshots/
├── research/       # 调研笔记（选题/对标/热点）
│   ├── topics/
│   ├── competitors/
│   └── hotspots/
├── templates/      # 自定义模板库
└── archive/        # 历史归档
```

## 排版引擎

### 16 个主题

```bash
# 浏览器内预览所有主题（并排对比 + 一键复制）
python3 toolkit/cli.py gallery

# 列出主题名称
python3 toolkit/cli.py themes
```

| 类别 | 主题 |
|------|------|
| 通用 | `professional-clean`（默认）、`minimal`、`newspaper` |
| 科技 | `tech-modern`、`bytedance`、`github` |
| 文艺 | `warm-editorial`、`sspai`、`ink`、`elegant-rose` |
| 商务 | `bold-navy`、`minimal-gold`、`bold-green` |
| 风格 | `bauhaus`、`focus-red`、`midnight` |

所有主题均支持微信暗黑模式。

### 微信兼容性自动修复

| 问题 | 自动修复 |
|------|---------|
| 外链被屏蔽 | 转为上标编号脚注 + 文末参考链接 |
| 中英混排无间距 | CJK-Latin 自动加空格 |
| 加粗标点渲染异常 | 标点移到 `</strong>` 外 |
| 原生列表不稳定 | `<ul>/<ol>` 转样式化 `<section>` |
| 暗黑模式颜色反转 | 注入 `data-darkmode-*` 属性 |
| `<style>` 被剥离 | 所有 CSS 内联注入 |

### 容器语法

````markdown
::::dialogue
你好，请问这个功能怎么用？
> 很简单，直接在 Markdown 里写就行。
::::

::::timeline
**2024 Q1** 立项启动
**2024 Q3** MVP 上线
::::

::::callout tip
提示框，支持 tip / warning / info / danger。
::::

::::quote
好的排版不是让读者注意到设计，而是让读者忘记设计。
::::
````

## 安装

**Claude Code**：

```bash
npx skills add cyhzzz/finance_aigc_skills/viral-content-factory
```

**OpenClaw / WorkBuddy**：

将 viral-content-factory 文件夹放入 skills 目录即可。

### 配置（可选）

```bash
cp config.example.yaml config.yaml
```

填入微信公众号 appid/secret 和图片 API key（生图需要）。不配也能用——降级为本地 HTML + 输出图片提示词。

## 快速开始

```
你：写一篇公众号文章             → 首次触发两阶段初始化
你：写一篇关于AI Agent的公号文    → 正常全流程
你：交互模式，写一篇效率工具推文   → 选题/框架处暂停确认
你：帮我润色刚才那篇             → 快速润色
你：学习我的修改                 → 飞轮学习 + 更新记忆库
你：看看有什么主题               → 选题展示
你：换成sspai主题               → 切换排版主题
你：看看文章数据怎么样            → 效果复盘
你：做一个小绿书                  → 图片帖
你：检查一下                      → 质量自检报告
你：导入范文                      → 风格库建库
你：查看我的金句                  → 浏览金句库
你：添加对标账号XX               → 录入benchmarks
你：学习排版                      → 从公号文章提取排版主题
```

## 完整目录结构

```
viral-content-factory/
├── SKILL.md                    # 主管道（v2: 含两阶段初始化 + 记忆系统 + 进化机制）
├── README.md                   # 本文件
├── config.example.yaml         # API 配置模板
├── style.example.yaml          # 风格配置模板
├── writing-config.example.yaml # 写作参数模板
├── requirements.txt
│
├── memory/                     # ★ v2新增：结构化记忆库（10个文件）
│   ├── README.md               # 记忆库使用规范
│   ├── golden-sentences.md     # 金句库
│   ├── viewpoints.md           # 观点与立场
│   ├── titles.md               # 标题自学习
│   ├── topics.md               # 选题库
│   ├── performance.md          # 效果复盘
│   ├── benchmarks.md           # 对标账号
│   ├── calendar.md             # 内容日历
│   ├── feedback.md             # 反馈记录（★最高优先级）
│   ├── materials.md            # 素材库
│   └── audience.md             # 读者画像
│
├── dist/openclaw/              # OpenClaw 兼容版
│
├── scripts/                    # 数据采集 + 诊断 + 构建
│   ├── fetch_hotspots.py        # 多平台热点抓取
│   ├── seo_keywords.py          # SEO 关键词分析
│   ├── fetch_stats.py           # 微信文章数据回填
│   ├── build_playbook.py        # 从历史生成 Playbook
│   ├── learn_edits.py           # 学习人工修改
│   ├── humanness_score.py       # 文章质量打分（11项检测）
│   ├── extract_exemplar.py      # 范文风格提取
│   ├── learn_theme.py           # 提取排版主题
│   ├── fetch_article.py         # 公号URL→Markdown
│   ├── diagnose.py              # 配置完备度检查
│   └── build_openclaw.py        # SKILL.md→OpenClaw转换
│
├── toolkit/                     # Markdown→微信工具链
│   ├── cli.py                   # CLI（preview/gallery/themes/image-post）
│   ├── converter.py             # Markdown→内联样式HTML+微信兼容修复
│   ├── theme.py                 # YAML主题引擎
│   ├── publisher.py             # 微信草稿箱API + 小绿书
│   ├── wechat_api.py            # access_token/图片上传
│   ├── image_gen.py             # AI图片生成（9provider，自动fallback）
│   └── themes/                  # 16+排版主题（含暗黑模式）
│
├── personas/                    # 5套写作人格预设
│
├── references/                  # Agent按需加载
│   ├── writing-guide.md         # 写作规范+质量检查
│   ├── frameworks.md            # 7种写作框架
│   ├── content-enhance.md       # 内容增强策略
│   ├── topic-selection.md       # 选题评估规则
│   ├── seo-rules.md             # 微信SEO规则
│   ├── visual-prompts.md        # 视觉AI提示词
│   ├── wechat-constraints.md    # 微信平台限制
│   ├── style-template.md        # 风格配置字段
│   ├── exemplar-seeds.yaml      # 通用人类写作模式种子
│   ├── exemplars/               # 用户范文风格库
│   ├── onboard.md               # 首次设置流程
│   ├── learn-edits.md           # 学习飞轮流程
│   └── effect-review.md         # 效果复盘流程
│
├── skills/                      # 子skill定义
│   ├── style-learning           # 风格学习
│   ├── content-type-framework   # 框架选择
│   ├── rewrite                  # 拆解改写
│   ├── review                   # 审校
│   └── platform-adaptation      # 多平台改写
│
├── output/                      # 输出（旧版兼容，v2优先用workspace/）
├── corpus/                      # 历史语料
├── lessons/                     # 修改记录
├── evals/                       # 评测集
├── docs/                        # 文档
├── CLAUDE.md
├── LICENSE
├── VERSION
└── playbook.md                  # 学习飞轮产物（自动维护）
```

运行时自动生成（不入 git）：style.yaml、history.yaml、writing-config.yaml、references/exemplars/*.md、workspace/

## Toolkit 独立使用

```bash
# Markdown → 微信 HTML
python3 toolkit/cli.py preview article.md --theme sspai

# 主题画廊
python3 toolkit/cli.py gallery

# 小绿书/图片帖（横滑轮播，3:4比例，最多20张）
python3 toolkit/cli.py image-post photo1.jpg photo2.jpg -t "标题" -c "描述"

# 抓热点
python3 scripts/fetch_hotspots.py --limit 20

# SEO 分析
python3 scripts/seo_keywords.py --json "AI大模型"

# 范文风格库
python3 scripts/extract_exemplar.py article.md
python3 scripts/extract_exemplar.py *.md -s "你的公号"
python3 scripts/extract_exemplar.py --list

# 文章质量检查
python3 scripts/humanness_score.py article.md --verbose

# 从公号文章学习排版主题
python3 scripts/learn_theme.py https://mp.weixin.qq.com/s/xxxx --name my-style
```

## License

MIT
