# -*- coding: utf-8 -*-
# 下面是xpath爬取方
# @Time    : 2020/1/1 11:20
# @Author  : zhiyong_wang
# @Email   : 946455381@qq.com
# @File    : 漫画牛.py
# @Software: PyCharm

import requests
import urllib.request
from lxml import etree
import urllib.request
import os
from pathlib import Path


class Spider(object):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    web_url = 'https://m.manhuaniu.com'
    chapter_len = ''
    comic_save_path = ''
    chapter_save_path = ''

    def init_spider(self, url, chapter_num, chapter_len):
        self.chapter_len = chapter_len
        r = requests.get(url, headers=self.headers, timeout=5)
        r.encoding = r.apparent_encoding
        r.raise_for_status()
        html = r.text
        html = html.encode('gbk', "ignore").decode('gbk')  # 先用gbk编码,忽略掉非法字符,然后再译码
        html = html.encode('utf-8').decode('utf-8')
        ret = etree.HTML(html)
        title_list = ret.xpath('//div[@class="view-sub autoHeight"]/h1[@class="title"]/text()')
        comic_title = title_list[0]
        print('当前漫画：', comic_title)
        self.comic_save_path = "comic\\" + comic_title
        path = Path(self.comic_save_path)
        if path.exists():
            pass
        else:
            path.mkdir()
        chapter_links = ret.xpath('//ul[@id="chapter-list-1"]/li/a/@href')
        chapter_titles = ret.xpath('//ul[@id="chapter-list-1"]/li/a/span/text()')
        print(chapter_links)
        print(chapter_titles)
        list_len = len(chapter_links)
        chapter_links = chapter_links[chapter_num:list_len]
        list_len2 = len(chapter_titles)
        chapter_titles = chapter_titles[chapter_num:list_len2]
        self.chapter_request(chapter_links, chapter_titles)

    # 遍历章节列表
    def chapter_request(self, chapter_links, chapter_titles):
        for link, title in zip(chapter_links, chapter_titles):
            print('当前章节： ', title)
            print('当前地址： ', link)
            try:
                self.chapter_save_path = self.comic_save_path + '\\' + title
                path = Path(self.chapter_save_path)
                if path.exists():
                    pass
                else:
                    path.mkdir()
                image_list = []
                for index in range(1, self.chapter_len):
                    if index == 1:
                        img_url = link
                    else:
                        img_url = link.replace('.html', '-') + str(index) + '.html'
                    image_list.append(img_url)
                print(image_list)
                self.download_image(image_list)
            except Exception as e:
                print(e)

    # 3. 下载章节的图片
    def download_image(self, image_list):
        index = 1
        for img_url in image_list:
            image_path = self.chapter_save_path + '\\' + str(index) + '.jpg'
            if os.path.isfile(image_path):
                print("此图已经存在:", image_path)
            else:
                r = requests.get(img_url, headers=self.headers, timeout=50)
                r.encoding = r.apparent_encoding
                html = r.text
                html = html.encode('gbk', "ignore").decode('gbk')  # 先用gbk编码,忽略掉非法字符,然后再译码
                html = html.encode('utf-8').decode('utf-8')
                ret = etree.HTML(html)
                image_src = ret.xpath('//mip-link/mip-img/@src')
                print("图片地址:", image_src)
                print("图片正在下载:", image_path)
                urllib.request.urlretrieve(image_src[0], image_path)
            index += 1


# 漫画地址
url = 'https://m.manhuaniu.com/manhua/5942/'
# 第几章节开始
chapter_num = 0
chapter_len = 20 # 每个章节有几张图
spider = Spider()
spider.init_spider(url, chapter_num, chapter_len)
