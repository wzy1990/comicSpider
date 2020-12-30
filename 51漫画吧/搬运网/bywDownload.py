# coding:utf-8
# import datetime
import random
import requests
import importlib, sys
import pandas as pd
import os
import json
import urllib.request
from bs4 import BeautifulSoup as bs
from datetime import datetime
from pathlib import Path

importlib.reload(sys)

class Downloader(object):
    comic_path = 'comic_list.csv'
    comic_root_path = 'D:\comic\\'
    comic_save_path = ''
    chapter_save_path = ''
    headers = {
        'Host': 'www.zerobywswit.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Cookie': 'kd5S_2132_saltkey=Y681pg8c; kd5S_2132_lastvisit=1608698229; __cfduid=de39030de4434d811716bd1f2b8d021c71608816056; kd5S_2132_nofavfid=1; kd5S_2132_manhuakaiguan=1; kd5S_2132_manhuamoshi=2; kd5S_2132_sendmail=1; kd5S_2132_sid=lUdL8E; kd5S_2132_ulastactivity=5393IDwHv%2BsNKRBc9wo7%2BpJ4zXLpezRBjGMMqYQkZCTcT5br4VPF; kd5S_2132_lastcheckfeed=2455716%7C1609331082; kd5S_2132_checkfollow=1; kd5S_2132_lastact=1609331082%09plugin.php%09; kd5S_2132_manhua_pcadvcookie=3; kd5S_2132_auth=f001%2FrMc5nRgZTz0Vx4zVWftVcKg%2FpcONXM4%2BLI3hFmfyXJJoB53rE029nfx1dbfCtI5pkAjwAD4FY20uf9JVKlKx9hB; kd5S_2132_tshuz_accountlogin=2455716'
    }

    # 获取网页信息
    def get_html(self, url):
        html = requests.get(url, headers=self.headers, timeout=50)
        html.encoding = html.apparent_encoding # ☾'utf8'
        soup = bs(html.text, 'lxml')
        return soup

    def get_csv_data(self, begin, end):
        # 必须添加header=None，否则默认把第一行数据处理成列名导致缺失
        data = pd.read_csv(self.comic_path, encoding='utf8', header=None)
        csv_reader_lines = data.values.tolist()
        for index in range(begin, end):
            comic_data = csv_reader_lines[index]
            comic_title = comic_data[1]
            print(comic_title)
            self.comic_save_path = self.comic_root_path + comic_title
            path = Path(self.comic_save_path)
            if path.exists():
                pass
            else:
                path.mkdir()

            chapter_links = comic_data[7].split(',')
            self.get_comic_chapter_img(chapter_links)

    def get_comic_chapter_img(self, chapter_links):
        for link in chapter_links:
            try:
                chapter_html = self.get_html(link)
                chapter_title = chapter_html.find('h3', {'class': 'uk-heading-line uk-text-center'}).text
                print('当前章节： ', chapter_title)
                self.chapter_save_path = self.comic_save_path + '\\' + chapter_title
                path = Path(self.chapter_save_path)
                if path.exists():
                    pass
                else:
                    path.mkdir()

                image_list = chapter_html.find_all('div', {'class': 'uk-text-center mb0'})
                self.download_image(image_list)
            except Exception as e:
                print(e)
        

    # 3. 下载章节的图片
    def download_image(self, image_list):
        for image in image_list:
            pic_name = image.find('div', {'class': 'uk-text-center xg1 xs2'}).text.split('/')[0]
            image_path = self.chapter_save_path + '\\' + pic_name + '.jpg'
            image_url = image.find('img')['src']
            print(image_path, image_url)
            if os.path.isfile(image_path):
                print("此图已经存在:", image_path)
            else:
                print("图片正在下载:", image_path)
                print('图片下载地址：', image_url)
                try:
                    # urllib.request.urlretrieve(image_url, image_path)
                    pic_data = requests.get(image_url)
                    with open(image_path, 'wb') as f:
                        f.write(pic_data.content)
                except:
                    print('图片下载失败：：：', image_url)
        

# start  
startTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print('startTime：', startTime)
imgDownloader = Downloader()

imgDownloader.get_csv_data(1, 2)

endTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print('endTime：', endTime)
print("################## finish... ##################")
