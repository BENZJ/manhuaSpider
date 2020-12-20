# 奇漫屋爬虫
## run
```
cd manhuaSpider
scrapy crawl dmoz
```
## docker方式运行
挂载上去两个目录一个是爬取的image存储文件夹，一个是pdf生成的存放文件夹
```shell
nohup docker build -t benzj/manhuaspider  . 2>&1
docker run -it  -v /root/images:/manhuaSpider/manhuaSpider/images\
                -v /root/out:/manhuaSpider/out  \
                benzj/manhuaspider /bin/bash
cd manhuaSpider
python3 createSplit.py
```
## 常见问题
### pymysql.err.DataError: (1366, 
修改数据库表编码
```sql
alter table <表名>  convert to  character set utf8mb4;
```