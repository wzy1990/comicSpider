# -*- coding: utf-8 -*-
# @Time    : 2020/12/28 11:20
# @Author  : zhiyong_wang
# @Email   : 946455381@qq.com
# @File    : 搬运网.py
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
    comic_url2 = 'http://www.zerobywswit.com/plugin.php?id=jameson_manhua&c=index&a=ku&category_id=1&jindu=1&page={}'          
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
        csv_title = ['标题', '作者', '封面', '标签', '是否完结', '内容简介', '章节列表', '详情地址']

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
                # 标题
                comic_title = comic.find('p', {'class': 'mt5 mb5 uk-text-truncate uk-text-center xs2'}).find('a').text
                comic_url = comic.find('p', {'class': 'mt5 mb5 uk-text-truncate uk-text-center xs2'}).find('a')['href']
                comic_url = comic_url.replace('./', 'http://www.zerobywswit.com/')
                comic_isover = '连载中' if '连载' in comic_title else '完结'
                comic_author = ''
                #print(comic_title, comic_url, comic_isover)

                # 漫画封面
                img_tag = comic.find('div', {'class': 'uk-card-media-top uk-inline'}).find('img')
                if img_tag:
                    comic_cover = img_tag['src']
                else:
                    comic_cover = ''
                
                tags_list = []
                comic_capter_list = []
                comic_content = ''
                try:
                    print(comic_url)
                    # 获取详情页信息
                    detail_page = self.get_html(comic_url)
                    # 简介
                    comic_content = detail_page.find('div', {'class': 'uk-alert xs2 mt5 mb5 pt5 pb5'}).text
                    # 章节列表
                    comic_capter_list = []
                    comic_capters = detail_page.find_all('div', {'class': 'muludiv'})
                    for capter in comic_capters:
                        capter_url = capter.find('a')['href'].replace('./', 'http://www.zerobywswit.com/')
                        print(capter_url)
                        comic_capter_list.append(capter_url)
                    # 标签列表
                    tags_html = []
                    tags_html.extend(detail_page.find_all('a', {'class': 'uk-label uk-label-border mbn'})) 
                    tags_html.extend(detail_page.find_all('span', {'class': 'uk-label uk-label-border uk-label-success mbn'}))
                    for tags in tags_html:
                        if '作者' in tags.text:
                            comic_author = tags.text
                        else:
                            tags_list.append(tags.text)
                    print('tags:', ','.join(tags_list))
                except:
                    pass
                print(','.join(comic_capter_list))
                post_list.append([comic_title, comic_author, comic_cover, ','.join(tags_list), comic_isover, comic_content, ','.join(comic_capter_list), comic_url])

        post_data = pd.DataFrame(columns=csv_title, data=post_list)
        #print(post_data)
        post_data.to_csv(save_path, encoding='utf8')

    def init(self):
        self.save_comic_detail(self.comic_url, 72, 'comic_list.csv')


spider = Spider()
spider.init()

