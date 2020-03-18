# -*- coding: utf-8 -*-
# 下面是xpath爬取方法，可跳过vip验证，直接爬取付费内容（漫客栈的vip）
# @Time    : 2020/1/1 11:20
# @Author  : zhiyong_wang
# @Email   : 946455381@qq.com
# @File    : 漫客栈.py
# @Software: PyCharm

import requests
from bs4 import BeautifulSoup as bs
import json
import time
import pandas as pd


class Spider(object):
    headers = {
        'user-agent': 'Mozilla/5.2 (Windows NT 10.0; WOW64) AppleWebKit/539.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    web_url = 'http://sacg.dmzj.com/mh/index.php?c=category&m=doSearch&status=2310&reader_group=0&zone=0&initial=all&type=0&p={}&callback=search.renderResult'
    web_rb = 'http://sacg.dmzj.com/mh/index.php?c=category&m=doSearch&status=2310&reader_group=0&zone=2304&initial=all&type=0&p={}&callback=search.renderResult'
    web_hg = 'http://sacg.dmzj.com/mh/index.php?c=category&m=doSearch&status=2310&reader_group=0&zone=2305&initial=all&type=0&p={}&callback=search.renderResult'
    web_om = 'http://sacg.dmzj.com/mh/index.php?c=category&m=doSearch&status=2310&reader_group=0&zone=2306&initial=all&type=0&p={}&callback=search.renderResult'
    web_gt = 'http://sacg.dmzj.com/mh/index.php?c=category&m=doSearch&status=2310&reader_group=0&zone=2307&initial=all&type=0&p={}&callback=search.renderResult'
    web_nd = 'http://sacg.dmzj.com/mh/index.php?c=category&m=doSearch&status=2310&reader_group=0&zone=2308&initial=all&type=0&p={}&callback=search.renderResult'
    web_qt = 'http://sacg.dmzj.com/mh/index.php?c=category&m=doSearch&status=2310&reader_group=0&zone=8435&initial=all&type=0&p={}&callback=search.renderResult'

    comic_json = 'https://v3api.dmzj.com/comic/comic_{}.json'
    site_url = 'https://manhua.dmzj.com'
    comic_save_path = ''
    chapter_save_path = ''

    # 获取网页信息
    def get_html(self, url):
        html = requests.get(url, headers=self.headers, timeout=50)
        html.encoding = html.apparent_encoding  # 'utf8'
        html = html.text
        html = html.encode('gbk', "ignore").decode('gbk')  # 先用gbk编码,忽略掉非法字符,然后再译码
        html = html.encode('utf-8').decode('utf-8')
        soup = bs(html, 'lxml')
        return soup

    def save_comic_detail(self, web_url, comic_type, page_num):
        csv_title = ['标题', '作者', '漫画分类', '风格类型', '保存格式', '封面', '内容简介', '是否完结']

        for index in range(10, page_num):
            post_list = []
            print('爬取第 {} 页数据：'.format(str(index)))
            url = web_url.format(str(index))
            response = requests.get(url, headers=self.headers, timeout=50)
            # print(response.text)
            response_data = response.text.replace('search.renderResult(', '').replace(');', '')
            response_json = json.loads(response_data)
            # print(response_json)
            if response_json['status'] == 'OK':
                comic_list = response_json['result']
                # print(comic_list)
                for comic in comic_list:
                    # print(comic)
                    # 漫画封面
                    comic_cover = 'http:' + comic['comic_cover']
                    # 漫画标题
                    comic_title = comic['name']
                    # print(comic_title)
                    comic_authors = comic['author']
                    comic_tags = comic['type'].replace('/', ',')
                    # 漫画是否完结
                    comic_isover = '已完结' if '完' in comic['status'] else '连载中'
                    last_chapter = comic['last_chapter']
                    # 漫画详情
                    comic_content = ''
                    # 进入漫画详情页
                    try:
                        url = self.comic_json.format(comic['id'])
                        response2 = requests.get(url, headers=self.headers, timeout=500)
                        response_json2 = json.loads(response2.text)
                        # print(response2.text)
                        comic_content = response_json2['description']
                        # print(comic_content)

                    except:
                        print('访问详情页失败：', url)

                    # 缓存这一条文章的全部信息，以备保存到CSV
                    # print(comic_title + "; " + '&'.join(comic_authors) + "; " + comic_content + '; ' + comic_isover)
                    post_list.append(
                        [comic_title, comic_authors, comic_type, comic_tags, 'JPG', comic_cover,
                         comic_content, comic_isover])
                    # print([comic_title, comic_type, comic_tags, 'JPG', comic_cover])
                    time.sleep(0.4)
            post_data = pd.DataFrame(columns=csv_title, data=post_list)
            if index == 1:
                post_data.to_csv(comic_type + '列表.csv', encoding='UTF-8')
            else:
                post_data.to_csv(comic_type + '列表.csv', mode='a', header=False, encoding='UTF-8')

    def init(self):
        # self.save_comic_detail(self.web_nd, '内地漫画', 26)
        # self.save_comic_detail(self.web_om, '欧美漫画', 43)
        self.save_comic_detail(self.web_rb, '日本漫画', 489)


spider = Spider()
spider.init()


