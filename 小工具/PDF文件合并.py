import glob
import fitz
import os

# 合并PDF文件
def mergePDFs(root, dir):
    dir_path = root + '/' + dir
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
        merge_pdf.save(merge_pdf_path)
    merge_pdf.close()


def listDir(dir_path):
    for home, dirs, files in os.walk(dir_path):
        # print("#######目录{}开始#######".format(home))
        # list = os.listdir(dir_path)
        if len(dirs) > 0:
            for dir in dirs:
                # print(dir)
                mergePDFs(home, dir)
        # print("#######目录{}结束#######".format(home))

if __name__ == '__main__':
    dir_path = input('请输入你需要合并的PDF目录：')
    listDir(dir_path)