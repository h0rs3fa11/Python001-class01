# 舆情分析平台

数据来源：什么值得买-手机

## 模块设计

### 爬虫模块

使用scrapy爬虫框架，实现爬取“什么值得买”手机类别的24小时排行前十的商品评论，保存到数据库

### 数据清洗

对原始评论内容进行情感语义分析，并保存分析结果

### 前端展示

使用django web框架+bootstrap框架以图表方式展示分析结果 ，并支持按时间、关键词筛选



## 模块详细实现

### 数据结构设计

爬虫模块从“什么值得买”爬取到的还未存入数据库的数据格式为：

```json
{
  "goods_list":{
    "good1_id":["comment1_id", "comment2_id"],
    "good2_id":["comment3_id", "comment4_id"]
  },
  "comment_list":{
    "comment1_id":"content",
    "comment2_id":"content",
    //...
  }
}
```

商品id`good_id`与评论id是一对多的关系，在（原始）数据库中设计为一个goods table、一个comment table，comment table中添加外键`good_id`关联两个表。

原始数据库中数据的更改：每日爬虫定时运行，网站更新后有新的商品加入前十，同时会有已存在商品从前十中删除

```sql
mysql> SHOW FULL COLUMNS FROM goods;
```

| Field   | Type    | Collation          | Null | Key  | Default | Extra | Privileges                      |
| ------- | ------- | ------------------ | ---- | ---- | ------- | ----- | ------------------------------- |
| good_id | char(8) | utf8mb4_0900_ai_ci | NO   | PRI  | NULL    |       | select,insert,update,references |

```sql
mysql> SHOW FULL COLUMNS FROM origin_comments;
```
| Field   | Type          | Collation          | Null | Key  | Default | Extra | Privileges                      |
| ------- | ------------- | ------------------ | ---- | ---- | ------- | ----- | ------------------------------- |
| comm_id | char(20)      | utf8mb4_0900_ai_ci | NO   | PRI  | NULL    |       | select,insert,update,references |
| content | varchar(1000) | utf8mb4_0900_ai_ci | YES  |      | NULL    |       | select,insert,update,references |
| good_id | char(8)       | utf8mb4_0900_ai_ci | NO   | MUL  | NULL    |       | select,insert,update,references |

另外还有一个语义分析后的表`analysis_comments`，外键也是`goods`表中的`good_id`
| Field      | Type          | Collation          | Null | Key  | Default | Extra | Privileges                      |
| ---------- | ------------- | ------------------ | ---- | ---- | ------- | ----- | ------------------------------- |
| comm_id    | char(20)      | utf8mb4_0900_ai_ci | NO   | PRI  | NULL    |       | select,insert,update,references |
| content    | varchar(1000) | utf8mb4_0900_ai_ci | YES  |      | NULL    |       | select,insert,update,references |
| sentiments | float         | NULL               | YES  | MUL  | NULL    |       | select,insert,update,references |
| good_id    | char(8)       | utf8mb4_0900_ai_ci | NO   | MUL  | NULL    |       | select,insert,update,references |


### 爬虫模块实现

#### `items`数据结构

定义了两个`items`类，`SmzdmItem`是爬取到的评论内容及对应评论id、商品id，`SmzdmGoodItem`是当前前十的商品id



#### `spiders`模块

主要功能：

`parse(response)`

解析请求https://www.smzdm.com/fenlei/zhinengshouji/h5c4s0f0t0p1/#feed-main/页面的响应，得到商品的评论url通过`scrapy.Request`调用并用函数`parse_comment(response, gid)`解析，并将前十的商品id返回给`pipeline`



`parse_comment(response, gid)`

提取具体商品页的评论内容，设置对应items字段返回给`pipeline`，并解析该页面评论是否还可以翻页，有就继续调用`scrapy.Request`解析新的页面



#### `pipeline`模块

- 判断接收到的item类型，如果是`SmzdmGoodItem`就保存为`self.new_goods`就结束
- 接收到的是爬取到的评论内容，解析数据并保存到原始数据库
- 评论语义情感分析，分析后的结果保存到另一个数据库



#### Pycharm调试scrapy

新建`run.py`

```python
import os
import sys
from scrapy.cmdline import execute

base_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(base_dir)
os.chdir(base_dir)
execute(['scrapy', 'runspider', 'smzdm/spiders/smzdm_comment.py'])
```

在Pycharm中配置`Run-Edit Configurations`， `+` 添加新配置，并在`script path`中选择`run.py`