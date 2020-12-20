import scrapy
import re
from manhuaSpider.items import bookChapterItem
from scrapy import FormRequest
import json
from scrapy import Request

rooturl = "http://m.qiman6.com"
class bookindexSpider(scrapy.Spider):
    name = "bookindex"
    def __init__(self, bookid= 14289 ,*args, **kwargs):
        super(bookindexSpider, self).__init__(*args, **kwargs)
        self.__dict__.update(kwargs)
        self.bookid = bookid
    pass

    def start_requests(self):
        url = "http://m.qiman6.com/bookchapter/"
        yield FormRequest(url, formdata={"id": str(self.bookid), "id2":"1"})
    def parse(self, response):
        response = json.loads(response.text)
        yield Request(rooturl+"/"+str(self.bookid)+"/", callback=self.parseindex,meta={'startindex':len(response)})
        pass
    
    def parseindex(self, response):
        ## 首页最新章节显示的数量
        urls = response.xpath('//div[@class="catalog-list"]/ul/li/a/@href').extract()
        varlen = len(urls)

        startindex = int(response.meta['startindex'])
        startindex += varlen
        bookname = response.xpath('//div[@class="box-back2"]/h1/text()').extract()
        names = response.xpath('//div[@class="catalog-list"]/ul/li/a/text()').extract()
        for i in range(len(urls)):
            item = bookChapterItem()
            item["bookid"] =self.bookid 
            item["url"] = urls[i]
            item["chaptername"] = (bookname[0]+"/"+("%05d" % (startindex))+"_"+names[i])
            startindex-=1
            yield item