import requests
import json
import os
import urllib.request
from pathlib import Path
from lxml import etree

class Spider(object):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    url_all = 'http://m.18hm.cc/home/api/cate/tp/1-0-2-1-{}' # 全部
    url_near = 'http://m.18hm.cc/home/api/cate/tp/1-0-1-1-{}' # 已完结的
    url_click = 'http://m.18hm.cc/home/api/cate/tp/1-0-0-1-{}' # 连载中
    web_url = 'https://www.mkzhan.com'
    comic_save_path = ''
    chapter_save_path = ''

    def init_spider(self):
        flag = True
        index = 1
        while flag:
            url = self.url_click.format(str(index))
            response = requests.get(url, headers=self.headers, timeout=50)
            response_data = json.loads(response.text)
            print(response_data)
            if response_data['code'] == 1:
                result = response_data['result']
                lastPage = result['lastPage']
                list = result['list']
                print(list)
                for comic in list:
                    comic_title = comic['title']
                    self.comic_save_path = "comic\\" + comic_title.replace(':', '：').replace('?', '？')
                    path = Path(self.comic_save_path)
                    if path.exists():
                        pass
                    else:
                        path.mkdir()
                    self.get_chapter(comic['id'])
                if lastPage:
                    flag = False
                else:
                    index += 1

            else:
                flag = False

    def get_chapter(self, chapter_id):
        url = 'http://m.18hm.cc/home/api/chapter_list/tp/{}-1-1-200'.format(chapter_id)
        response = requests.get(url, headers=self.headers, timeout=50)
        response_data = json.loads(response.text)
        result = response_data['result']
        list = result['list']
        print(list)
        # print(len(list))
        for item in list:
            print('当前章节：', item['title'])
            self.chapter_save_path = self.comic_save_path + '\\' + item['title']
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
            image_path = self.chapter_save_path + '\\' + str(index) + '.jpg'
            if os.path.isfile(image_path):
                print("此图已经存在:", image_path)
            else:
                print("图片正在下载:", image_path)
                img_url = 'http://17z.online/' + img_url.replace('./', '')
                print('下载地址：', img_url)
                urllib.request.urlretrieve(img_url, image_path)
            index += 1


spider = Spider()
spider.init_spider()
# spider.get_chapter()