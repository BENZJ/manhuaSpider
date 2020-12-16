import fitz 
import os
rootdir = './manhuaSpider/images'
doc = fitz.open()

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