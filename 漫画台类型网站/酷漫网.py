# -*- coding: utf-8 -*-
# @Time    : 2019/6/11 9:47
# @Author  : wujf
# @Email   : 1028540310@qq.com
# @File    : 斗罗大陆2.py
# @Software: PyCharm

'''   Beatifulsoup爬取方式        '''
import requests
import urllib.request
from lxml import etree
import urllib.request
from pathlib import Path

class Spider(object):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    web_url = 'http://www.kuman.com'
    comic_save_path = ''
    chapter_save_path = ''

    def init_spider(self, url):

        r = requests.get(url, headers=self.headers, timeout=5)
        r.encoding = 'utf-8'
        # r.raise_for_status()
        html = r.text
        # html = html.encode('gbk', "ignore").decode('gbk')  # 先用gbk编码,忽略掉非法字符,然后再译码
        # html = html.encode('utf-8').decode('utf-8')
        ret = etree.HTML(html)
        title_list = ret.xpath('//header[@class="cartoon-header-box"]/h3')
        print(title_list[0].text)
        comic_title = title_list[0].text
        self.comic_save_path = "comic\\" + comic_title
        print(self.comic_save_path)
        path = Path(self.comic_save_path)
        if path.exists():
            pass
        else:
            path.mkdir()
        chapterLinks = ret.xpath('//div[@class="chapter-list"]/a/@href')
        print(chapterLinks)
        self.chapter_request(chapterLinks)

    # 遍历章节列表
    def chapter_request(self, chapterLinks):
        for link in chapterLinks:
            link = self.web_url + link
            print(link)
            try:
                t = requests.get(link)
                parse = t.text
                print(parse)
                parse = parse.encode('gbk', "ignore").decode('gbk')  # 先用gbk编码,忽略掉非法字符,然后再译码
                parse = parse.encode('utf-8').decode('utf-8')
                # print(parse)
                treee = etree.HTML(parse)

                chapter_title = treee.xpath('//h4[@class="chapter-title"]/span/text()')
                print(chapter_title[0])
                self.chapter_save_path = self.comic_save_path + '\\' + chapter_title[0]
                path = Path(self.chapter_save_path)
                if path.exists():
                    pass
                else:
                    path.mkdir()
                image = treee.xpath('//ul[@class="pic-list"]/li/div[@class="chapter-img-box"]/img')
                print(etree.tostring(image[0]))
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

url = 'http://www.kuman.com/cartoon/7119'
spider = Spider()
spider.init_spider(url)