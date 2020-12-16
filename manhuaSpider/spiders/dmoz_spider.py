import scrapy
import re
from manhuaSpider.items import ImagespiderItem
from scrapy import FormRequest
import json
from scrapy import Request

imagepath="https://p.pstatp.com/origin/"
chapterpath="http://m.qiman6.com/12896/"
class DmozSpider(scrapy.Spider):
    name = "dmoz"
    # start_urls = [
    #     # "http://m.qiman6.com/12896/1051883.html",
    #     "http://m.qiman6.com/12896/1051945.html",
    #     #"http://m.qiman6.com/bookchapter/"      
    # ]
    def start_requests(self):
        url = "http://m.qiman6.com/bookchapter/"
        yield FormRequest(url, formdata={"id": "12896", "id2":"1"})
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
        if vals[lenval-1] == "":
            vals = vals[0:-1]
            lenval -=1
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
        
            