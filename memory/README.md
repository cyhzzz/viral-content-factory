# 上下文记忆库

本文件夹保存优质上下文记忆，帮助 AI 在后续创作中复用高质量素材、观点和经验。每次创作完成后自动沉淀，越用越聪明。

## 文件夹结构

```
memory/
├── README.md              # 本说明文件
├── golden-sentences.md    # 金句库：优质金句（含风格标签和句式模式）
├── viewpoints.md          # 观点与立场库：核心观点、价值判断、立场倾向
├── titles.md              # 标题自学习库：标题效果档案、高效模式、偏好画像
├── topics.md              # 选题库：按赛道分类，含爆款潜力评分
├── performance.md         # 数据复盘：文章发布效果追踪、高效写作模式
├── benchmarks.md          # 对标账号：竞品档案、爆款规律、差异化分析
├── calendar.md            # 内容日历：发布排期、节假日规划、内容搭配
├── feedback.md            # 反馈记录：用户修改意见和风格偏好
├── materials.md           # 素材库：案例、数据、故事等可复用素材
└── audience.md            # 读者画像：目标读者特征和偏好
```

## 使用规范

### 写入规则
1. 每次完成一篇文章后，自动提取以下内容写入：
   - 产生的优质金句 → `golden-sentences.md`
   - 标题选择和效果 → `titles.md`
   - 选题信息和效果 → `topics.md`
   - 用户修改反馈 → `feedback.md`
   - 使用的案例素材 → `materials.md`

2. 用户提供文章时，自动提取：
   - 核心观点和立场 → `viewpoints.md`
   - 文章中的金句 → 自创金句存 `golden-sentences.md`，外部金句存 `materials.md`
   - 用户风格特征 → `feedback.md`

3. 发布后效果数据写入：
   - 文章效果数据 → `performance.md`
   - 对标账号分析 → `benchmarks.md`
   - 排期更新 → `calendar.md`

### 读取规则（每次创作前扫描）
1. feedback.md（用户偏好最优先）
2. viewpoints.md（用户立场和观点）
3. performance.md（效果数据指导策略）
4. titles.md（标题偏好和高效模式）
5. topics.md（选题库，避免重复选题）
6. calendar.md（排期确认当前任务）
7. benchmarks.md（对标情报）
8. audience.md（读者画像）
9. golden-sentences.md（金句复用）
10. materials.md（素材复用）

### 容量限制与清理
| 文件 | 上限 | 淘汰规则 |
|------|------|---------|
| golden-sentences.md | 100 条 | 删除使用次数最少、超过6个月未使用的 |
| viewpoints.md | 150 条 | 不确定立场超3个月未确认的移入待确认区 |
| topics.md | 500 条 | 已弃选题超3个月删除，已写保留 |
| performance.md | 不限 | 保留全部 |
| benchmarks.md | 20 个账号 | 超6个月未更新标记为不活跃 |
| calendar.md | 最近3个月 | 超过3个月的归档到历史排期 |
| materials.md | 200 条 | 超6个月未使用的移到冷素材区 |
| feedback.md | 不限 | 保留全部 |

## 与现有系统的关系

本记忆库是对 viral-content-factory 原有系统的**增强和扩展**，不是替代：
- `style.yaml` / `playbook.md` → 仍然负责**写作风格**和**编辑飞轮**
- `memory/` → 新增**内容资产**管理（金句/标题/素材/观点/选题等）
- 两者互补：style 管理怎么写，memory 管写什么、写过什么、效果如何
