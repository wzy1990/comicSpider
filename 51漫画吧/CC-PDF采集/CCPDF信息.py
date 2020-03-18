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
        'Host': 'www.cc-pdf.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Cookie': 'haircki=haircooki; wordpress_logged_in_3fa8395c34e8fd4b9140b2b47cae1015=8069.255.8ccf355f284e41e6b6b9fd7433e49994%7C1584024925%7CZVX6QKbFv58bHCIi2bCwCmrRK9NcIHL1SNcOCVoYAZV%7Cb9623d4234b7fa6e3f0d15ce4fd27edd230afa8d3022a163ad7e8d3f6f618557; wp_xh_session_3fa8395c34e8fd4b9140b2b47cae1015=3924018522b8c7eba5a2b6d56cd4cdea%7C%7C1582987924%7C%7C1582984324%7C%7C3c402bf175411954b8fca9455579e1a5; wp-settings-time-8069=1582815368; PHPSESSID=9490n2pnmeami5nh7nouhklga2'
    }
    comic_url = 'http://www.cc-pdf.com/page/{}'
    web_url = 'http://www.cc-pdf.com'
    comic_root_path = '漫客栈网\\'
    comic_save_path = ''
    chapter_save_path = ''

    # 获取网页信息
    def get_html(self, url):
        html = requests.get(url, headers=self.headers, timeout=50)
        html.encoding = html.apparent_encoding # ☾'utf8'
        soup = bs(html.text, 'lxml')
        return soup

    def save_comic_detail(self, list_url, page_num, save_path):
        post_list = []
        csv_title = ['标题', '作者', '封面', '内容简介', '是否完结', '最新章节']

        for index in range(1, page_num):
            print(index)
            url = list_url.format(str(index))
            print(url)
            page = self.get_html(url)
            # print(page)
            list_container = page.find('div', {'id': 'infinite-post-wrap'})
            # print(list_container)
            comic_list = list_container.find_all('article')
            # print(comic_list)
            for comic in comic_list:
                print('1')
                # 漫画标题
                comic_authon_title = comic.find('h2', {'class': 'entry-title'}).find('a').text.split('–')
                if len(comic_authon_title) > 1:
                    comic_title = comic_authon_title[1]
                    comic_isover = '连载中' if '连载中' in comic_title else '完结'
                    # 漫画作者
                    comic_author = comic_authon_title[0]
                else:
                    break

                print('2')
                # 漫画封面
                img_tag = comic.find('img')
                if img_tag:
                    comic_cover = img_tag['src']
                else:
                    comic_cover = ''
                print('3')
                # 漫画简介
                comic_content = ''
                # 缓存这一条文章的全部信息，以备保存到CSV
                # print(comic_title)
                # print(comic_author)
                # print('4')
                print(comic_isover)
                post_list.append([comic_title, comic_author, comic_cover, comic_content, comic_isover, ''])

        post_data = pd.DataFrame(columns=csv_title, data=post_list)
        print(post_data)
        post_data.to_csv(save_path, encoding='gbk')

    def init(self):
        self.save_comic_detail(self.comic_url, 2, '漫画列表.csv')


spider = Spider()
spider.init()

