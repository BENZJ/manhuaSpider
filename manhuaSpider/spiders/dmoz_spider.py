import scrapy
import re
from manhuaSpider.items import ImagespiderItem
from scrapy import FormRequest
import json
from scrapy import Request
baseurl = "http://m.qiman6.com"
"""
狐妖小红娘           12896
大神仙              14289
长歌行              14391
女子学院的男生       12645
校园默示录           2025
"""


class DmozSpider(scrapy.Spider):
    def __init__(self, mahuacode=14289, *args, **kwargs):
        super(DmozSpider, self).__init__(*args, **kwargs)
        self.mahuacode = mahuacode
        self.chapterpath= baseurl+"/"+self.mahuacode+"/"
        self.__dict__.update(kwargs)
    name = "dmoz"
    # start_urls = [
    #     # "http://m.qiman6.com/12896/1051883.html",
    #     # "http://m.qiman6.com/12896/1051945.html",
    #     #"http://m.qiman6.com/bookchapter/"
    #     # "http://m.qiman6.com/12896/1051946.html"     
    # ]
    def start_requests(self):
        url = "http://m.qiman6.com/bookchapter/"
        yield FormRequest(url, formdata={"id": self.mahuacode, "id2":"1"})

    def parseindex(self, response):
        urls = response.xpath('//div[@class="catalog-list"]/ul/li').re(r"href=\".*?\"")
        varlen = len(urls)
        startindex = int(response.meta['startindex'])
        startindex += varlen
        for i in range(len(urls)):
            urls[i] = urls[i][ 6: -1]
        names = response.xpath('//div[@class="catalog-list"]/ul/li/a').re(r">.*?<")
        for i in range(len(names)):
             names[i] = names[i][ 1: -1]
        
        for i in range(len(urls)):
            yield Request (baseurl+urls[i], callback=self.parsechapter , meta={'chaptername': ("%05d" % (startindex))+"_"+names[i]})
            startindex-=1


    def parse(self, response):
        response = json.loads(response.text)
        k = 0
        yield Request(self.chapterpath, callback=self.parseindex,meta={'startindex':len(response)})
        for index in response:
            k+=1
            newurl = self.chapterpath+index["id"]+".html"
            yield Request(url=newurl, callback=self.parsechapter,  meta={'chaptername': ("%05d" % (len(response)-k+1))+"_"+index["name"]},)
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
                    if(vals[self.charToNum(i)]!=""):
                        relurl = relurl+vals[self.charToNum(i)]
                    else:
                        relurl = relurl+i
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
        
            