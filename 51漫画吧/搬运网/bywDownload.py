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
        'Connection': 'keep-alive',
        'Host': 'www.zerobywswit.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        'Cookie': 'kd5S_2132_saltkey=Y681pg8c; kd5S_2132_lastvisit=1608698229; __cfduid=de39030de4434d811716bd1f2b8d021c71608816056; kd5S_2132_nofavfid=1; kd5S_2132_manhuakaiguan=1; kd5S_2132_manhuamoshi=2; kd5S_2132_lastcheckfeed=2455716%7C1609331082; kd5S_2132_manhua_pcadvcookie=5; kd5S_2132_creditnotice=0D0D2D0D0D0D0D0D0D2455716; kd5S_2132_creditbase=0D0D16D0D0D0D0D0D0; kd5S_2132_creditrule=%E6%AF%8F%E5%A4%A9%E7%99%BB%E5%BD%95; kd5S_2132_ulastactivity=f71eJBP%2F55uWoMMAdOC%2FNcALNrNvEa03e3xNDETEZKdRRZBwftVM; kd5S_2132_auth=a0709A2AGHLbWE%2BJMsD3M%2B8Qdk04bCnNL90mWRiS424A7E6PwkW5iwV5UZ7WPwWKjanZTXwSxtr88vbjud3S2ibSi9JH; kd5S_2132_tshuz_accountlogin=2455716; kd5S_2132_sid=P9e629; kd5S_2132_lip=113.111.7.79%2C1609402079; kd5S_2132_lastact=1609402093%09home.php%09spacecp'
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
                # print(chapter_html)
                chapter_title = chapter_html.find('h3', {'class': 'uk-heading-line uk-text-center'}).text
                print('当前章节： ', chapter_title)
                self.chapter_save_path = self.comic_save_path + '\\' + chapter_title
                path = Path(self.chapter_save_path)
                if path.exists():
                    pass
                else:
                    path.mkdir()

                image_list = chapter_html.find_all('div', {'class': 'uk-text-center mb0'})
                # self.download_image(image_list)
                # 开启多线程
                pool = ThreadPool(8) # Sets the pool size to 4
                results = pool.map(self.download_image, image_list)
                pool.close();
                pool.join();
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
