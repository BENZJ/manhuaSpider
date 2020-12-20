import fitz 
import os
rootdir = '../hmSpider/hmSpider/images'

list = os.listdir(rootdir)
list.sort()
for i in range(0, len(list)):
    doc = fitz.open()
    chiledrootdir = os.path.join(rootdir, list[i])
    childlist = os.listdir(chiledrootdir)
    childlist.sort()
    for j in range(0, len(childlist)):
        img_file = os.path.join(chiledrootdir, childlist[j])
        imgdoc = fitz.open(img_file)
        pdfbytes = imgdoc.convertToPDF()
        pdf_name = str(j) + '.pdf'
        imgpdf = fitz.open(pdf_name, pdfbytes)
        doc.insertPDF(imgpdf)
    doc.save("./out/"+list[i]+'.pdf')
    doc.close()