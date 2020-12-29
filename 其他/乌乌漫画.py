# -*- coding: utf-8 -*-
# 下面是xpath爬取方法
# @Time    : 2020/1/1 11:20
# @Author  : zhiyong_wang
# @Email   : 946455381@qq.com
# @File    : 漫客栈.py
# @Software: PyCharm

import requests
import json
import urllib.request
from lxml import etree
from pathlib import Path

class Spider(object):
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'no-cache',
        'Cookie': 'PHPSESSID = 44f7a7d151cb840edd5b62041ec57e8d;t1578326400 = v34',
        'Host': 'python2050.applinzi.com',
        'Origin': 'http://python2050.applinzi.com',
        'Referer': 'http://python2050.applinzi.com/Cartoon/Read?CartoonId=502&chapterId=25195'
    }
    web_url = 'https://www.mkzhan.com'
    comic_save_path = ''
    chapter_save_path = ''

    def init_spider(self, comic_id, comic_name):
        comic_url = 'http://python2050.applinzi.com/Cartoon/GetIndexOrderBy?CartoonId=' + str(comic_id) + '&pageStart=0&pageSize=100&orderBy=asc'
        response = requests.post(url=comic_url, headers=self.headers)
        print(response.url)
        print(response.text)
        self.comic_save_path = "comic\\" + comic_name
        path = Path(self.comic_save_path)
        if path.exists():
            pass
        else:
            path.mkdir()

        chapter_list = json.loads(response.text)
        self.chapter_request(chapter_list)

    # 遍历章节列表
    def chapter_request(self, chapter_list):
        for link in chapter_list:
            try:
                # 付费章节返回只有前三张图，没法弄
                chapter_url = 'http://python2050.applinzi.com/Cartoon/GetContent?chapterId='+link['Id']+'&typeId=0&cIndex='+link['Index']+'&ifCheck=0&cartoonId='+link['CartoonId']+'&isBuy=1&sId='+link['CartoonId']
                response = requests.post(url=chapter_url, headers=self.headers)
                print(response.url)
                print(response.text)
                response_data = json.loads(response.text)
                chapter_title = response_data['name']
                print(chapter_title)
                self.chapter_save_path = self.comic_save_path + '\\' + chapter_title
                path = Path(self.chapter_save_path)
                if path.exists():
                    pass
                else:
                    path.mkdir()
                image_list = response_data['imglist']
                self.download_image(image_list)

            except Exception as e:
                print(e)

    # 3. 下载章节的图片
    def download_image(self, image_list):
        index = 1
        for img in image_list:
            image_path = self.chapter_save_path + '\\' + str(index) + '.jpg'
            print(image_path)
            s = urllib.request.urlretrieve(img['u'], image_path)
            index = index + 1
            print("正在下载%s" % img[u])


comic_id = 502
comic_name = '弱点'
spider = Spider()
spider.init_spider(comic_id, comic_name)