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
import os
from pathlib import Path


class Spider(object):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    comic_url = 'https://www.mkzhan.com/{}/'
    web_url = 'https://www.mkzhan.com'
    comic_save_path = ''
    chapter_save_path = ''

    def init_spider(self, comic_id, chapter_num):
        r = requests.get(self.comic_url.format(comic_id), headers=self.headers, timeout=50)
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
        chapter_links = ret.xpath('//a[@class="j-chapter-link"]/@data-hreflink')
        chapter_links.reverse()
        list_len = len(chapter_links)
        chapter_links = chapter_links[chapter_num:list_len]
        # print(chapter_links)
        self.chapter_request(chapter_links)

    # 遍历章节列表
    def chapter_request(self, chapter_links):
        for link in chapter_links:
            link = self.web_url + link
            print(link)
            try:
                t = requests.get(link)
                parse = t.text
                parse = parse.encode('gbk', "ignore").decode('gbk')  # 先用gbk编码,忽略掉非法字符,然后再译码
                parse = parse.encode('utf-8').decode('utf-8')
                html = etree.HTML(parse)
                chapter_title = html.xpath('//h1[@class="comic-title"]/a[@class="last-crumb"]/text()')
                print('当前章节： ', chapter_title[0])
                self.chapter_save_path = self.comic_save_path + '\\' + chapter_title[0]
                path = Path(self.chapter_save_path)
                if path.exists():
                    pass
                else:
                    path.mkdir()
                image = html.xpath('//div[@class="rd-article__pic hide"]/img[@class="lazy-read"]/@data-src')
                self.download_image(image)
            except Exception as e:
                print(e)

    # 3. 下载章节的图片
    def download_image(self, image_list):
        index = 1
        for img_url in image_list:
            if index < 10:
                pic_name = '0' + str(index)
            else:
                pic_name = str(index)
            image_path = self.chapter_save_path + '\\' + pic_name + '.jpg'
            if os.path.isfile(image_path):
                print("此图已经存在:", image_path)
            else:
                print("图片正在下载:", image_path)
                urllib.request.urlretrieve(img_url, image_path)
            index += 1


# 漫画id
comic_id = input('请输入你需要下载的漫画ID：')
# 第几章节开始
chapter_num = int(input('请输入开始章节：'))
spider = Spider()
spider.init_spider(comic_id, chapter_num)

# '213887' 琅琊榜
# '208670' 风起苍岚
