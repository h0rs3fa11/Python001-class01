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
| good_name | varchar(50) | utf8mb4_0900_ai_ci | NO   |   | NULL    |       | select,insert,update,references |

```sql
mysql> SHOW FULL COLUMNS FROM origin_comments;
```
| Field   | Type          | Collation          | Null | Key  | Default | Extra | Privileges                      |
| ------- | ------------- | ------------------ | ---- | ---- | ------- | ----- | ------------------------------- |
| comm_id | char(20)      | utf8mb4_0900_ai_ci | NO   | PRI  | NULL    |       | select,insert,update,references |
| content | varchar(1000) | utf8mb4_0900_ai_ci | YES  |      | NULL    |       | select,insert,update,references |
| good_id | char(8)       | utf8mb4_0900_ai_ci | NO   | MUL  | NULL    |       | select,insert,update,references |
| time    | datatime      | NULL               | YES  |      | NULL    |       | select,insert,update,references |

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

### Web模块

django框架结合bootstrap进行数据展示

主要分为两个页面，主页和具体商品信息页与搜索结果页，在app下面的urls.py中配置，对应不同的views

配置好mysql连接并用manager.py的inspectdb命令导出数据库的models

#### 数据展示

主页中要展示的信息是商品总数、评论总数，以及商品列表，不需要对models的数据进行筛选，主要代码如下

```python
# 商品id
goods = Goods.objects.all()
# 商品名称
good_name = Goods.objects.values('good_name')
# 商品总数
goods_count = Goods.objects.all().count()
# 评论总数
comment_count = OriginComments.objects.all().count()
return render(request, 'index.html', locals())
```

商品名称`good_name`在html中用for循环逐条展示

实现了从商品名称直接点击进入对应商品详情页的功能

```html
{% for g in goods %}
<tr>
<td>
<a href="{% url 'smzdm:good_info' g.good_id %}">{{g.good_name}}</a>
</td>
</tr>
{% endfor %}
```

超链接调用views的`good_info`，传入参数商品id



接下来是商品详情页

商品详情页做了一些筛选

```python
# 筛选当前商品对应的评论
queryset = AnalysisComments.objects.values('content')
conditions = {'good_id__exact': id}
comments_count = queryset.filter(**conditions).count()
#获取当前商品对应的商品名
good_name = Goods.objects.values('good_name').filter(**conditions)[0]['good_name']
#筛选情感倾向，并计算平均值
queryset = AnalysisComments.objects.values('sentiments')
sent_avg = f"{queryset.filter(**conditions).aggregate(Avg('sentiments'))['sentiments__avg']:0.2}"
#筛选负向评论
queryset = AnalysisComments.objects.values('sentiments')
sent_cond = {'sentiments__lt': 0.5}
minus = queryset.filter(**conditions).filter(**sent_cond).count()
#筛选正向评论
sent_cond = {'sentiments__gte': 0.5}
plus = queryset.filter(**conditions).filter(**sent_cond).count()
#获取当前商品对应的所有评论
queryset = AnalysisComments.objects.all()
analysis_comment = queryset.filter(**conditions)
```



#### 搜索

将侧边栏`base_layout.html`中的搜索表单改为

```html
<form role="search" method="get" action="/search/">
      {% csrf_token %}
			<input type="search" name="q" placeholder="Search" required>
            <button class="btn btn-default" type="submit">
                 <i class="fa fa-search"></i>
            </button>
</form>
```

urlconf中添加筛选的url

```python
re_path('search\/.*', views.search, name='search')
```

在view中定义search函数

```python
def search(request):
    query = request.GET.get('q')
    try:
        search_date = datetime.strptime(query, "%Y-%m-%d")
        query_date = search_date.strftime("%Y-%m-%d")
        goods_result = None
        comment_result = OriginComments.objects.filter(time__gte=query_date)
    except ValueError:
        goods_result = Goods.objects.filter(good_name__icontains=query)
        comment_result = OriginComments.objects.filter(content__icontains=query)
    return render(request, 'comment_search_result.html',
                  {'error_msg': 0, 'result': {"goods": goods_result, "comments": comment_result}})
```

并在结果页展示

#### 爬虫定时任务

使用scrapyd部署scrapy项目，然后将scrapyd命令添加到django定时任务中

