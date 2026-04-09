# 爆款智坊 多平台改造设计文档

**日期**：2026-04-03
**版本**：v1.2
**状态**：✅ 合规规则已补充 | ✅ 风格学习框架已补充 | ✅ Onboarding+多平台风格确认已补充

---

## 一、核心设计原则

**混合架构**：核心流程（选题→素材→初稿）共用，配图/排版/改写各平台独立。

**两大入口分支**：
- **全新创作**：热点抓取 → 选题评分 → 框架选择 → 素材采集 → 初稿
- **拆解改写**：URL抓取/粘贴 → 格式整理 → 内容梳理 → 框架梳理 → 分析报告确认 → 改写

---

## 二、完整工作流

```
用户触发「全新创作」或「改解改写」
    │
    ├── Step 0  入口判断
    │     ├── 全新创作 → Step 1
    │     └── 拆解改写 → Step 1R
    │
    ├── 【全新创作分支】
    │     └── Step 1  环境检查 + 热点抓取 → 选题评分 → 框架选择
    │                → 素材采集（WebSearch）→ Step 2
    │
    ├── 【拆解改写分支】
    │     └── Step 1R  URL抓取/粘贴 → 格式整理 → 内容梳理 → 框架梳理
    │                       → 分析报告展示（用户可补充素材/调整方向）
    │                       → 确认后进入 Step 2
    │
    ├── Step 2  初稿写作（内容增强 + 风格注入 + 编辑锚点）
    │
    ├── Step 3  多平台输出选择（预设三件套可改）
    │            预设：微信长文 + 小红书笔记 + 微博短文案
    │            可修改：添加/删除/替换目标平台
    │
    ├── Step 4  审校（SEO + 内容质量 + 合规三合一）
    │            ├── SEO优化：标题策略/摘要/关键词/标签
    │            ├── 内容质量审校：深入浅出/吸引力/情绪弧线
    │            └── 合规审校：个股/收益承诺/极端表述
    │            ↑ 用户确认后继续
    │
    └── Step 5  多平台改写
          ├── 微信长文 → HTML 文件 + 纯文本文件
          ├── 小红书 → 标题+正文+配图提示词/卡片HTML
          ├── 微博 → 140字Markdown
          ├── 知乎 → Markdown
          ├── 头条 → Markdown
          └── 短视频 → 脚本Markdown
```

---

## 三、目录结构调整

### 新增目录

```
skills/                              # 子技能模块（Skill tool 按需调用）
├── rewrite/                         # 拆解改写子技能
│   ├── SKILL.md                     # Step 1R 工作流
│   └── references/
│       ├── format-organize.md       # 格式整理规则
│       ├── content-analyze.md       # 内容梳理模板（按4类内容类型）
│       └── framework-map.md          # 框架梳理模板（按4类内容类型）
│
├── style-learning/                  # 风格学习子技能
│   ├── SKILL.md                     # 风格学习工作流
│   └── references/
│       ├── author-profile.md        # 作者定位分析框架
│       ├── style-extract.md          # 写作风格提取规则
│       └── platform-diff.md          # 跨平台差异分析
│
├── review/                           # 审校子技能
│   ├── SKILL.md                     # 审校工作流
│   └── references/
│       ├── seo-rules.md              # SEO规则（沿用）
│       ├── quality-check.md          # 内容质量评估标准
│       └── compliance.md             # 合规审校规则（新增，待用户补充）
│
├── platform-adaptation/              # 多平台改写子技能
│   ├── SKILL.md                     # Step 5 工作流
│   └── references/
│       ├── wechat-html.md            # 微信HTML输出规范
│       ├── xhs-card.md              # 小红书卡片规范
│       ├── weibo-short.md           # 微博140字规范
│       ├── zhihu-long.md            # 知乎长文规范
│       ├── toutiao.md               # 今日头条规范
│       └── video-script.md         # 短视频脚本规范
│
└── content-type-framework/           # 内容类型框架库
    ├── SKILL.md                     # 内容类型路由
    └── frameworks/
        ├── market-comment.md         # 市场评论框架
        ├── hotspot-interpretation.md # 热点解读框架
        ├── industry-analysis.md      # 行业分析框架
        └── invest-edu.md             # 投教营销框架

output/platforms/                    # 多平台输出
├── {date}_{title}/
│   ├── wechat.html                  # 微信HTML
│   ├── wechat.txt                   # 微信纯文本
│   ├── xhs.md                       # 小红书
│   ├── xhs-cards.html               # 小红书卡片HTML（可选）
│   ├── weibo.md                     # 微博
│   ├── zhihu.md                     # 知乎
│   ├── toutiao.md                   # 头条
│   └── video-script.md              # 短视频
└── analysis-report/                 # 拆解改写的分析报告
```

### 改造目录

| 原路径 | 改造后路径 | 说明 |
|--------|-----------|------|
| `references/seo-rules.md` | `skills/review/references/seo-rules.md` | 迁移 |
| `references/frameworks.md` | `skills/content-type-framework/frameworks/*.md` | 拆分为4类 |
| `references/wechat-constraints.md` | `skills/platform-adaptation/references/wechat-html.md` | 整合排版规范 |
| `scripts/extract_exemplar.py` | `scripts/extract_exemplar.py` | 改造为风格学习脚本 |
| `scripts/humanness_score.py` | `scripts/humanness_score.py` | 改造为审校脚本 |
| `scripts/fetch_article.py` | `scripts/fetch_article.py` | 改造为拆解改写素材抓取 |
| `scripts/learn_edits.py` | `scripts/learn_edits.py` | 改造为风格飞轮（支持多平台） |
| `toolkit/publisher.py` | — | **废弃**（取消直接发布） |
| `toolkit/converter.py` | `toolkit/converter.py` | 改造为多平台converter |
| — | `toolkit/xhs_converter.py` | 新增 |
| — | `toolkit/weibo_converter.py` | 新增 |
| — | `toolkit/zhihu_converter.py` | 新增 |
| — | `toolkit/toutiao_converter.py` | 新增 |
| — | `toolkit/video_converter.py` | 新增 |

### 保留目录

```
personas/           # 5套写作人格（扩充平台维度）
config.example.yaml # 配置模板（增加多平台API配置）
requirements.txt
evals/
```

---

## 四、关键文件引用关系

```
SKILL.md（主管道）
    │
    ├── Step 0（入口判断）
    │
    ├── 【全新创作分支】→ skills/content-type-framework/SKILL.md
    │                        └── frameworks/{market-comment|hotspot|industry|invest-edu}.md
    │
    ├── 【拆解改写分支】→ skills/rewrite/SKILL.md
    │                        ├── references/format-organize.md
    │                        ├── references/content-analyze.md
    │                        └── references/framework-map.md
    │
    ├── Step 1/1R → scripts/fetch_hotspots.py / scripts/fetch_article.py
    │
    ├── Step 2（素材采集，仅全新创作分支）→ scripts/fetch_hotspots.py
    │
    ├── Step 3 → personas/{persona}.yaml + skills/style-learning/references/style-extract.md
    │
    ├── Step 4（平台选择）→ config.yaml（预设三件套）
    │
    ├── Step 5 → skills/review/SKILL.md
    │              ├── references/seo-rules.md
    │              ├── references/quality-check.md
    │              └── references/compliance.md（待用户提供）
    │
    └── Step 6 → skills/platform-adaptation/SKILL.md
                   ├── references/wechat-html.md
                   ├── references/xhs-card.md
                   ├── references/weibo-short.md
                   ├── references/zhihu-long.md
                   ├── references/toutiao.md
                   └── references/video-script.md
```

---

## 五、平台输出规范

| 平台 | 格式 | 包含元素 |
|------|------|---------|
| 微信长文 | 内联样式HTML + 纯文本 | 标题、封面图提示、正文、脚注 |
| 小红书笔记 | Markdown + 配图提示词/卡片HTML | 标题（emoji+标签）、正文、3:4配图提示词 |
| 微博 | Markdown（140字内） | 话题标签、互动引导语 |
| 知乎长文 | Markdown | 结构化标题层级、论证式行文、参考文献脚注 |
| 今日头条 | Markdown | 短段落+关键词前置、情绪化标题 |
| 短视频脚本 | Markdown | 开场钩子（3秒）、分镜式正文、结尾引导 |

---

## 六、风格学习模块

### Onboarding 机制

```
首次触发 爆款智坊
    │
    ├── 检测是否有风格档案（style.yaml / references/exemplars/）
    │     ├── 有 → 正常进入 Step 0
    │     └── 无 → 强制进入【风格学习 Onboarding】
    │
    └── 用户随时可说「学习我的风格」/「重新学习」→ 触发风格学习流程
```

### Onboarding 流程（首次强制引导）

```
Step Onboard  风格档案初始化 ✋
    │
    ├── 询问用户提供3-5篇满意文章（粘贴/文件/URL）
    ├── 标注来源平台 + 作者名
    ├── 执行风格学习 Phase 1-5
    │
    └── 生成风格档案：
          ├── style.yaml（系统用）
          ├── references/exemplars/*.md（范文风格库）
          ├── style_manual.md（通用风格7章框架）
          └── platform_styles/（各平台差异化手册）
    
    ↓ 完成后进入主流程 Step 0
```

### 持续学习机制

```
用户编辑文章后说「学习我的修改」
    │
    ├── 对比初稿 vs 用户修改稿
    ├── 提取新增风格特征
    ├── 更新 style.yaml + exemplars/
    └── 提示：「已学习 X 处修改，风格档案已更新」

用户说「重新学习风格」
    │
    ├── 清空现有 exemplars/
    ├── 从头执行 Phase 1-5
    └── 提示：「已重新学习，最新风格档案已更新」
```

### 风格学习输出结构

```
风格档案/
├── style.yaml                    # 系统用风格参数
├── style_manual.md               # 通用风格（7章框架）
└── platform_styles/             # 各平台差异化风格手册
    ├── wechat_style.md          # 微信公众号
    ├── xhs_style.md             # 小红书
    ├── weibo_style.md           # 微博
    ├── zhihu_style.md           # 知乎
    ├── toutiao_style.md         # 今日头条
    └── video_style.md           # 短视频脚本

platform_styles 内容：
- 该平台的语气正式度（1-5分）
- 段落结构特征
- 数据呈现方式
- 风险提示格式
- 相对通用风格的调整点说明
```

### 风格学习用户确认界面

```
【风格学习完成】✋

📱 微信长文 — 语气3.5/5，长段落300字，精确数据，必含风险提示
📸 小红书 — 语气2/5，短段落80字，整数对比，口语+emoji
🐦 微博 — 语气1.5/5，单段落140字，一句话观点+话题标签
…（其他平台同理）

【确认】风格手册已定稿，开始写作
【重新学习】调整原始素材后重新分析
【分平台调整】单独修改某个平台的风格手册
```

### 风格学习流程

```
用户触发「学习我的风格」
    │
    ├── Step 1  素材录入
    │     ├── 粘贴文本 / 上传文件 / 指定URL抓取
    │     ├── 支持多篇（同一平台 or 跨平台）
    │     └── 标注来源平台
    │
    ├── Step 2  风格分析
    │     ├── 作者定位识别（身份标签/内容定位/读者画像）
    │     ├── 写作风格提取（语气/句式/情绪/转折/不确定性表达）
    │     ├── 固定文案识别（开场白/收尾/连接词）
    │     └── 平台差异分析（跨平台录入时触发）
    │
    └── Step 3  生成作者风格手册
          ├── System Prompt 注入（静默）
          ├── 通用风格手册（style_manual.md）
          ├── 各平台差异化手册（platform_styles/）
          └── 固定文案素材库
```

---

## 七、审校Severity分级

| 级别 | 名称 | 含义 | 处理方式 |
|------|------|------|---------|
| Error | 阻断 | 必须修改才能发布（提及个股、承诺收益） | 标红，用户确认修改 |
| Warning | 提醒 | 表述过于极端、确定性过高 | 标黄，给出建议，用户可选保留 |
| Info | 建议 | 信息密度可提升、开头可优化 | 标蓝，供参考，不阻断 |

---

## 八、合规审校规则（已补充）

来源：`references/compliance-source.md`（已内化）

### 审校输出格式

```
### 1. 合规摘要 (Compliance Summary)
- 交通信号灯形式：【🟢 低风险】、【🟡 中风险】、【🔴 高风险】
- 简述核心问题与优化原则（1-2句话）

### 2. 分项优化建议 (Itemized Optimization Suggestions)
每个风险点：
- **问题定位**：原文引用 + 引用法规/制度依据
- **修改建议**：词语替换/删除建议（参考福格行为模型，简化修改）
- **优化示例**：原句 → 修订后

### 3. 修订版全文 (Revised Note)
- 完整融合所有优化建议的版本
- 底部保留用户原有固定引导内容和合规提示，注明"（此部分为原文固定结尾，未作改动）"
```

### 禁止表达清单

**市场预测类（绝对禁止）**
- ❌ 必将大涨/大跌、确定上涨/下跌、一定涨/一定跌、必然会/必定会

**操作承诺类（绝对禁止）**
- ❌ 推荐买入/卖出、赶紧买/卖、满仓梭哈、抄底/逃顶

**绝对化词汇（谨慎使用）**
- ❌ 暴涨/暴跌、极好/极差、完全/彻底、只能/必须（操作建议中）

### 概率性表达（推荐使用）

- ✅ 大概率、或、可能、倾向于、值得关注
- ✅ 建议关注、可以考虑、逢低布局、控制仓位、分散风险

### 风险提示格式（每篇必含）

```
本内容仅供参考，不构成投资建议。投资者据此操作，风险自担。
市场有风险，投资需谨慎。
```

### 数据来源标注

- ✅ 指数行情："根据官方行情数据显示"
- ✅ 资金流向："根据官方行情数据显示"
- ✅ 政策文件："根据证监会XX文件"
- ✅ 新闻报道："根据XX媒体报道"
- ❌ 模糊来源："据悉"、"有消息称"（必须核实）

### 合规检查清单

- [ ] 无绝对化市场预测词汇
- [ ] 无操作承诺性语句
- [ ] 有风险提示
- [ ] 关键数据有来源标注
- [ ] 使用概率性表达（大概率/或/可能）

---

## 九、风格学习框架（已补充）

来源：
- `创作风格提取提示词v3.1.txt` — 《风格创作手册》生成器
- `tougu-writer-factory` — 8维深度提取 + 自测评循环
- `xhs-writer-factory` — 品牌信息最高优先级 + 4步工厂流程

### 风格学习输出：《作者风格创作手册》框架

```markdown
# 《[作者姓名]风格创作手册》

## 一、风格核心定位
- **风格一句话定义**：[例如：一种以"学者侦探"视角展开的、冷峻精密又不失人文体温的叙事-论述混合体。]
- **精神内核**：贯穿所有作品的恒定价值观与认知姿态。
- **拟达到的读者感知**：希望读者产生何种整体印象与情感认知。

## 二、语气与语态规范
- **主导语气**：冷静的观察者 / 平等的交流者 / 权威的解读者
- **语态参数**：正式度 / 抽象度 / 情感浓度（各1-5分）
- **语气禁区**：严禁出现的语态（如：浮夸的惊叹、武断的结论）

## 三、文章结构蓝图
- **通用结构模板**：开场白类型 → 主体展开逻辑 → 过渡标志 → 收尾方式
- **节奏控制**：段落平均长度、信息密度曲线、张弛安排
- **结构禁忌**：避免使用的结构（如：平铺直叙的编年史）

## 四、句式与词汇偏好
- **标志性句式**：高频且具辨识度的句型（≥3个）
- **词汇光谱**：高频抽象词 / 高频具象词 / 特征修饰词 / 禁用词汇表

## 五、标志性修辞与手法
- **比喻系统**：擅长用【XX领域】的意象比喻【YY概念】
- **对比策略**：惯于在【时间纵轴】与【系统横轴】上建立对比
- **论证手法**：常用【归谬法】或【追溯前提】来解构流行观点

## 六、写作反模式（常见误区）
| 误区 | 错误示例 | 正确示例 | 核心原因 |
| :--- | :--- | :--- | :--- |

## 七、修改与核查清单
- 【宏观层】思维与结构核查
- 【中观层】段落与节奏核查
- 【微观层】语句与用词核查
```

### 风格学习工作流

```
Phase 1: 文章采集存档（需用户确认样本）
    ↓
Phase 2: 多维度深度提取
    ├── 8维提取（投顾场景）：标题/段落/句式/词汇/分析逻辑/数据规范/固定表达/数据需求
    └── 11维提取（小红书场景）：+ 段落强制开头语/比喻体系/图片偏好/封面尾页结构
    ↓
Phase 3: 一致率分析 → 风格画像
    ├── ≥80% → 核心模式
    ├── 50-79% → 标准模式
    └── <50% → 可选变体
    ↓
Phase 4: Skill组装（固化模块 + 个性化提取 + 自测评）
    ↓
Phase 5: 自测评循环（≥80%通过，最多3轮）
```

### 投顾场景固化模块（直接复制，无需提取）

- `固化模块/compliance.md` — 合规红线
- `固化模块/market_data.py` — 市场数据获取脚本

---

## 十、待补充事项

- [x] **合规审校规则** ✅ — 已补充至 Section 八
- [x] **风格学习提示词框架** ✅ — 已补充至 Section 九
- [ ] **财经内容类型框架细化**：4类内容类型框架模板需进一步填充
- [ ] **各平台具体改写提示词**：微信HTML/小红书/微博/知乎/头条/短视频的具体改写规范

---

## 十一、改造优先级

**Phase 1（基础架构）**
1. 主SKILL.md重构（Step 0 入口判断 + 平台选择）
2. `skills/content-type-framework/` 内容类型路由
3. `skills/rewrite/` 拆解改写流程
4. `skills/platform-adaptation/` 多平台改写框架

**Phase 2（质量保障）**
5. `skills/review/` 审校流程（含合规规则）
6. `scripts/humanness_score.py` 改造

**Phase 3（风格增强）**
7. `skills/style-learning/` 风格学习流程
8. `scripts/extract_exemplar.py` 改造
9. `personas/` 扩充平台维度

**Phase 4（工具链）**
10. `toolkit/` 新增各平台converter
11. `toolkit/publisher.py` 废弃
12. 输出目录结构重建
