# -*- coding: utf-8 -*-
# 下面是xpath爬取方法，可跳过vip验证，直接爬取付费内容
# @Time    : 2020/1/6 11:20
# @Author  : zhiyong_wang
# @Email   : 946455381@qq.com
# @File    : 阅漫网.py
# @Software: PyCharm
# pip install requests
# pip install lxml
# pip install pandas

import requests
import urllib.request
from lxml import etree
from pathlib import Path
import pandas as pd
import os
import json


class Spider(object):
    headers = {
        'Content-Type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    get_filter_data = 'http://dlmh02.com/api/app/get_filter_data'
    get_detail_url = 'http://dlmh02.com/api/cartoon/get_detail'
    comic_root_path = "comic\\韩漫完结\\"
    comic_save_path = ''
    chapter_save_path = ''

    # 1. 查询漫画信息，章节列表
    def comic_request(self, comic_id):
        post_data = {
            'id': comic_id,
            'uid': 3484998
        }
        response = requests.post(url=self.get_detail_url, data=json.dumps(post_data), headers=self.headers)
        response_data = json.loads(response.text)['data']
        comic_title = response_data['data']['name']
        print(response_data)
        print(comic_title)
        self.comic_save_path = self.comic_root_path + comic_title
        path = Path(self.comic_save_path)
        if path.exists():
            pass
        else:
            path.mkdir()

        chapter_list = response_data['chapters']
        self.chapter_request(chapter_list)

    # 2. 遍历章节列表
    def chapter_request(self, chapter_list):
        for chapter in chapter_list:
            print('\n当前章节信息：', chapter)
            self.chapter_save_path = self.comic_save_path + '\\' + chapter['title'].replace('?', '？')
            path = Path(self.chapter_save_path)
            if path.exists():
                pass
            else:
                path.mkdir()
            try:
                chapter_url = 'http://dlmh02.com/chapter/' + str(chapter['id'] )
                print('当前章节URL：', chapter_url)
                response = requests.get(chapter_url, headers=self.headers, timeout=50)
                response.encoding = response.apparent_encoding
                html = response.text
                html = html.encode('gbk', "ignore").decode('gbk')  # 先用gbk编码,忽略掉非法字符,然后再译码
                html = html.encode('utf-8').decode('utf-8')
                html = etree.HTML(html)
                image_list = html.xpath('//div[@class="container"]/img/@src')
                self.download_image(image_list)
            except Exception as e:
                print(e)

    # 3. 下载章节的图片
    def download_image(self, image_list):
        index = 1
        print(image_list)
        for img_url in image_list:
            image_path = self.chapter_save_path + '\\' + str(index) + '.jpg'

            if os.path.isfile(image_path):
                print("此图已经存在:", image_path)
            else:
                try:
                    pic_data = requests.get(img_url, headers=self.headers, timeout=50)
                    with open(image_path, 'wb') as f:
                        f.write(pic_data.content)
                    # urllib.request.urlretrieve(img_url, image_path)
                    print("图片下载成功:", image_path)
                except:
                    print("图片下载失败:", image_path)
                    pass
            index += 1

    def get_comic_info(self):
        begin_line = 0
        end_line = 10
        self.comic_root_path = "comic\\韩漫连载\\"
        data = pd.read_csv('comic\\韩漫连载.csv', encoding='utf8', header=None)
        # 必须添加header=None，否则默认把第一行数据处理成列名导致缺失
        csv_reader_lines = data.values.tolist()
        print(csv_reader_lines)
        for index in range(begin_line, end_line, 1):
            print(csv_reader_lines[index][1])
            self.comic_request(csv_reader_lines[index][0])

    def save_comic_list(self, comic_list, csv_path):
        # id:100
        # image:"cosplay-cover/d3f0201b3f985e65495ee6b0e650f704.jpg"
        # images_count:185
        # name:"Your sweet Angel"
        # resource_type:5
        csv_title = ['漫画ID', '标题', '作者', '封面', '内容简介', '是否完结', '最新章节', '题材类型', '关键字', '评分']
        data_list = []
        for comic in comic_list:
            comic_isover = '连载中' if comic['serialize'] == 1 else '已完结'
            data_list.append([comic['id'], comic['name'], comic['auther'], comic['image'], comic['desc'], comic_isover,
                              comic['last_chapter_title'], comic['ticai'], comic['tags'], comic['pingfen']])
        post_data = pd.DataFrame(columns=csv_title, data=data_list)
        post_data.to_csv(csv_path, index=False, header=False, mode='a+', encoding='UTF-8')

    def init_spider(self):
        post_data = {
            'page': 1,
            'size': 10,
            'filter': '1,1,0'
        }
        for index in range(1, 100):
            post_data['page'] = index
            try:
                response = requests.post(url=self.get_filter_data, data=json.dumps(post_data), headers=self.headers)
                response_data = json.loads(response.text)['data']
                comic_list = response_data['data']
                print(response_data)
                print(comic_list)
                if len(comic_list) > 0:
                    csv_path = 'comic\\韩漫连载.csv'
                    self.save_comic_list(comic_list, csv_path)
                else:
                    break
            except:
                pass


spider = Spider()
# spider.comic_request(900)
# spider.get_comic_info()
spider.init_spider()



