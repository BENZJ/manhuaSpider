import scrapy
import re
from manhuaSpider.items import ImagespiderItem


class chapterSpider(scrapy.Spider):
    name = "chapterSpider"
    def __init__(self, start_urls= None, chaptername = None ,*args, **kwargs):
        super(chapterSpider, self).__init__(*args, **kwargs)
        self.__dict__.update(kwargs)
        self.chaptername = chaptername
        self.start_urls = [start_urls]
    
    def parse(self, response):
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
            item['chaptername'] = self.chaptername

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
    