# PyMuPDF（又名“fitz”）：MuPDF的Python绑定，它是一个轻量级的PDF和XPS查看器。
# 该库可以访问PDF，XPS，OpenXPS，epub，漫画和小说书籍格式的文件，并以其顶级性能和高渲染质量而闻名。
# pip install PyMuPDF 在线安装PDF库
# pip install PyMuPDF-1.16.10-cp37-none-win_amd64.whl  本地安装PDF库
# import fitz   引入PDF库

import glob
import fitz
import os
from pathlib import Path

class Pdftool(object):
    def pic2pdf(self, home, dir):
        # print(home, dir)
        dir_path = home + '/' + dir
        pdf_dir = home + '【PDF版】/'
        pdf_path = pdf_dir + dir.split('-')[0] + '.pdf'

        path = Path(pdf_dir)
        if path.exists():
            pass
        else:
            path.mkdir()
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

        print(dir_path)
        img_list = sorted(glob.glob(dir_path + '/*.jpg'))
        print(img_list)

        if len(img_list) > 0:
            self.saveToPDF(img_list, pdf_path)

    def saveToPDF(self, img_list, pdf_path):
        doc = fitz.open()
        for img in img_list:
            print(img)
            try:
                imgdoc = fitz.open(img)  # open pic as document
                rect = imgdoc[0].rect  # pic dimension
                rect_width = 900
                rect_height = rect.height / rect.width * 900
                pdfbytes = imgdoc.convertToPDF()  # make a PDF stream
                imgdoc.close()  # no longer needed
                imgpdf = fitz.open('pdf', pdfbytes)  # open stream as PDF
                page = doc.newPage(width=rect_width, height=rect_height)
                page.showPDFpage((0.0, 0.0, rect_width, rect_height), imgpdf, 0)  # image fills the page
            except:
                pass
        doc.save(pdf_path)
        doc.close()

    def list_dir(self, dir_path):
        count_index = 0
        for home, dirs, files in os.walk(dir_path):
            if count_index < 1:
                # print("#######目录{}开始#######".format(home))
                if len(dirs) > 0:
                    for dir in dirs:
                        print(home, dir)
                        self.pic2pdf(home, dir)
                if len(files) > 0:
                    img_list = []
                    for img in files:
                        img_list.append(os.path.join(home, img))
                    self.saveToPDF(img_list, home + '.pdf')
                # print("#######目录{}结束#######".format(home))
            count_index += 1

    # 将目标文件夹下的所有的漫画一一转化成PDF格式
    def list_root_dir(self, root_path):
        dirs = os.listdir(root_path)
        print(dirs)
        if len(dirs) > 0:
            for dir in dirs:
                dir_path = os.path.join(root_path, dir)
                print(dir_path)
                self.list_dir(dir_path)

    def init(self):
        print("    | --------------------------------- |")
        print("    |     欢迎使用JPG转PDF小工具！         |")
        print("    | ================================= |")
        print("    |    1. 指定某个漫画目录              |")
        print("    |    2. 指定漫画列表目录              |")
        # # 选择功能
        option = int(input('请选择功能选项：'))
        dir_path = input('请输入漫画目录：')
        if option == 1:
            self.list_dir(dir_path)
        elif option == 2:
            self.list_root_dir(dir_path)


pdfTool = Pdftool()
pdfTool.init()

# imgdoc = fitz.open(img)  # open pic as document
# pdfbytes = imgdoc.convertToPDF()  # make a PDF stream
# imgdoc.close()  # no longer needed
# imgpdf = fitz.open('pdf', pdfbytes)  # open stream as PDF
# doc.insertPDF(imgpdf)