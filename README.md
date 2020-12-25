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
                -v /root/out:/manhuaSpider/manhuaSpider/out  \
                --name=manhuaspider \
                benzj/manhuaspider /bin/bash


docker run -d -p 0.0.0.0:3309:3306 --name mysql01 \
            -e MYSQL_ROOT_PASSWORD="jbcbenz"  \
            -e MYSQL_USER="benz" \
            -e MYSQL_PASSWORD="jbcbenz" \
            -v=/root/mysql/data:/var/lib/mysql \
            docker.io/mysql:5.6.26
```
## 数据库
```sql
-- 爬取的书籍
create table Book
(
  bookcode int          not null
    primary key,
  name     varchar(150) not null
)
  charset = utf8mb4;


-- 记录章节是否已经爬取
create table Book_Chapter
(
  url         varchar(150)     not null
    primary key,
  bookid      int              not null,
  chaptername varchar(200)     not null,
  flag        int default '-1' not null
)
  charset = utf8mb4;

```


## 常见问题
### pymysql.err.DataError: (1366, 
修改数据库表编码
```sql
alter table <表名>  convert to  character set utf8mb4;
```