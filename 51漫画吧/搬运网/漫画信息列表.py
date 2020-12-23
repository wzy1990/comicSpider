# -*- coding: utf-8 -*-
# @Time    : 2020/1/1 11:20
# @Author  : zhiyong_wang
# @Email   : 946455381@qq.com
# @File    : 搬运网.py
# @Software: PyCharm

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


class Spider(object):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    comic_url = 'https://www.mkzhan.com/{}/'
    web_rb = 'https://www.manhuadb.com/manhua/list-r-4-page-{}.html'
    web_xg = 'https://www.manhuadb.com/manhua/list-r-5-page-{}.html'
    web_hg = 'https://www.manhuadb.com/manhua/list-r-6-page-{}.html'
    web_tw = 'https://www.manhuadb.com/manhua/list-r-7-page-{}.html'
    web_nd = 'https://www.manhuadb.com/manhua/list-r-8-page-{}.html'
    web_om = 'https://www.manhuadb.com/manhua/list-r-9-page-{}.html'
    site_url = 'https://www.manhuadb.com'
    comic_save_path = ''
    chapter_save_path = ''

    # 获取网页信息
    def get_html(self, url):
        html = requests.get(url, headers=self.headers)
        html.encoding = html.apparent_encoding  # 'utf8'
        soup = bs(html.text, 'lxml')
        return soup

    def save_comic_detail(self, web_url, comic_type, page_num):
        post_list = []
        csv_title = ['标题', '作者', '漫画分类', '风格类型', '保存格式', '封面', '内容简介', '是否完结', '漫画地址']

        for index in range(1, page_num):
            try:
                url = web_url.format(str(index))
                print(url)
                page = self.get_html(url)
                # print(page)
                list_container = page.find('div', {'class': 'comic-main-section bg-white p-3'})
                # print(list_container)
                comic_list = list_container.find_all('div', {'class': 'media comic-book-unit'})
                # print(comic_list)
                for comic in comic_list:
                    # print(comic)
                    # 漫画封面
                    comic_cover = comic.find('img', {'class': 'mr-3 comic-book-cover'})['src']
                    comic_url = self.site_url + comic.find('a', {'class': 'd-block'})['href']
                    print(comic_cover)
                    # 漫画标题
                    comic_title = comic.find('h2', {'class': 'h3 my-0'}).find('a').text
                    print(comic_title)
                    # 漫画详情
                    comic_content = comic.find('div', {'class': 'comic-story-intro text-justify mt-3'}).text
                    print(comic_content)
                    # 漫画作者
                    author_list = comic.find('div', {'class': 'comic-creators'}).find_all('a')
                    comic_author = []
                    for author in author_list:
                        comic_author.append(author.text)
                    # 漫画完结情况，分类
                    tags_list = comic.find('div', {'class': 'comic-categories'}).find_all('span')
                    comic_tags = []
                    for tag in tags_list:
                        comic_tags.append(tag.text)
                    print(comic_tags)
                    comic_isover = comic_tags[0]
                    print(comic_isover)

                    # 缓存这一条文章的全部信息，以备保存到CSV
                    print(comic_title + "; " + '&'.join(comic_author) + "; " + comic_content + '; ' + comic_isover)
                    post_list.append([comic_title, '&'.join(comic_author), comic_type, ','.join(comic_tags), 'JPG', comic_cover, comic_content, comic_isover, comic_url])
            except:
                pass

        post_data = pd.DataFrame(columns=csv_title, data=post_list)
        post_data.to_csv(comic_type + '列表.csv', encoding='UTF-8')

    def init(self):
        self.save_comic_detail(self.web_tw, '台湾漫画', 2)


spider = Spider()
spider.init()


