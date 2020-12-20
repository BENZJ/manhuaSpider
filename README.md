# 奇漫屋爬虫
## run
```
cd manhuaSpider
scrapy crawl dmoz
```
## docker方式运行
挂载上去两个目录一个是爬取的image存储文件夹，一个是pdf生成的存放文件夹
```shell
nohup docker build -t scrapy-ubuntu  . 2>&1
docker run -it  -v /root/images:/manhuaSpider/manhuaSpider/images\
                -v /root/out:/manhuaSpider/out  \
                scrapy-ubuntu /bin/bash
```