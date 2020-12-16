import scrapy
import re
from manhuaSpider.items import ImagespiderItem
from scrapy import FormRequest
import json
from scrapy import Request
baseurl = "http://m.qiman6.com"
"""
狐妖小红娘 12896
大神仙    14289
"""
mahuacode = "14289" 
chapterpath= baseurl+"/"+mahuacode+"/"
class DmozSpider(scrapy.Spider):
    name = "dmoz"
    # start_urls = [
    #     # "http://m.qiman6.com/12896/1051883.html",
    #     # "http://m.qiman6.com/12896/1051945.html",
    #     #"http://m.qiman6.com/bookchapter/"
    #     # "http://m.qiman6.com/12896/1051946.html"     
    # ]
    def start_requests(self):
        yield Request(chapterpath, callback=self.parseindex)
        url = "http://m.qiman6.com/bookchapter/"
        yield FormRequest(url, formdata={"id": mahuacode, "id2":"1"})

    def parseindex(self, response):
        urls = response.xpath('//div[@class="catalog-list"]/ul/li').re(r"href=\".*?\"")
        for i in range(len(urls)):
            urls[i] = urls[i][ 6: -1]
        names = response.xpath('//div[@class="catalog-list"]/ul/li/a').re(r">.*?<")
        for i in range(len(names)):
             names[i] = names[i][ 1: -1]
        for i in range(len(urls)):
            yield Request (baseurl+urls[i], callback=self.parsechapter , meta={'chaptername': names[i]})

    def parse(self, response):
        print(response)
        response = json.loads(response.text)
        for index in response:
            newurl = chapterpath+index["id"]+".html"
            yield Request(url=newurl, callback=self.parsechapter,  meta={'chaptername': index["name"]},)
        pass

    # 获取并解析漫画网页顺序
    # def parsechapter(self, response):
    def parsechapter(self, response):
        urls = ''
        vals = []
        for sel in response.xpath('//script').re(r'\[.*?\]'):
            if len(sel)>30 :
                urls = sel
        for sel in response.xpath('//script').re(r',\'.*?\''):
            if len(sel)>30:
                vals = sel.split("|")
        lenval = len(vals)
        vals[0] = vals[0][2:]
        vals[lenval-1] = vals[lenval-1][:-2]
        if lenval>=26 :
            vals[25]="p"
        pattern = re.compile(r"\".*?\"")
        urls = pattern.findall(urls)
        for i in range(len(urls)):
            urls[i] = urls[i][1:-1]
        pass
        relurs =[]
        index = 1
        for url in urls:
            relurl = ""
            for i in url:
                if(not self.needchange(i)):
                    relurl = relurl+i
                elif (self.charToNum(i)<lenval):
                    relurl = relurl+vals[self.charToNum(i)]
                else:
                    relurl = relurl+i
            item = ImagespiderItem()
            item['imgurl'] = relurl
            item['imgname'] = "%05d" % index
            item['chaptername'] = response.meta['chaptername']
            index+=1
            yield item
            
        pass

        
        
    def needchange(self, input):
        if(input<='9' and input >="0"):
            return True
        elif (input<='z' and input >="a"):
             return True
        else:
            return False
    def charToNum(self, input):
        if(input<='9' and input >="0"):
            return ord(input)-ord('0')
        else:
            return ord(input)-ord('a')+10
        
            