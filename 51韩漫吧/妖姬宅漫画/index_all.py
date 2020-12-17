import requests
import json
import os
import urllib.request
from pathlib import Path
import pandas as pd

class Spider(object):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    url_all = 'http://m.18hm.cc/home/api/cate/tp/1-0-2-1-{}' # 全部
    url_over = 'http://m.18hm.cc/home/api/cate/tp/1-0-1-1-{}' # 已完结的
    url_serialize = 'http://m.18hm.cc/home/api/cate/tp/1-0-0-1-{}' # 连载中
    url_chapter_list = 'http://m.18hm.cc/home/api/chapter_list/tp/{}-1-1-200'
    url_image_download = 'https://img.toptoon.club/'
    comic_save_path = ''
    chapter_save_path = ''

    def get_comic_list(self, list_url, comic_root_path):
        flag = True
        index = 1
        while flag:
            url = list_url.format(str(index))
            response = requests.get(url, headers=self.headers, timeout=50)
            html = response.text
            # html = html.encode('gbk', "ignore").decode('gbk')  # 先用gbk编码,忽略掉非法字符,然后再译码
            html = html.encode('utf-8').decode('utf-8')
            response_data = json.loads(html)
            # print(json.loads(html))
            if response_data['code'] == 1:
                result = response_data['result']
                lastPage = result['lastPage']
                list = result['list']
                # print(list)
                for comic in list:
                    self.get_comic_detail(comic['title'], comic['id'], comic_root_path)
                if lastPage:
                    flag = False
                else:
                    index += 1

            else:
                flag = False

    def get_comic_detail(self, comic_title, comic_id, comic_root_path):
        self.comic_save_path = comic_root_path + comic_title.replace(':', '：').replace('?', '？')
        path = Path(self.comic_save_path)
        if path.exists():
            pass
        else:
            path.mkdir()
        self.get_comic_chapter(comic_id)

    def save_comic_detail(self, list_url, save_path):
        post_list = []
        csv_title = ['漫画ID', '标题', '作者', '封面', '内容简介', '是否完结', '最新章节', '题材类型', '关键字', '评分']
        flag = True
        index = 1
        while flag:
            url = list_url.format(str(index))
            response = requests.get(url, headers=self.headers, timeout=50)
            response_data = json.loads(response.text)
            if response_data['code'] == 1:
                result = response_data['result']
                lastPage = result['lastPage']
                list = result['list']
                for comic in list:
                    # print(comic)
                    comic_isover = '已完结' if comic['mhstatus'] == '1' else '连载中'
                    post_list.append([comic['id'], comic['title'], comic['auther'], comic['image'], comic['desc'], comic_isover,
                                      comic['last_chapter_title'], comic['ticai'], comic['keyword'], comic['pingfen']])

                if lastPage:
                    flag = False
                else:
                    index += 1

            else:
                flag = False

        post_data = pd.DataFrame(columns=csv_title, data=post_list)
        post_data.to_csv(save_path, encoding='UTF-8')

    def get_comic_chapter(self, comic_id):
        url = self.url_chapter_list.format(comic_id)
        response = requests.get(url, headers=self.headers, timeout=50)
        response.encoding = response.apparent_encoding
        response_data = json.loads(response.text)
        result = response_data['result']
        print(result)
        list = result['list']
        print(list)
        # print(len(list))
        for item in list:
            title = item['title'].replace(':', '：').replace('?', '？').replace('...', '').strip()
            print('当前章节：', item['title'])
            self.chapter_save_path = self.comic_save_path + '\\' + title
            path = Path(self.chapter_save_path)
            if path.exists():
                pass
            else:
                path.mkdir()
            self.down_img(item['imagelist'])

    def down_img(self, image_list):
        print(image_list.split(','))
        index = 1
        image_list = image_list.split(',')
        for img_url in image_list:
            if index < 10:
                pic_name = '00{}.jpg'.format(str(index))
            elif index < 100:
                pic_name = '0{}.jpg'.format(str(index))
            else:
                pic_name = '{}.jpg'.format(str(index))
            image_path = self.chapter_save_path + '\\' + pic_name
            if os.path.isfile(image_path):
                print("此图已经存在:", image_path)
            else:
                print("图片正在下载:", image_path)
                img_url = self.url_image_download + img_url.replace('./', '')
                print('图片下载地址：', img_url)
                # urllib.request.urlretrieve(img_url, image_path)
                try:
                    pic_data = requests.get(img_url, headers=self.headers, timeout=50)
                    with open(image_path, 'wb') as f:
                        f.write(pic_data.content)
                except:
                    print('图片下载失败：：：', img_url)
            index += 1

    def init_spider(self):
        print("    | ---------------------------------  |")
        print("    |     欢迎使用妖姬宅漫画下载器！         |")
        print("    |       目标站点：m.18hm.cc            |")
        print("    | 作者:zhiyong_wang(946455381@qq.com) |")
        print("    | ================================== |")
        print("    |    1. 下载完结漫画(D:\manhua\完结韩漫) |")
        print("    |    2. 下载连载漫画(D:\manhua\连载韩漫) |")
        print("    |    3. 下载指定漫画                   |")
        print("    |    4. 保存漫画列表信息到本地           |")
        # 选择功能
        option = int(input('请选择功能选项：'))
        if option == 1:
            self.get_comic_list(self.url_over, 'D:\manhua\完结韩漫\\')
        elif option == 2:
            self.get_comic_list(self.url_serialize, 'D:\manhua\连载韩漫\\')
        elif option == 3:
            # 漫画名称
            comic_title = input('请输入你需要下载的漫画名称：')
            # 漫画ID
            comic_id = input('请输入你需要下载的漫画ID：')
            # 漫画保存路径
            comic_root_path = 'D:\manhua\完结韩漫\\'
            self.get_comic_detail(comic_title, comic_id, comic_root_path)
        else:
            self.save_comic_detail(self.url_over, '完结漫画列表.csv')
            self.save_comic_detail(self.url_serialize, '连载漫画列表.csv')

spider = Spider()
spider.init_spider()