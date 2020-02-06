import os
import pandas as pd

def save_list(dir_path, save_path):
    post_list = []
    csv_title = ['标题']
    for filename in os.listdir(dir_path):
        print(filename)
        post_list.append([filename.replace('.zip', '')])

    post_data = pd.DataFrame(columns=csv_title, data=post_list)
    post_data.to_csv(save_path, encoding='UTF-8')


if __name__ == '__main__':
    dir_path = input('请输入你目标目录：')
    save_path = input('请输入你需要保存的文件路径：')
    save_list(dir_path, save_path)