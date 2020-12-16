import fitz 
import os
rootdir = './manhuaSpider/images'
doc = fitz.open()



# if __name__ == "__main__":
#     rootdir = './manhuaSpider/images/00001_前篇'
#     list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
#     for i in range(0, len(list)):
#         path = os.path.join(rootdir, list[i])
#         print(path)


# 循环path中的文件，可import os 然后用 for img in os.listdir(img_path)实现
# 这里为了让文件以1，2，3的形式进行拼接，就偷懒循环文件名中的数字。
list = os.listdir(rootdir)
list.sort()
for i in range(0, len(list)):
    chiledrootdir = os.path.join(rootdir, list[i])
    childlist = os.listdir(chiledrootdir)
    childlist.sort()
    for j in range(0, len(childlist)):
        img_file = os.path.join(chiledrootdir, childlist[j])
        print(img_file)
        imgdoc = fitz.open(img_file)
        pdfbytes = imgdoc.convertToPDF()
        pdf_name = str(j) + '.pdf'
        imgpdf = fitz.open(pdf_name, pdfbytes)
        doc.insertPDF(imgpdf)
doc.save('combined.pdf')
doc.close()