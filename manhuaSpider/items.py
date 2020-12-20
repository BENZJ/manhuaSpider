# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ManhuaspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# 继承scrapy.item类
class ImagespiderItem(scrapy.Item):
    # Field类仅是内置字典类（dict）的一个别名，并没有提供额外的方法和属性。
    # 被用来基于类属性的方法来支持item生命语法。
    imgurl = scrapy.Field()
    imgname = scrapy.Field()
    chaptername = scrapy.Field()
    # zhangjie = scrapy.Field()
    pass

# 用来存储数据库判断这本书这一章节是否爬过
class bookChapterItem(scrapy.Item):
    bookid = scrapy.Field()
    url = scrapy.Field()
    chaptername = scrapy.Field()
    pass