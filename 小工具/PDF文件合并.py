import glob
import fitz
import os


class PDFMerge(object):
    need_encrypt = 2
    perm = int(fitz.PDF_PERM_ACCESSIBILITY) # always use this
    owner_pass = "wzy1990"  # owner password
    user_pass = "51mhb.com"  # user password
    encrypt_meth = fitz.PDF_ENCRYPT_AES_256  # strongest algorithm

    # 合并PDF文件
    def mergePDFs(self, root, dir):
        dir_path = root + '/' + dir

        if self.need_encrypt == 1:
            merge_pdf_path = root + '/' + dir + '【' + self.user_pass + '】' + '.pdf'
        else:
            merge_pdf_path = root + '/' + dir + '.pdf'

        if os.path.exists(merge_pdf_path):
            os.remove(merge_pdf_path)

        pdf_list = sorted(glob.glob(dir_path + '/*.pdf'))
        print(pdf_list)
        merge_pdf = fitz.open()

        if len(pdf_list) > 0:
            for pdf_path in pdf_list:
                print(os.path.join(root, pdf_path))
                pdfdoc = fitz.open(os.path.join(root, pdf_path))
                merge_pdf.insertPDF(pdfdoc)
            if self.need_encrypt == 1:
                merge_pdf.save(merge_pdf_path,
                                encryption = self.encrypt_meth,  # set the encryption method
                                owner_pw = self.owner_pass,  # set the owner password
                                user_pw = self.user_pass,  # set the user password
                                permissions = self.perm)  # set permissions
            else:
                merge_pdf.save(merge_pdf_path)
        merge_pdf.close()

    def list_dir(self, dir_path):
        count_index = 0
        for home, dirs, files in os.walk(dir_path):
            if count_index < 1:
                # print("#######目录{}开始#######".format(home))
                if len(dirs) > 0:
                    for dir in dirs:
                        # print(dir)
                        self.mergePDFs(home, dir)
                # print("#######目录{}结束#######".format(home))
            count_index += 1

    # 将目标文件夹下的所有的漫画PDF一一合并
    def list_root_dir(self, root_path):
        dirs = os.listdir(root_path)
        print(dirs)
        if len(dirs) > 0:
            for dir in dirs:
                dir_path = os.path.join(root_path, dir)
                print(dir_path)
                self.list_dir(dir_path)

    def init(self):
        flag = True
        while flag:
            print("    | ---------------------------------|")
            print("    |     欢迎使用PDF合并小工具！         |")
            print("    | =================================|")
            print("    |    1. 指定某个漫画PDF目录          |")
            print("    |    2. 指定漫画PDF列表目录          |")
            # # 选择功能
            option = int(input('请选择功能选项：'))
            dir_path = input('请输入需要合并的漫画PDF目录：')
            self.need_encrypt = int(input('是否加密合并后的PDF文件？ 1.加密  2.不加密 \n'))

            if option == 1:
                self.list_dir(dir_path)
            elif option == 2:
                self.list_root_dir(dir_path)

            is_continue = input('是否继续合并其他PDF文件？ 1.继续  2.退出 \n')
            if is_continue != '1':
                flag = False


pdfMerge = PDFMerge()
pdfMerge.init()
