import scrapy
# from manhuaSpider.spidersDmozSpider import 
# from manhuaSpider.items import ImagespiderItem
class newupdate(scrapy.Spider):
    name = "newupdate"
    baseurl = "http://m.qiman6.com"
    start_urls = [
        "http://m.qiman6.com/12896/",   
    ]
    def parse(self, response):
        urls = response.xpath('//div[@class="catalog-list"]/ul/li').re(r"href=\".*?\"")
        for i in range(len(urls)):
            urls[i] = urls[i][ 6: -1]
        names = response.xpath('//div[@class="catalog-list"]/ul/li/a').re(r">.*?<")
        for i in range(len(names)):
             names[i] = names[i][ 1: -1]
        pass
    

