from scrapy.cmdline import execute
import sys
import os

sys.path.append("/Users/benz/Desktop/漫画爬虫/manhuaSpider")
execute(['scrapy','crawl','dmoz'])