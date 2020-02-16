import os
import glob
import fitz


def del_selected_page(dir_path, page_index):
    # for filename in os.listdir(r'G:\漫画\已上传\其他\韩漫'):
    for pdf in sorted(glob.glob(dir_path + '/*')):
        print(pdf)
        doc = fitz.open(pdf)
        doc.deletePage(page_index)
        save_name = pdf.replace('-', '').replace('_压缩', '')
        doc.save(save_name)
        doc.close()


if __name__ == '__main__':
    dir_path = input('请输入你需要编辑的PDF目录：')
    num = int(input('你需要删除的第几页：'))
    del_selected_page(dir_path, num)