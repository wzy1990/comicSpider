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
    comic_url = 'https://www.mkzhan.com/{}/'
    url_over = 'https://www.mkzhan.com/category/?finish=2&page={}'  # 已完结的
    url_serialize = 'https://www.mkzhan.com/category/?finish=1&page={}'  # 连载中
    web_url = 'https://www.mkzhan.com'
    comic_root_path = '漫客栈网\\'
    comic_save_path = ''
    chapter_save_path = ''

    # 获取网页信息
    def get_html(self, url):
        html = requests.get(url, headers=self.headers)
        html.encoding = html.apparent_encoding # ☾'utf8'
        soup = bs(html.text, 'lxml')
        return soup

    def save_comic_detail(self, list_url, page_num, save_path):
        post_list = []
        csv_title = ['漫画ID', '标题', '作者', '封面', '内容简介', '是否完结', '最新章节']

        for index in range(1, page_num):
            try:
                url = list_url.format(str(index))
                page = self.get_html(url)
                list_container = page.find('div', {'class': 'cate-comic-list clearfix'})
                comic_list = list_container.find_all('div', {'class': 'common-comic-item'})
                for comic in comic_list:
                    # print(comic)
                    # 漫画封面
                    comic_cover = comic.find('img', {'class': 'lazy'})['data-src']
                    # 漫画标题
                    comic_title = comic.find('p', {'class': 'comic__title'}).find('a').text
                    comic_currChapter = comic.find('a', {'class': 'hl'}).text
                    comic_isover = '完结' if list_url == self.url_over else '连载中'
                    # 漫画详情页地址
                    href = comic.find('p', {'class': 'comic__title'}).find('a')['href']
                    comic_id = href.replace('/', '')
                    comic_url = self.web_url + href
                    try:
                        comic_html = self.get_html(comic_url)
                        # 漫画详情信息区域
                        comic_detail = comic_html.find('div', {'class': 'de-info__box'})
                        # 漫画作者
                        comic_author = comic_detail.find('span', {'class': 'name'}).find('a').text
                        # 漫画简介
                        comic_content = comic_detail.find('p', {'class': 'intro'}).text
                    except:
                        comic_author = ''
                        comic_content = ''
                    # 缓存这一条文章的全部信息，以备保存到CSV
                    print(comic_id + "; " + comic_title + "; " + comic_author + "; " + comic_content + '; ' + comic_isover + "; " + comic_currChapter)
                    post_list.append([comic_id, comic_title, comic_author, comic_cover, comic_content, comic_isover, comic_currChapter])
            except:
                pass

        post_data = pd.DataFrame(columns=csv_title, data=post_list)
        post_data.to_csv(save_path, encoding='UTF-8')

    def init(self):
        self.save_comic_detail(self.url_over, 50, '完结漫画列表.csv')
        self.save_comic_detail(self.url_serialize, 50, '连载漫画列表.csv')

spider = Spider()
spider.init()
# # 漫画id
# comic_id = input('请输入你需要下载的漫画ID：')
# # 第几章节开始
# chapter_num = int(input('请输入开始章节：'))
# spider.comic_request('211692', 521)
# spider.comic_request('210839', 240)
# comic_list = [210839]
# spider.download_comic_list(comic_list)
# '49733' 斗破苍穹
# '209107' 武动乾坤
# '211692' 斗罗大陆2绝世唐门
# ‘210839’ 斗罗大陆3龙王传说

