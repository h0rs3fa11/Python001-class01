import scrapy


class SmzdmCommentSpider(scrapy.Spider):
    name = 'smzdm_comment'
    allowed_domains = ['smzdm.com']
    start_urls = ['http://smzdm.com/']

    def parse(self, response):
        pass
