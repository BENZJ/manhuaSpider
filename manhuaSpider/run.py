from scrapy.cmdline import execute
import sys
import os
import pymysql
import subprocess
from PyPDF2 import PdfFileMerger
import img2pdf 

def mkpdf(rootdir, savename):
    print(os.getcwd())
    list = [f for f in os.listdir(rootdir) if f.endswith('.jpg')]
    list.sort()
    images = []
    for j in range(0, len(list)):
        img_file = os.path.join(rootdir, list[j])
        print(img_file)
        images.append(img_file)
    pdf_bytes = img2pdf.convert(images)
    file = open(savename+".pdf", "wb")
    file.write(pdf_bytes) 
    file.close() 
    print("Successfully made pdf file") 

bookcode=["14289","12780",]

db = pymysql.connect(
    host='49.235.207.129',
    port=3309,
    db='MAN_HUA',
    user='root',
    password='jbcbenz',
    charset='utf8',
)
        # 通过cursor执行增删查改
cursor = db.cursor()

for code in bookcode:
    subprocess.Popen('scrapy crawl bookindex -a bookid={0}'.format(code), shell=True).wait()
try: 
    # 执行sql
    sql = "SELECT * FROM Book_Chapter WHERE flag=-1"
    cursor.execute(sql)
    results = cursor.fetchall() 
    for row in results:
        url = row[0]
        bookid = row[1]
        chaptername = row[2]
        subprocess.Popen('scrapy crawl chapterSpider -a chaptername="{0}" -a start_urls="{1}"'.format(chaptername,"http://m.qiman6.com"+url), 
        shell=True).wait()
        sql = 'UPDATE Book_Chapter set flag = 1 where url="{0}"'.format(url)
        cursor.execute(sql)
        rootDir = "./manhuaSpider/images/"
        outRir="./manhuaSpider/out/"
        outChildDir = outRir+chaptername.split("/",1)[0]
        ##判断目录是否存在
        if os.path.isdir(outChildDir):
            pass
        else:
            os.mkdir(outChildDir)
        try:
            mkpdf(rootDir+chaptername,outRir+chaptername)
        except Exception as e:
            print("Exeception occured:{}".format(e))
            pass
        db.commit()
except Exception as e:
    print("Exeception occured:{}".format(e))
    pass
finally:
    # 关闭数据库链接
    db.close()
# 
# subprocess.Popen('scrapy crawl bookindex', shell=True).wait()
# subprocess.Popen('scrapy crawl bookindex', shell=True).wait()

