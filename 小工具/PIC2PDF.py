# PyMuPDF（又名“fitz”）：MuPDF的Python绑定，它是一个轻量级的PDF和XPS查看器。
# 该库可以访问PDF，XPS，OpenXPS，epub，漫画和小说书籍格式的文件，并以其顶级性能和高渲染质量而闻名。
# pip install PyMuPDF 在线安装PDF库
# pip install PyMuPDF-1.16.10-cp37-none-win_amd64.whl  本地安装PDF库
# import fitz   引入PDF库

import glob
import fitz
import os

def pic2pdf(home, dir):
    # print(home)
    # print(dir)
    dir_path = home + '/' + dir
    pdf_path = home + '/' + dir.split('-')[0] + '.pdf'
    if os.path.exists(pdf_path):
        os.remove(pdf_path)

    doc = fitz.open()
    for img in sorted(glob.glob(dir_path + '/*')):
        print(img)
        imgdoc = fitz.open(img)
        pdfbytes = imgdoc.convertToPDF()
        imgpdf = fitz.open('pdf', pdfbytes)
        doc.insertPDF(imgpdf)
    doc.save(pdf_path)
    doc.close()

def listDir(dir_path):
    for home, dirs, files in os.walk(dir_path):
        # print("#######目录{}开始#######".format(home))
        # list = os.listdir(dir_path)
        if len(dirs) > 0:
            for dir in dirs:
                # print(dir)
                pic2pdf(home, dir)
        # print("#######目录{}结束#######".format(home))


if __name__ == '__main__':
    # pic2pdf()
    # dir_path = 'comic/堕落教师'
    dir_path = input('请输入你需要将JPG图片合并成PDF的漫画目录：')
    listDir(dir_path)