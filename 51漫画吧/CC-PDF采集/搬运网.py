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
        'Host': 'www.zerobywswit.com',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        'Cookie': '__cfduid=dfd2b8af05a90dd9077ccf6a9fd2f0cee1608729874; kd5S_2132_saltkey=iX45GG1F; kd5S_2132_lastvisit=1608726274; kd5S_2132_forum_lastvisit=D_103_1608731594D_70_1608731631; kd5S_2132_visitedfid=70D103D46; kd5S_2132_ulastactivity=f4523Bme1ThurQk9ck3n28sumstq127NjzGKkxBzBKjAwZHUMOdI; kd5S_2132_lastcheckfeed=2455716%7C1609163172; kd5S_2132_auth=6539SQSxReTdqYoTJC8rpL6EfogBvXI5De8C2HRUbAssHUNQgzPPq2SpN4aXLTb4Xw%2FfLzBDxDe8ePPB0GdyN0imLDeS; kd5S_2132_tshuz_accountlogin=2455716; kd5S_2132_manhuakaiguan=1; kd5S_2132_manhuamoshi=2; kd5S_2132_manhua_pcadvcookie=10; kd5S_2132_sid=dtb2oO; kd5S_2132_lip=112.97.213.123%2C1609163172; kd5S_2132_lastact=1609164925%09plugin.php%09'
    }
    comic_url = 'http://www.zerobywswit.com/plugin.php?id=jameson_manhua&c=index&a=ku&jindu=1&page={}'
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
        csv_title = ['标题', '封面', '地址', '是否完结', '内容']

        for index in range(1, page_num):
            print(index)
            url = list_url.format(str(index))
            print(url)
            page = self.get_html(url)
            # print(page)
            list_container = page.find('div', {'id': 'jameson_manhua'})
            # print(list_container)
            comic_list = list_container.find_all('div', {'class': 'uk-card mbm uk-text-center'})
            # print(comic_list)
            for comic in comic_list:
                #print(comic)
                # 漫画标题
                comic_title = comic.find('p', {'class': 'mt5 mb5 uk-text-truncate uk-text-center xs2'}).find('a').text
                comic_url = comic.find('p', {'class': 'mt5 mb5 uk-text-truncate uk-text-center xs2'}).find('a')['href']
                comic_isover = '连载中' if '连载' in comic_title else '完结'

                #print(comic_title, comic_url, comic_isover)
                # 漫画封面
                img_tag = comic.find('div', {'class': 'uk-card-media-top uk-inline'}).find('img')
                if img_tag:
                    comic_cover = img_tag['src']
                else:
                    comic_cover = ''
                #print('漫画封面:', comic_cover)
                post_list.append([comic_title, comic_cover, comic_url, comic_isover, ''])

        post_data = pd.DataFrame(columns=csv_title, data=post_list)
        #print(post_data)
        post_data.to_csv(save_path, encoding='utf8')

    def init(self):
        self.save_comic_detail(self.comic_url, 2, '漫画列表.csv')


spider = Spider()
spider.init()

