from scrapy.cmdline import execute
import sys
import os
import pymysql
import subprocess
from PyPDF2 import PdfFileMerger
import img2pdf 
import smtplib
from email.mime.text import MIMEText #邮件文本
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
# TRXGGYPBEUIFJFES
def sendMail(bookname:str, pdfDir:str ) :
    content_part = MIMEText(
    """<h2>漫画更新</h2>
        <p>{0}</p>
<br>
<h5>祝生活愉快</h5>
<p>XXXXXX</p>
    """.format(bookname), "html", "utf-8")
    #添加附件（pdf文档）
    pdfFile = pdfDir+".pdf"  #需发文件路径
    pdf = MIMEApplication(open(pdfFile, 'rb').read())
    pdf.add_header('Content-Disposition', 'attachment', filename='漫画')
    m = MIMEMultipart()
    m.attach(content_part)  #添加邮件正文内容
    m.attach(pdf)
    m['Subject'] = '漫画更新{}'.format(bookname) #邮件主题
    m['From'] = "benz_auto@163.com"   #发件人
    m['To'] = "549614989@qq.com"    #收件人
    try:
        # 发件人邮箱中的SMTP服务器，163邮箱的端口是465
        server=smtplib.SMTP_SSL("smtp.163.com", 465)
        # 登陆邮箱（参数1：发件人邮箱，参数2：邮箱授权码）
        server.login("benz_auto@163.com", "TRXGGYPBEUIFJFES")
        # 发送邮件（参数1：发件人邮箱，参数2：若干收件人邮箱，参数3：把邮件内容格式改为str）
        server.sendmail("benz_auto@163.com", ["549614989@qq.com" ], m.as_string())
        print('发送邮件成功')
        server.quit()
        pass
    except Exception as e:
        print ("Error: 无法发送邮件,",e)
# sendMail("元尊/00573_第272话上 拍碎剑丸/","./manhuaSpider/out/元尊/00573_第272话上 拍碎剑丸")
# exit()
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
            sendMail(chaptername,outRir+chaptername)          
        except Exception as e:
            print("生成PDF错误，Exeception occured:{}".format(e))
            pass
        db.commit()
except Exception as e:
    print("数据库执行错误，Exeception occured:{}".format(e))
    pass
finally:
    # 关闭数据库链接
    db.close()
# 
# subprocess.Popen('scrapy crawl bookindex', shell=True).wait()
# subprocess.Popen('scrapy crawl bookindex', shell=True).wait()

