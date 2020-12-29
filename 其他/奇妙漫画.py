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
from pathlib import Path
import os
import json

class Spider(object):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    web_url = 'https://m.qimiaomh.com'
    comic_save_path = ''
    chapter_save_path = ''

    def init_spider(self, url):

        r = requests.get(url, headers=self.headers, timeout=50)
        # r.encoding = r.apparent_encoding
        r.raise_for_status()
        html = r.text
        html = html.encode('gbk', "ignore").decode('gbk')  # 先用gbk编码,忽略掉非法字符,然后再译码
        html = html.encode('utf-8').decode('utf-8')
        ret = etree.HTML(html)
        title_list = ret.xpath('//div[@class="ncp1b_div ncp1b_tit"]/h1')
        comic_title = title_list[0].text
        print(comic_title)
        self.comic_save_path = "comic\\奇妙漫画\\" + comic_title
        path = Path(self.comic_save_path)
        if path.exists():
            pass
        else:
            path.mkdir()

        chapterLinks = ret.xpath('//ul[@id="ncp3_ul"]/li/a/@href')
        chapterTitles = ret.xpath('//ul[@id="ncp3_ul"]/li/a/div/text()')
        print(chapterLinks)
        print(chapterTitles)
        self.chapter_request(chapterLinks, chapterTitles)

    # 遍历章节列表
    def chapter_request(self, chapterLinks, chapterTitles):
        for link, title in zip(chapterLinks, chapterTitles):
            print(title, link)
            self.chapter_save_path = self.comic_save_path + '\\' + title
            path = Path(self.chapter_save_path)
            if path.exists():
                pass
            else:
                path.mkdir()
            try:
                link = link.replace('/manhua/', '').split('/')
                url = 'https://m.qimiaomh.com/Action/Play/AjaxLoadImgUrl?did=' + link[0] + '&sid=' + link[1].replace('.html', '') + '&tmp=0.5955032991116953'
                response = requests.post(url=url, headers=self.headers)
                print(response.url)
                print(response.text)
                image_list = json.loads(response.text)['listImg']
                self.download_image(image_list)
            except Exception as e:
                print(e)

    # 3. 下载章节的图片
    def download_image(self, image_list):
        for img_url in image_list:
            img_name = img_url.replace('https://mh1.88bada.com/upload/', '').split('/')[2]
            image_path = self.chapter_save_path + '\\' + img_name

            if os.path.isfile(image_path):
                print("此图已经存在:", image_path)
            else:
                print("图片正在下载:", image_path)
                try:
                    urllib.request.urlretrieve(img_url, image_path)
                except:
                    pass


url = 'https://m.qimiaomh.com/manhua/2978.html'
spider = Spider()
spider.init_spider(url)