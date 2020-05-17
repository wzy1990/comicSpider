# -*- coding: utf-8 -*-
# 下面是xpath爬取方法，可跳过vip验证，直接爬取付费内容（漫客栈的vip）
# @Time    : 2020/1/1 11:20
# @Author  : zhiyong_wang
# @Email   : 946455381@qq.com
# @File    : 漫客栈.py
# @Software: PyCharm

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


class Spider(object):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    web_url = 'http://www.ccdm13.com/List/All/0/32/0/0/0/bid/p/{}/'
    site_url = 'http://www.ccdm13.com'
    comic_save_path = ''
    chapter_save_path = ''

    # 获取网页信息
    def get_html(self, url):
        html = requests.get(url, headers=self.headers, timeout=5000)
        html.encoding = html.apparent_encoding  # 'utf8'
        html = html.text
        html = html.encode('gbk', "ignore").decode('gbk')  # 先用gbk编码,忽略掉非法字符,然后再译码
        html = html.encode('utf-8').decode('utf-8')
        soup = bs(html, 'lxml')
        return soup

    def save_comic_detail(self, web_url, comic_type, page_num):
        post_list = []
        csv_title = ['标题', '作者', '漫画分类', '风格类型', '保存格式', '封面', '内容简介', '是否完结', '漫画地址']

        for index in range(1, page_num):
            post_list = []
            url = web_url.format(str(index))
            print(url)
            page = self.get_html(url)
            # print(page)
            list_container = page.find('ul', {'id': 'contList'})
            # print(list_container)
            comic_list = list_container.find_all('li')
            # print(comic_list)
            for comic in comic_list:
                # print(comic)
                # 漫画封面
                comic_img = comic.find('img')
                print(comic_img)
                print('data-src' in str(comic_img))
                if 'data-src' in str(comic_img):
                    comic_cover = comic_img['data-src']
                else:
                    comic_cover = comic_img['src']
                # 漫画标题
                comic_title = comic.find('a', {'class': 'bcover'})['title']
                print(comic_title)
                # 漫画详情
                comic_content = ''
                # 漫画作者
                author_list = ''
                # 漫画详情页地址
                comic_url = self.site_url + comic.find('a', {'class': 'bcover'})['href']
                # 进入漫画详情页
                try:
                    comic_html = self.get_html(comic_url)
                    # 漫画简介
                    comic_content = comic_html.find('div', {'id': 'intro-all'}).text
                    comic_detail_list = comic_html.find('ul', {'class': 'detail-list cf'}).find_all('li')
                    # 漫画分类
                    span_list0 = comic_detail_list[0].find_all('span')
                    comic_type = span_list0[0].find('a').text
                    # 漫画作者,漫画类型
                    span_list = comic_detail_list[1].find_all('span')
                    authors_list = span_list[1].find_all('a')
                    comic_authors = []
                    for author in authors_list:
                        comic_authors.append(author.text)
                    tags_list = span_list[0].find_all('a')
                    comic_tags = []
                    for tag in tags_list:
                        comic_tags.append(tag.text)
                    # 漫画是否完结
                    over_status = comic_detail_list[2].find_all('span')
                    comic_isover = over_status[1].text
                except:
                    print('访问详情页失败：', comic_url)

                # 缓存这一条文章的全部信息，以备保存到CSV
                # print(comic_title + "; " + '&'.join(comic_authors) + "; " + comic_content + '; ' + comic_isover)
                post_list.append(
                    [comic_title, '&'.join(comic_authors), comic_type, ','.join(comic_tags), 'JPG', comic_cover,
                     comic_content, comic_isover, comic_url])
                print([comic_title, '&'.join(comic_authors), comic_type, ','.join(comic_tags), 'JPG', comic_cover,
                     comic_content, comic_isover, comic_url])

            post_data = pd.DataFrame(columns=csv_title, data=post_list)
            if index == 1:
                post_data.to_csv('高清单行本列表.csv', encoding='UTF-8')
            else:
                post_data.to_csv('高清单行本列表.csv', mode='a', header=False, encoding='UTF-8')

    def init(self):
        self.save_comic_detail(self.web_url, '高清单行本', 15)


spider = Spider()
spider.init()


