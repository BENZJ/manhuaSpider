# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
from manhuaSpider.items import bookChapterItem
from manhuaSpider.items import ImagespiderItem
import pymysql



class ManhuaspiderPipeline:
    def __init__(self):
        self.connect = pymysql.connect(
            host='49.235.207.129',
            port=3309,
            db='MAN_HUA',
            user='root',
            password='jbcbenz',
            charset='utf8',
        )
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()
        pass
    def process_item(self, item, spider):
        if isinstance(item, bookChapterItem):
            sql='INSERT INTO Book_Chapter(bookid, url, chaptername)  VALUES(%s,%s,%s) '
            try:
                self.cursor.execute(sql,(item['bookid'],item['url'],item['chaptername']))
                self.connect.commit()
            except :
                print("已经添加过，无需添加数据库")
            return item
        else:
            return item
    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()

class downloadImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
            if isinstance(item, ImagespiderItem):
                yield Request(item['imgurl'], meta={'name':item['imgname'], 'chaptername':item['chaptername']})
            else:
                return item

    def file_path(self, request, response=None, info=None):
        # 提取url前面名称作为图片名。
        filename = request.meta['name']+".jpg"
        filename = u'{0}/{1}'.format(request.meta['chaptername'], filename)
        # 分文件夹存储的关键：{0}对应着name；{1}对应着image_guid
        return filename
