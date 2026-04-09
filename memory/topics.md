# 选题库

> 管理选题信息，按赛道分类，含爆款潜力评分和历史去重。

## 格式

```csv
id,topic,category,score_hot,score_seo,score_unique,status,date_added,date_used,article_title,notes
```

| 字段 | 说明 |
|------|------|
| id | 选题编号 TPC-XXX |
| topic | 选题描述 |
| category | 赛道分类（投资/科技/职场/生活等） |
| score_hot | 热点潜力评分 0-10 |
| score_seo | SEO友好度 0-10 |
| score_unique | 角度独特性 0-10 |
| status | pending / used / discarded |
| date_added | 入库日期 |
| date_used | 使用日期 |
| article_title | 最终文章标题（used时填写） |
| notes | 备注 |

## 选题记录

<!-- ### 投资理财
| ID | 选题 | 热点 | SEO | 独特 | 状态 | 入库日 | 使用日 |
|----|------|------|-----|------|------|--------|--------|
（待积累）

### 科技趋势
（待积累）

### 职场成长
（待积累）

### 方法工具
（待积累）

### 生活感悟
（待积累） -->

## 去重规则
- 已标记 `used` 的选题不再推荐
- 同一角度的不同表述视为重复
- 超3个月未写的 `pending` 选题重新评估热度
- 已弃选题超3个月删除

## 容量上限：500条
