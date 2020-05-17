import os
import glob
import fitz


class PDFDelete(object):
    def del_selected_page(self, dir_path, page_index):
        # for filename in os.listdir(r'G:\漫画\已上传\其他\韩漫'):
        for pdf in sorted(glob.glob(dir_path + '/*')):
            print(pdf)
            doc = fitz.open(pdf)
            doc.deletePage(page_index)
            save_name = pdf.replace('-', '~').replace('_压缩', '')
            doc.save(save_name)
            doc.close()

    def init(self):
        flag = True
        while flag:
            print("    | --------------------------------- |")
            print("    |     欢迎使用JPG转PDF小工具！         |")
            print("    | ================================= |")
            dir_path = input('请输入你需要操作的PDF目录：')
            num = int(input('你需要删除的第几页：'))
            self.del_selected_page(dir_path, num)

            is_continue = input('是否继续操作其他PDF文件？ 1.继续  2.退出 \n')
            if is_continue != '1':
                flag = False


pdfDelete = PDFDelete()
pdfDelete.init()