# 学习人工修改（核心飞轮）

这是 爆款智坊 最重要的长期价值。每次用户编辑文章后让系统学习，下一版的初稿就会更接近用户的风格，需要的编辑量越来越少。

**飞轮效应**：初稿需要改 30% → 学习 5 次后只需改 15% → 学习 20 次后只需改 5%

**触发**：用户说"我改了，学习一下"、"学习我的修改"

## 1. 获取 draft 和 final

- **draft**：`workspace/drafts/` 下最新草稿目录中的 draft.md
- **final**：用户提供修改后的版本。主动引用："请把你改好的文章全文粘贴给我，或者告诉我文件路径。"

## 2. LLM diff 分析

将 draft 和 final 全文交给 LLM，逐句对比分析，识别修改模式。

## 3. 分析并记 pattern

**每个 pattern 必须包含**：
- `type`：`word_sub` / `para_delete` / `para_add` / `structure` / `title` / `tone` / `expression`
- `key`：短唯一标识（英文，如 `avoid_jiangzhen`、`shorter_paragraphs`、`more_negative_emotion`）
- `description`：这次修改是什么（如"把'讲真'替换为'坦白说'"）
- `rule`：可执行的写作指令（**必须是祈使句，不是描述句**）

**key 的复用**：如果这次的修改和之前学习过的 pattern 是同一种偏好，使用**相同的 key**，confidence 自动累加提升。

## 4. 写入 memory/feedback.md

将本次分析出的 pattern 追加写入 `memory/feedback.md`，标注：
- key、type、rule、confidence、last_seen

**confidence 规则**：
- 首次出现：confidence = 3.0
- 相同 key 再次出现：confidence += 1.0（上限 10.0）
- 长期未出现（超过 10 次学习）：confidence -= 0.5（下限 2.0，低于 2.0 删除）

## 5. Step 3 如何使用 feedback.md

每次初稿写作前读取 `memory/feedback.md`：
- **confidence ≥ 7 的规则**：作为硬性约束执行
- **confidence 4-6 的规则**：作为软性参考
- **confidence < 4 的规则**：忽略（可能已过时）

这确保：
- 用户反复确认的偏好（高 confidence）被严格执行
- 只出现过一次的偏好（低 confidence）不过度影响
- 用户风格变化时，旧规则自然衰减退出
