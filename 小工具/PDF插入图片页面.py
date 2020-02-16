import glob
import fitz
import os

# 给PDF文件插入一页图片
def insert_pdf():
    doc = fitz.open('D:\python_spider\妖姬宅漫画\comic\PDF\merge.pdf')
    imgdoc = fitz.open('D:\python_spider\妖姬宅漫画\comic\PDF\漫画吧1.jpg')
    pdfbytes = imgdoc.convertToPDF()
    imgpdf = fitz.open('pdf', pdfbytes)
    # 首页插入
    doc.insertPDF(imgpdf, start_at=0)
    # 尾页插入
    doc.insertPDF(imgpdf, start_at=-1)
    doc.save('D:\python_spider\妖姬宅漫画\comic\PDF\merge2.pdf')
    doc.close()

if __name__ == '__main__':
    # dir_path = input('请输入你需要将JPG图片合并成PDF的漫画目录：')
    insert_pdf()