# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request


class ManhuaspiderPipeline:
    def process_item(self, item, spider):
        return item

class downloadImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
            yield Request(item['imgurl'], meta={'name':item['imgname'], 'chaptername':item['chaptername']})

    def file_path(self, request, response=None, info=None):
        # 提取url前面名称作为图片名。
        filename = request.meta['name']+".jpg"
        filename = u'{0}/{1}'.format(request.meta['chaptername'], filename)
        # 分文件夹存储的关键：{0}对应着name；{1}对应着image_guid
        return filename
