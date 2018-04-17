import scrapy
from zhihu.items import zhihuItem

class zhihuService(scrapy.Spider):
    name = 'zhihu'

    allowed_domains = ["www.zhihu.com"]

    offset = 0

    url = 'https://www.zhihu.com/node/ExploreAnswerListV2?params={"offset":%s,"type":"day"}'

    start_urls = [url  % (offset)]

    def parse(self, response):
        for each in response.xpath("//div[@class='explore-feed feed-item']"):
            # 初始化模型对象
            item = zhihuItem()
            # 标题
            item['title'] = each.xpath("./h2/a/text()").extract()[0]
            # 回答人
            # item['answer_people'] = each.xpath("./td[1]/a/@href").extract()[0]
            # # 回答
            # item['answer'] = each.xpath("./td[2]/text()").extract()[0]

            yield item

        if self.offset < 20:
            self.offset += 5

        # 每次处理完一页的数据之后，重新发送下一页页面请求
        # self.offset自增10，同时拼接为新的url，并调用回调函数self.parse处理Response
        yield scrapy.Request(self.url % (self.offset), callback=self.parse)