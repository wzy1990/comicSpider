# -*- coding: utf-8 -*-
# 下面是xpath爬取方法，可跳过vip验证，直接爬取付费内容（漫客栈的vip）
# @Time    : 2020/1/1 11:20
# @Author  : zhiyong_wang
# @Email   : 946455381@qq.com
# @File    : 漫客栈.py
# @Software: PyCharm

import requests
import urllib.request
from lxml import etree
import urllib.request
from pathlib import Path

class Spider(object):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    web_url = 'https://www.mkzhan.com'
    comic_save_path = ''
    chapter_save_path = ''

    def init_spider(self, url):

        r = requests.get(url, headers=self.headers, timeout=5)
        r.encoding = r.apparent_encoding
        r.raise_for_status()
        html = r.text
        html = html.encode('gbk', "ignore").decode('gbk')  # 先用gbk编码,忽略掉非法字符,然后再译码
        html = html.encode('utf-8').decode('utf-8')
        ret = etree.HTML(html)
        title_list = ret.xpath('//p[@class="comic-title j-comic-title"]')
        comic_title = title_list[0].text
        self.comic_save_path = "comic\\" + comic_title
        path = Path(self.comic_save_path)
        if path.exists():
            pass
        else:
            path.mkdir()
        chapterLinks = ret.xpath('//a[@class="j-chapter-link"]/@data-hreflink')
        print(chapterLinks)
        chapterLinks.reverse()
        self.chapter_request(chapterLinks)

    # 遍历章节列表
    def chapter_request(self, chapterLinks):
        for link in chapterLinks:
            link = self.web_url + link
            print(link)
            try:
                t = requests.get(link)
                parse = t.text
                parse = parse.encode('gbk', "ignore").decode('gbk')  # 先用gbk编码,忽略掉非法字符,然后再译码
                parse = parse.encode('utf-8').decode('utf-8')
                # print(parse)
                treee = etree.HTML(parse)

                chapter_title = treee.xpath('//h1[@class="comic-title"]/a[@class="last-crumb"]/text()')
                print(chapter_title[0])
                self.chapter_save_path = self.comic_save_path + '\\' + chapter_title[0]
                path = Path(self.chapter_save_path)
                if path.exists():
                    pass
                else:
                    path.mkdir()
                image = treee.xpath('//div[@class="rd-article__pic hide"]/img[@class="lazy-read"]/@data-src')
                self.download_image(image)

            except Exception as e:
                print(e)

    # 3. 下载章节的图片
    def download_image(self, image):
        index = 1
        for img in image:
            image_url = self.chapter_save_path + '\\' + str(index) + '.jpg'
            print(image_url)
            s = urllib.request.urlretrieve(img, image_url)
            index = index + 1
            print("正在下载%s" % img)

url = 'https://www.mkzhan.com/49733/'
spider = Spider()
spider.init_spider(url)