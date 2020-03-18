import glob
import fitz
import os

# 给PDF文件插入一页图片
def insert_pdf():
    dir_path = input('请输入漫画目录：')
    for home, dirs, files in os.walk(dir_path):
        # print("#######目录{}开始#######".format(home))
        if len(files) > 0:
            for file in files:
                file_path = home + '/' + file
                pdf_doc = fitz.open(file_path)
                insert_logo_page(pdf_doc)
                save_path = file_path.replace('.pdf', '【51mhb.com】.pdf')
                pdf_doc.save(save_path)
                pdf_doc.close()
        # print("#######目录{}结束#######".format(home))

def insert_logo_page(pdf_doc):
    img_doc = fitz.open('D:\\51漫画吧LOGO.png')
    rect = img_doc[0].rect
    rect_width = 800
    rect_height = rect.height / rect.width * rect_width
    pdfbytes = img_doc.convertToPDF()
    img_doc.close()
    imgpdf = fitz.open('pdf', pdfbytes)
    page = pdf_doc.newPage(width=rect_width, height=rect_height)
    page.showPDFpage((0.0, 0.0, rect_width, rect_height), imgpdf, -1)  # image fills the page
    # # 首页插入
    # pdf_doc.insertPDF(imgpdf, start_at=0)
    # # 尾页插入
    # pdf_doc.insertPDF(imgpdf, start_at=-1)


if __name__ == '__main__':
    # dir_path = input('请输入你需要将JPG图片合并成PDF的漫画目录：')
    insert_pdf()