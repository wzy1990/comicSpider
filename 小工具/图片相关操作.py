import glob
import fitz
import os
import imghdr

# 批量修改图片名称
def change_img_name(dest_path):
    for root, dirs, files in os.walk(dest_path):
        if len(files) > 1:
            for file in files:
                print(file)
                file_num = int(file.replace('.jpg', ''))
                if file_num < 10:
                    file_name = '00{}.jpg'.format(str(file_num))
                elif file_num < 100:
                    file_name = '0{}.jpg'.format(str(file_num))
                else:
                    file_name = '{}.jpg'.format(str(file_num))
                print(file_name)
                os.rename(os.path.join(root, file), os.path.join(root, file_name))

# 批量删除损坏的图片
def del_bad_img(dest_path):
    for root, dirs, files in os.walk(dest_path):
        if len(files) > 1:
            # print(files)
            for file in files:
                file_name = os.path.join(root, file)
                check = imghdr.what(file_name)
                if check == None:
                    print(root, file_name)
                    os.remove(file_name)


if __name__ == '__main__':
    print("    | --------------------------------- |")
    print("    |     欢迎使用JPG操作小工具！          |")
    print("    | ================================= |")
    print("    |    1. 修改漫画图片名称              |")
    print("    |    2. 删除损坏的漫画图片             |")
    # # 选择功能
    option = int(input('请选择功能选项：'))
    dest_path = input('请输入漫画目录：')
    if option == 1:
        change_img_name(dest_path)
    else:
        del_bad_img(dest_path)