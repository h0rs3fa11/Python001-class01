import scrapy
from smzdm.items import SmzdmItem, SmzdmGoodItem


class SmzdmCommentSpider(scrapy.Spider):
    name = 'smzdm_comment'
    allowed_domains = ['smzdm.com']
    start_urls = ['https://www.smzdm.com/fenlei/zhinengshouji/h5c4s0f0t0p1/#feed-main/']

    def parse_comments(self, response, gid):
        # 解析每个条目的评论，清洗，返回item
        for comment_id in response.xpath('//*[@id="commentTabBlockNew"]/ul[1]/li/@id').getall():
            items = SmzdmItem()
            comment = response.xpath(
                f'//*[@id="{comment_id}"]/div[@class="comment_conBox"]/div[@class="comment_conWrap"]/div[@class="comment_con"]/p/span/text()').extract_first().strip()
            comment = "".join(comment)
            good_name = response.xpath('//*[@id="feed-main"]/div[@class="info J_info"]/div/div[@class="title-box"]/h1/text()').extract_first().strip()
            items['comment_id'] = comment_id
            items['comment_text'] = comment
            items['goods_id'] = gid
            items['good_name'] = good_name
            yield items
        next_page = response.xpath(
            '//*[@id="commentTabBlockNew"]/ul[@class="pagination"]/li[@class="pagedown"]/a/@href').get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse_comments, cb_kwargs=dict(gid=gid))

    def parse(self, response):
        items = SmzdmGoodItem()
        items['goods_id'] = []
        good_url = []
        for selector in response.xpath('//*[@id="feed-main-list"]/li')[:10]:
            url = selector.xpath(
                './div/div[@class="z-feed-content "]/div[@class="z-feed-foot"]/div[@class="z-feed-foot-l"]/a[@class="z-group-data"]/@href').extract_first()
            good_id = selector.xpath('@articleid').get()[2:]
            items['goods_id'].append(good_id)
            good_url.append((url, good_id))
            yield scrapy.Request(url=url, callback=self.parse_comments, cb_kwargs=dict(gid=good_id))
        yield items

