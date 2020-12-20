import img2pdf 
import os 
from PyPDF2 import PdfFileMerger

rootDir = "../manhuaSpider/manhuaSpider/images"
list = os.listdir(rootDir)
list.sort()

file_merger = PdfFileMerger()
for i in range(0, len(list)):
    chiledRootDir = os.path.join(rootDir, list[i])
    childList = [f for f in os.listdir(chiledRootDir) if f.endswith('.jpg')]
    childList.sort()
    images = []
    for j in range(0, len(childList)):
        img_file = os.path.join(chiledRootDir, childList[j])
        print(img_file)
        images.append(img_file)
    pdf_bytes = img2pdf.convert(images)
    file = open("./out/"+list[i]+".pdf", "wb")
    file.write(pdf_bytes) 
    file.close() 
    print("Successfully made pdf file") 

