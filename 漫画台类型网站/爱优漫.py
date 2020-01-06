# -*- coding: utf-8 -*-
# 可跳过vip验证，直接爬取付费内容
# @Time    : 2020/1/4 15:20
# @Author  : zhiyong_wang
# @Email   : 946455381@qq.com
# @File    : 爱优漫.py
# @Software: PyCharm

import requests
import urllib.request
from lxml import etree
import urllib.request
from pathlib import Path
import os


class Spider(object):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    web_url = 'https://www.iyouman.com/'
    img_url = 'https://mhpic.jumanhua.com/comic'
    img_sub = '.jpg-aym.middle.webp'
    comic_title = ''
    img_url_comic = ''
    img_url_chapter = ''
    initials = 'L'
    prefix = ''
    suffix = '话GQ'
    comic_save_path = ''
    chapter_save_path = ''

    def init_spider(self, url, initials, prefix, suffix, comic_title):
        self.comic_title = comic_title
        self.initials = initials
        self.prefix = prefix
        self.suffix = suffix

        response = requests.get(url, headers=self.headers, timeout=5)
        response.encoding = response.apparent_encoding
        response.raise_for_status()
        html = response.text
        html = html.encode('gbk', "ignore").decode('gbk')  # 先用gbk编码,忽略掉非法字符,然后再译码
        html = html.encode('utf-8').decode('utf-8')
        tree = etree.HTML(html)
        title_list = tree.xpath('//h1[@id="detail-title"]/text()')
        comic_title = title_list[0]
        self.comic_save_path = "comic\\" + comic_title
        if self.comic_title:
            self.img_url_comic = self.img_url + '/' + self.initials + '/' + self.comic_title
        else:
            self.img_url_comic = self.img_url + '/' + self.initials + '/' + comic_title

        print(self.img_url_comic)
        path = Path(self.comic_save_path)
        if path.exists():
            pass
        else:
            path.mkdir()
        chapterTitles = tree.xpath('//ol[@id="j_chapter_list"]/li/a/@title')
        chapterLinks = tree.xpath('//ol[@id="j_chapter_list"]/li/a/@href')
        print(chapterLinks)
        chapterLinks.reverse()
        chapterTitles.reverse()
        self.chapter_request(chapterLinks, chapterTitles)

    # 遍历章节列表
    def chapter_request(self, chapterLinks, chapterTitles):
        index = 0
        for link in chapterLinks:
            chapter_num = chapterTitles[index].split('话')[0].replace('第', '')
            print(chapter_num)
            self.img_url_chapter = self.img_url_comic + '/' + self.prefix + chapter_num + self.suffix + '/'
            print(self.img_url_chapter)
            link = self.web_url + link
            print(link)
            self.chapter_save_path = self.comic_save_path + '\\' + chapterTitles[index]
            path = Path(self.chapter_save_path)
            if path.exists():
                pass
            else:
                path.mkdir()

            index += 1
            self.download_image()

    # 3. 下载章节的图片
    def download_image(self):
        for img_num in range(1, 50):
            img_download_url = self.img_url_chapter + str(img_num) + self.img_sub
            print(img_download_url)
            image_url = self.chapter_save_path + '\\' + str(img_num) + '.jpg'
            print(image_url)
            # s = urllib.request.urlretrieve(img_download_url, image_url)
            # print("正在下载%s" % img_download_url)
            if os.path.isfile(image_url):
                print("########此图已经下载########")
            else:
                try:
                    pic_data = requests.get(img_download_url, headers=self.headers)
                    if pic_data.status_code == 200:
                        with open(image_url, 'wb') as f:
                            f.write(pic_data.content)
                    else:
                        break
                except:
                    pass

# https://mhpic.jumanhua.com/comic/B/不嫁总裁嫁男仆重切版/251话/1.jpg-aym.middle.webp
url = 'https://www.iyouman.com/104754/'
comic_title = '不嫁总裁嫁男仆重切版'
initials = 'B'
prefix = ''
suffix = '话V'
spider = Spider()
spider.init_spider(url, initials, prefix, suffix, comic_title)