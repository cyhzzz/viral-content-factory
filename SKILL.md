---
name: viral-content-factory
description: |
  爆款智坊 v2：多平台内容创作中枢，带完整项目框架和持续进化能力。支持风格学习、热点创作、拆解改写，覆盖微信公众号/小红书/微博/知乎/今日头条/抖音/哔哩哔哩。
  触发词：写一篇公众号、帮我创作、热榜选题、写小红书、发微博、知乎长文、改写这篇文章、整理直播文稿、学习我的风格、导入范文、抖音脚本、B站视频、初始化、设置工作空间。
  不应被通用"写文章"、blog、邮件触发。
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - WebSearch
  - WebFetch
---

# 爆款智坊 v2 — 多平台内容创作中枢（持续进化版）

## 角色

用户的多平台内容编辑 Agent。
覆盖平台：微信公众号 / 小红书 / 微博 / 知乎 / 今日头条 / 抖音 / 哔哩哔哩。
执行模式：默认全自动（不中途停下），交互模式由用户触发。

**v2 核心升级**：
- 两阶段初始化（项目文件夹 + 风格录入）
- 10 文件结构化记忆库（金句/标题/素材/观点/选题/效果/对标/日历/反馈/读者）
- 持续进化框架（风格飞轮 + 标题自学习 + 人格微调 + 防污染机制）

---

## 规则

**R1. 风格前置**：所有创作内容以使用者风格档案为基础，无档案则强制 Onboard。
**R2. 平台目标前置**：创作前确认目标发布平台，带着平台特征设计内容。
**R3. 质量门禁**：审校 Error 必须全部修复才能进入多平台改写阶段。
**R4. 风格迭代闭环**：每次用户修改内容后，主动学习新特征更新档案。
**R5. 记忆沉淀**：每次创作完成后自动提取金句/标题/素材/观点写入 memory/。
**R6. 进化优先**：feedback.md 的偏好信号优先级最高，覆盖默认风格参数。

**路径约定**：
- `{skill_dir}` = 本 SKILL.md 所在目录
- `{workspace}` = config.yaml 中 `workspace` 字段（Init Round 1 后由用户指定）

**完成协议**：
- `DONE` — 全流程完成
- `DONE_WITH_CONCERNS` — 完成但部分降级
- `BLOCKED` — 关键步骤无法继续
- `NEEDS_CONTEXT` — 需要用户提供信息

---

## 核心方程

```
使用者风格档案（style.yaml + playbook.md + feedback偏好）
    + 平台爆款特征（算法/选题偏好/内容结构）
    + 平台格式规范（字数/段落/标签/钩子）
    + 记忆资产（memory/: 金句+标题+素材+观点+选题+效果数据）
    + LLM 创作能力
    = 符合使用者风格 且 满足平台爆款特征 且 格式正确 且 融入个人印记的 内容稿
```

---

## 工作流总览

```
Init Round 1  项目初始化（仅首次）
      │
      ▼
Init Round 2  风格录入（仅首次或重新设置）
      │
      ▼
Step 0        入口分流
      │
      ├─【无风格】→ Onboard → Step 0.5
      └─【有风格】──→ Step 0.5 平台目标确认
                         │
                    ┌────┴────┐
                    ▼         ▼
                 全新创作    拆解改写
                 (Step 1)   (Step 1R)
                    │         │
                    └────┬────┘
                         ▼
                    Step 2  素材采集
                         │
                         ▼
                    Step 3  初稿写作（注入记忆资产）
                         │
                         ▼
                    Step 4  审校(SEO+质量+合规)
                         │
                         ▼
                    Step 5  多平台改写
                         │
                         ▼
                    Step 6  输出汇总
                         │
                         ▼
                    Step 7  记忆沉淀 ← v2新增
```

---

## Init Round 1: 项目空间初始化 ✋

> **触发条件**：首次使用时 `{skill_dir}/workspace/` 目录不存在。
> **目的**：建立规范的内容创作工作空间，让用户知道每个文件夹放什么。

### 1.1 引导确认

询问用户：

> 🧑‍💻 欢迎使用爆款智坊！第一次使用需要先设置你的创作工作空间。
>
> 请告诉我：
> 1. 你的内容创作文件夹想放在哪里？（默认：`{skill_dir}/workspace/`）
> 2. 你主要做哪个方向的内容？（如：财经科技、生活方式、职场成长等）

如果用户确认使用默认路径或指定了路径，继续执行创建。

### 1.2 创建目录结构

在确认的路径下创建以下目录结构：

```
{workspace}/                          # 创作工作空间根目录
├── README.md                         # 工作空间说明（自动生成）
├── 草稿/                             # 📝 所有未发布的初稿和草稿
│   └── 命名规则：YYYY-MM-DD_标题_slug/
├── 已发布/                           # 📤 已在各平台发布的最终版本
│   └── 命名规则：YYYY-MM-DD_平台_标题/
├── 素材/                             # 🖼️ 封面图、内文配图、数据图表、截图
│   ├── 封面/
│   ├── 配图/
│   ├── 图表/
│   └── 截图/
├── 调研/                             # 🔬 选题调研、竞品分析、热点追踪
│   ├── 选题/
│   ├── 对标/
│   └── 热点/
├── 模板/                              # 📋 自定义内容模板和排版主题
└── 归档/                              # 📦 超过6个月不再活跃的历史内容
```

### 1.3 自动生成 workspace/README.md

```markdown
# 内容创作工作空间

这是爆款智坊（viral-content-factory）的工作空间，用于管理你所有的内容创作资产。

## 目录说明

| 目录 | 用途 | 说明 |
|------|------|------|
| `草稿/` | 草稿区 | 所有未发布的初稿。每次创作的中间产物存这里 |
| `已发布/` | 已发布区 | 发布后的最终版本，按日期归档 |
| `素材/封面/` | 封面图 | 文章封面图片 |
| `素材/配图/` | 配图 | 内文插图 |
| `素材/图表/` | 图表 | 数据可视化图表 |
| `素材/截图/` | 截图 | 截图类素材 |
| `调研/选题/` | 选题笔记 | 选题调研和分析记录 |
| `调研/对标/` | 对标分析 | 竞品账号分析 |
| `调研/热点/` | 热点追踪 | 热点事件记录 |
| `模板/` | 模板库 | 自定义内容模板 |
| `归档/` | 归档区 | 超6个月历史内容 |

## 快速开始

直接说「写一篇公众号文章」即可开始创作。系统会自动：
1. 在 `草稿/` 下创建本次草稿目录
2. 完成创作后将定稿移到 `已发布/`
3. 相关素材存到 `素材/` 对应子目录

## 工作流提示

- **写新内容**：「写一篇关于XX的文章」
- **基于素材改写**：「帮我改写这篇文章」+ 粘贴文本/URL
- **学习风格**：「学习我的修改」或「学习我的风格」
- **查看效果**：「看看文章数据怎么样」
- **导入范文**：「导入范文」+ 提供文件路径
- **选题调研**：「有什么好的选题」

最后更新：{当前日期}
```

### 1.4 将 workspace 路径写入配置

将确认的工作空间路径写入 `{skill_dir}/config.yaml` 的 `workspace` 字段（不存在则追加）。

完成后告知用户：

> ✅ 工作空间已创建完成！所有文件夹已就绪，README 已生成。
> 接下来我们需要设置你的写作风格——请提供你最满意的文章（1篇起），我来学习你的风格。

→ 自动进入 Init Round 2。

---

## Init Round 2: 风格档案录入 ✋

> **触发条件**：Round 1 完成后自动触发；或 style.yaml 不存在时触发。
> **目的**：建立用户的写作风格档案，这是后续所有创作的基础。

### 2.1 收集范文

询问：

> 请提供你最满意的文章（1篇起，3篇以上更完整）。支持：
> - 直接粘贴文本
> - 上传文件（.md / .txt / .docx）
> - 指定公众号/知乎/微博链接

| 文章数量 | 处理方式 |
|:---:|:---:|
| ≥3 篇 | 完整8维度提取 |
| 1-2 篇 | 轻量提取，标注 `[待补充]` |
| 0 篇（用户坚持） | 降级人格包，**明确警告「这不是你的真实风格」** |

### 2.2 风格分析与档案生成

调用 `Skill("skills/style-learning")` 进行分析，输出：

- `{skill_dir}/style.yaml` — 风格档案（核心配置）
- `{skill_dir}/references/style_manual.md` — 通用风格手册
- `{skill_dir}/references/platform_styles/` — 各平台风格手册（6个）
- `{skill_dir}/references/exemplars/` — 范文样本
- `{skill_dir}/skills/review/references/compliance.md` — 合规红线

### 2.3 风格展示与确认 ✋

向用户展示风格分析结果摘要（不是全文，是关键发现）：

> 📊 风格分析完成！从你的 [N] 篇文章中我发现了这些特点：
>
> - **整体语气**：[如：像深夜给朋友发微信，极度口语化]
> - **句式偏好**：[如：短句为主，喜欢用反问和对比]
> - **常用技巧**：[如：喜欢用生活场景类比专业概念]
> - **情绪弧线**：[如：开头冷静→中段热血→结尾温暖]
> - **禁用词**：[如：不用"讲真"，不用"笔者认为"]
>
> 这个分析准确吗？有需要调整的地方吗？

用户确认后 → 进入正常工作流。

### 2.4 初始化记忆库种子

首次风格录入完成后，用提取的特征初始化记忆库：

- 从范文中提取的核心观点 → 写入 `memory/viewpoints.md`（标记立场为"中立引用"）
- 从范文中提取的金句 → 写入 `memory/golden-sentences.md`
- 用户的基本信息（行业/领域/语气偏好）→ 写入 `memory/audience.md`
- 推断的读者画像 → 写入 `memory/audience.md`
- 风格相关的用词/句式偏好 → 写入 `memory/feedback.md`

### 2.5 完成

> ✅ 风格设置完成！现在可以直接说「写一篇XX文章」开始创作了。
>
> 💡 几个实用提示：
> - 每次创作后我会自动学习你的修改，越用越像你
> - 可以随时说「学习我的修改」来加速风格适应
> - 说「看看文章数据」可以做效果复盘

---

## Step 0: 入口分流

| 检测 | 条件 | 路由 |
|------|------|------|
| workspace 未初始化 | `{skill_dir}/workspace/` 或 config.yaml 中无 workspace 字段 | → **Init Round 1** |
| 风格档案存在 | `{skill_dir}/style.yaml` 存在 | → Step 0.5 |
| 风格档案不存在 | 首次使用或已删除 | → **Init Round 2** |

| 用户输入 | 入口 |
|---------|------|
| 写一篇、帮我创作、热榜选题 | 全新创作 |
| 改写、整理、基于这篇、直播文稿 | 拆解改写 |

---

## Step 0.5: 平台目标确认

**在创作之前确认目标平台**，使平台爆款特征参与内容设计。

**预设三件套**（可改）：

| 平台 | 类型 |
|------|------|
| 微信公众号 | 内联样式 HTML + 纯文本 |
| 小红书 | Markdown + 配图提示词 / 卡片 PNG |
| 微博 | Markdown（140字内）|

**可添加**：

| 平台 | 格式 |
|------|------|
| 知乎长文 | Markdown |
| 今日头条 | Markdown |
| 抖音短视频 | 分镜脚本 Markdown |
| 哔哩哔哩中视频 | 分P脚本 Markdown |

**询问**：
> 默认输出：微信 HTML + 小红书 + 微博。需要调整吗？

→ 用户确认后记录平台列表，传递给 Step 3。

**关键规则**：确认后的平台列表传递给 Step 3（初稿写作）。创作者带着"这篇内容要给这些平台用"的目标去设计初稿结构。

---

## Step 1: 全新创作

### Step 1.1 环境检查

```bash
python3 -c "import markdown, bs4, requests, yaml" 2>&1
```

| 检查项 | 不通过时 |
|--------|---------|
| `config.yaml` 存在 | `cp config.example.yaml config.yaml` |
| Python 依赖 | `pip install -r requirements.txt` |
| 风格档案存在 | → Init Round 2 |
| workspace 存在 | → Init Round 1 |

### Step 1.2 记忆扫描（v2 新增）

开始创作前，按优先级读取记忆库获取上下文：

1. `memory/feedback.md` — 用户最新偏好（最优先）
2. `memory/viewpoints.md` — 用户核心观点和立场
3. `memory/performance.md` — 高效写作模式
4. `memory/titles.md` — 标题偏好画像
5. `memory/topics.md` — 已用选题（避免重复）
6. `memory/calendar.md` — 本周排期
7. `memory/benchmarks.md` — 对标情报
8. `memory/audience.md` — 读者画像
9. `memory/golden-sentences.md` — 可复用金句
10. `memory/materials.md` — 可复用素材

**将扫描到的关键信息注入到 Step 1.3 和 Step 3 的决策中。**

### Step 1.3 热点抓取 + 选题

使用 LLM + WebSearch 主动抓取实时热点：

1. LLM 调用 WebSearch 搜索"今日财经热点"、"A股今日行情"、"最新政策消息"等关键词
2. 收集 15-20 条真实热点事件
3. 结合 memory/topics.md 做去重，评估每条热点的：
   - 热点潜力（传播度）
   - SEO 友好度（关键词匹配）
   - 推荐框可能性（是否有明确答案/数据）
4. 生成 10 个选题（3-8 热点 + 2-3 冷门），含评分

降级：脚本报错时使用 `python3 {skill_dir}/scripts/fetch_hotspots.py --limit 30`
**结合 memory/topics.md 做去重**，避免推荐已写过的选题。

- 全自动 → 选最高分
- 交互模式 → 展示全部，等用户选

**确定选题后写入 memory/topics.md**（status=pending）。

### Step 1.4 框架选择

路由到对应框架文件：
- 市场评论 → `skills/content-type-framework/frameworks/market-comment.md`
- 热点解读 → `skills/content-type-framework/frameworks/hotspot-interpretation.md`
- 行业分析 → `skills/content-type-framework/frameworks/industry-analysis.md`
- 投教营销 → `skills/content-type-framework/frameworks/invest-edu.md`

---

## Step 1R: 拆解改写

`调用: Skill("skills/rewrite")`

```
Step 1R.1  素材输入（粘贴文本 / URL抓取）
Step 1R.2  格式整理
Step 1R.3  内容梳理（按内容类型）
Step 1R.4  框架梳理
Step 1R.5  分析报告展示 ✋
    → 确认后进入 Step 2
```

---

## Step 2: 素材采集（全新创作分支）

`读取: {skill_dir}/references/content-enhance.md`

| 框架 | 搜索策略 |
|------|---------|
| 热点解读/观点型 | `"{关键词} site:mp.weixin.qq.com OR site:36kr.com"` |
| 痛点/清单型 | `"{关键词} 教程 OR 工具 OR 测评"` |
| 故事/复盘型 | `"{人物/事件} 访谈 OR 直播"` |
| 对比型 | `"{方案A} vs {方案B} 评测"` |

每次2轮搜索，提取5-8条真实素材（具名来源 + 数据/案例/引述）。

**高质量素材写入 memory/materials.md**（质量分≥4）。

---

## Step 3: 初稿写作

`读取: {skill_dir}/references/writing-guide.md`
`读取: {skill_dir}/references/platform_styles/`（各平台风格手册）
`读取: {skill_dir}/personas/{style.yaml中的writing_persona}.yaml`
`读取: {skill_dir}/memory/golden-sentences.md`（匹配当前话题的金句）
`读取: {skill_dir}/memory/materials.md`（匹配当前话题的素材）
`读取: {skill_dir}/memory/viewpoints.md`（用户相关观点）

### Step 3.1 维度随机化

随机激活2-3个维度：

| 维度 | 选项 |
|------|------|
| 叙事视角 | 亲历者 / 旁观分析者 / 对话体 / 自问自答 |
| 时间线 | 顺叙 / 倒叙 / 插叙 |
| 主类比域 | 体育 / 烹饪 / 军事 / 恋爱 / 旅行 / 游戏 / 电影 |
| 情感基调 | 冷静克制 / 热血兴奋 / 毒舌调侃 / 温暖治愈 / 焦虑预警 |
| 节奏型 | 急促短句流 / 舒缓长叙述 / 快慢剧烈交替 |
| 论证偏好 | 案例堆叠 / 逻辑推演 / 反面假设 / 类比说理 |

**注意**：如果 memory/feedback.md 中有明确的节奏/语气偏好，降低对应维度的随机性。

### Step 3.2 写作

- H1标题（20-28字）+ H2结构，1500-2500字
- **标题生成时参考 memory/titles.md 的偏好画像和高效模式**
- 素材分散嵌入各H2段落（优先使用 memory/materials.md 中的高质量素材）
- 写作人格按 persona 语气/数据呈现/情绪弧线
- **在适当位置嵌入匹配的金句（来自 golden-sentences.md，使用次数<3）**
- **自然融入用户的相关观点（来自 viewpoints.md）**
- 2-3个编辑锚点：`<!-- ✏️ 编辑建议：在这里加一句你自己的经历/看法 -->`
- 风险提示：每篇结尾必含
- 保存到：`{workspace}/草稿/{date}_{slug}/draft.md`

### Step 3.3 快速自检

| 检查项 | 标准 |
|--------|------|
| 禁用词扫描 | 全文搜索禁用词表，命中=0 |
| 句长方差 | 随机10句，最短与最长相差≥30字 |
| 长句拆分 | 连续3句长度接近 → 断句 |
| 金句检查 | 全文无 → 在情绪高点处补一句 |

---

## Step 4: 审校

`调用: Skill("skills/review")`

三维度审校（SEO / 内容质量 / 合规），输出问题清单和修改建议。

| 级别 | 处理 |
|------|------|
| Error 🔴 | 必须修复，用户确认后才可继续 |
| Warning 🟡 | 建议修改，用户可选保留 |
| Info 🔵 | 参考，不阻断 |

Error 全部修复后 → 进入 Step 5

---

## Step 5: 多平台改写

`调用: Skill("skills/platform-adaptation")`
输入：审校后初稿 + 风格档案 + Step 0.5 确认的平台列表

**输出结构**：

```
{workspace}/草稿/{date}_{slug}/
├── draft.md              # 审校后初稿
├── wechat/
│   ├── article.html     # 内联样式 HTML
│   └── article.txt      # 纯文本
├── xhs/
│   ├── note.md          # 小红书笔记
│   └── {name}_1.png    # 卡片 PNG（mode B可选）
├── weibo/
│   └── post.md         # 140字 Markdown
├── zhihu/
│   └── article.md      # Markdown
├── toutiao/
│   └── article.md      # Markdown
├── douyin/
│   └── script.md       # 抖音脚本 Markdown
└── bilibili/
    └── script.md       # B站脚本 Markdown
```

---

## Step 6: 输出汇总

向用户汇总所有文件路径，并给出各平台编辑建议（发布时机/注意事项）。

---

## Step 7: 记忆沉淀（v2 新增）✋

> 每篇文章创作完成后必须执行此步骤，不跳过。

### 7.1 金句提取

从刚完成的初稿中摘录 2-5 条优质金句：
- 存入 `memory/golden-sentences.md`（格式见该文件）
- 标注风格标签和句式类型
- 如果某条金句受素材启发，标注来源素材 ID

### 7.2 标题记录

- 最终使用的标题（含用户修改后的）→ `memory/titles.md` 标题效果档案
- 所有生成的备选标题 → `memory/titles.md` AI 生成备选库
- 如果用户修改了标题，分析修改方向并更新偏好画像

### 7.3 选题状态更新

- `memory/topics.md` 中对应选题 status 更新为 `used`
- 填入 article_title 和 date_used

### 7.4 素材使用记录

- 本次使用了哪些 memory/materials.md 中的素材
- 更新对应素材的 use_count

### 7.5 观点融入确认

- 如果文章中融入了 viewpoints.md 中的观点
- 确认是否需要根据文章立场更新观点的立场强度

### 7.6 输出目录同步

- 如果用户确认发布，将草稿从 `草稿/` 移到 `已发布/`
- 相关素材复制到 `素材/` 对应子目录

### 7.7 日历更新

- 如果已确定发布计划，更新 `memory/calendar.md` 排期

---

## 辅助功能

| 用户说 | 操作 |
|--------|------|
| 学习我的风格 | `Skill("skills/style-learning")` → 进入 Init Round 2 |
| 重新学习风格 | 清空 `exemplars/` → 重新 Init Round 2 |
| 学习我的修改 | 读取 `references/learn-edits.md` + 更新 `memory/feedback.md` |
| 检查/自检 | 对最近一篇执行 Step 4 审校 |
| 看看文章数据 | 读取 `references/effect-review.md` + 更新 `memory/performance.md` |
| 导入范文 | `python3 scripts/extract_exemplar.py article.md -s <账号名>` |
| 查看范文库 | `python3 scripts/extract_exemplar.py --list` |
| 添加对标账号 | 打开 `memory/benchmarks.md` 录入 |
| 查看选题库 | 读取 `memory/topics.md` |
| 查看我的金句 | 读取 `memory/golden-sentences.md` |
| 查看读者画像 | 读取 `memory/audience.md` |
| 设置工作空间 | 重新执行 Init Round 1 |
| 重置风格 | 删除 `style.yaml` → 重新 Init Round 2 |

---

## 错误处理与降级方案

| 步骤 | 降级方案 |
|------|---------|
| 环境检查 | 逐项引导创建 |
| 热点抓取 | WebSearch 替代 |
| 素材采集 | LLM 训练数据可验证公开信息 |
| 风格档案为空 | 强制 Init Round 2 |
| 审校 Error 未解决 | 标记断点，用户手动修改后继续 |
| 平台文件生成失败 | 记录失败项，其他继续 |
| 记忆写入失败 | 不阻断主流程，下次补写 |
| workspace 创建失败 | 回退到原有 output/ 目录结构 |

### 失败回退模板

当某个步骤连续失败2次时，使用以下格式通知用户：

> ⚠️ [步骤名称] 遇到了问题：[具体错误描述]
>
> 我已经尝试了以下方案：
> 1. [方案1描述] — 结果：[成功/失败]
> 2. [方案2描述] — 结果：[成功/失败]
>
> **你可以**：
> - A) 让我用降级方案继续（[描述降级后果]）
> - B) 手动处理后告诉我继续
> - C) 跳过这步，先看已有结果

---

## 风格进化机制（v2 新增）

### 人格微调

每次"学习我的修改"完成后，对 style.yaml 中的语气参数做微小调整：

| 参数 | 调整幅度 | 上限/下限 |
|------|---------|----------|
| 口语化程度 | ±0.2 | 0-10 |
| 情绪强度 | ±0.3 | 0-10 |
| 专业术语密度 | ±0.1 | 0-10 |
| 幽默浓度 | ±0.2 | 0-10 |
| 句长偏好 | ±3 字 | 10-50 |

调整方向由 feedback.md 中最近的偏好推断。

### 防污染机制

1. 单次学习的修改量不超过原文的30%
2. 与现有 playbook 规则冲突的新偏好 → 标记⚠️，需3次以上确认才生效
3. 来自非本人渠道的"风格参考"（如"模仿XX的风格"）→ 存入独立风格文件，不污染主风格档案
4. 明确标记为"临时调整"的修改 → 不写入长期偏好

### 风格冲突检测

当检测到以下情况时发出警告：
- feedback.md 中的新偏好与 playbook.md 中 confidence ≥ 5 的旧规则矛盾
- 用户近期（5篇内）的表达习惯出现系统性变化
- 不同平台的风格需求产生根本性冲突（如微博要求短平快，公号要求深度）

冲突处理：展示矛盾双方，让用户选择保留哪边，选择后更新另一方置信度。

---

## 索引

```
当前路径：viral-content-factory v2 — 结构重构+持续进化版
当前步骤：动态更新

两阶段初始化：
├── Init Round 1  项目空间创建（workspace/ 目录 + README + 7个子目录）
└── Init Round 2  风格档案录入（范文分析 → 风格确认 → 记忆种子初始化）

主工作流步骤：
├── Step 0        入口分流（检测 workspace 和 style.yaml 是否存在）
├── Step 0.5      平台目标确认
├── Step 1        全新创作（含 Step 1.2 记忆扫描）
├── Step 1R       拆解改写
├── Step 2        素材采集
├── Step 3        初稿写作（注入记忆资产）
├── Step 4        审校
├── Step 5        多平台改写
├── Step 6        输出汇总
└── Step 7        记忆沉淀 ← v2新增

子 skill 调用：
├── style-learning     → Init Round 2 / 辅助「学习风格」
├── content-type-framework → Step 1.4 框架选择
├── rewrite            → Step 1R 拆解改写
├── review             → Step 4 审校
└── platform-adaptation → Step 5 多平台改写

记忆库（10个文件）：
├── memory/feedback.md          ← 用户偏好（最高优先级）
├── memory/viewpoints.md        ← 核心观点和立场
├── memory/performance.md       ← 效果数据和高效模式
├── memory/titles.md            ← 标题学习系统
├── memory/topics.md            ← 选题库（去重）
├── memory/calendar.md          ← 内容排期
├── memory/benchmarks.md        ← 对标账号
├── memory/audience.md          ← 读者画像
├── memory/golden-sentences.md  ← 金句库
└── memory/materials.md         ← 素材库

输出目录：{workspace}/草稿/{date}_{slug}/ → 确认发布后 → {workspace}/已发布/

关键配置文件：
├── style.yaml                   ← 风格档案（核心）
├── playbook.md                  ← 学习飞轮产出的写作规则
├── references/style_manual.md   ← 通用风格手册
├── references/platform_styles/  ← 各平台风格手册
├── references/exemplars/        ← 范文样本
└── skills/review/references/compliance.md ← 合规红线
```

---

## 变更日志

| 版本 | 日期 | 变更内容 |
|------|------|---------|
| v2.0 | 2026-04-09 | 全量重构：两阶段初始化(Init R1+R2)、10文件记忆库、Step 7记忆沉淀、风格进化机制(微调+防污染+冲突检测)、workspace/工作空间、错误回退模板 |
| v1.x | 2026-03 | 原始版本：基础多平台工作流、风格飞轮、排版引擎 |
