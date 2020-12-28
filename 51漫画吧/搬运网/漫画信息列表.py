import requests
import json
import os
import urllib.request
from pathlib import Path
import pandas as pd

class Spider(object):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'Cookie': 'kd5S_2132_saltkey=Y681pg8c; kd5S_2132_lastvisit=1608698229; kd5S_2132_ulastactivity=3e46Z3C0fXGFD0X0IW4u%2Fw5SGzYuwcj%2Bvm1xXxrSaipKcQ4R5KPd; kd5S_2132_lastcheckfeed=2455716%7C1608810624; kd5S_2132_auth=01cb9AGX9ty6RcCDquw4RgMsoMebjIHaMPI3v%2BYyzSXYi3%2FqL1RIFlvO%2BoQ2ZW5%2BLT9Iygjb41VsjWzwDkmMTXGClVY3; kd5S_2132_tshuz_accountlogin=2455716; kd5S_2132_manhuakaiguan=1; kd5S_2132_manhuamoshi=2; kd5S_2132_manhua_pcadvcookie=1; kd5S_2132_xiazaitime=1608812464102; kd5S_2132_xiazaicishu=4; __cfduid=de39030de4434d811716bd1f2b8d021c71608816056; kd5S_2132_sid=pM5CEZ; kd5S_2132_lip=116.21.228.102%2C1608815897; kd5S_2132_lastact=1608817247%09plugin.php%09'
    }
    url_all = 'http://www.zerobywswit.com/plugin.php' # 全部
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

    def get_img_list(self):
        data = {
            'id': 'jameson_manhua:ajax',
            'zjid': '177823',
            'optype': 'getimglist',
            'formhash': 'dc93ef43',
        }
        response = requests.get(self.url_all, json=data, headers=self.headers, timeout=50)
        response.encoding = response.apparent_encoding
        print(response.text.replace('\u301c','').replace('\xa0',''))

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
        print("1. 下载完结漫画(D:\manhua\完结)")
        print("2. 下载连载漫画(D:\manhua\连载)")
        # 选择功能
        option = int(input('请选择功能选项：'))
        if option == 1:
            self.get_comic_list(self.url_over, 'D:\manhua\完结\\')
        elif option == 2:
            self.get_comic_list(self.url_serialize, 'D:\manhua\连载\\')

spider = Spider()
# spider.init_spider()
spider.get_img_list()







