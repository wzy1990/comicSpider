# 带有自定义栏目字段的发布文章代码
# pip install python-wordpress-xmlrpc
# coding:utf-8
import datetime
import csv
import pypinyin
import random
import requests
from bs4 import BeautifulSoup as bs
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.methods import posts, media
from wordpress_xmlrpc.methods import taxonomies
from wordpress_xmlrpc import WordPressTerm
from wordpress_xmlrpc.compat import xmlrpc_client
import importlib, sys
import pandas as pd
from datetime import datetime

importlib.reload(sys)

class WpPost(object):
    homepath = 'G:\\comic资源'
    leimu = '港台漫画'
    begin_line = 2 # 第几行开始
    end_line = 100 # 结束行
    step = 1
    csv_title = ['文章ID', '标题', '作者', '封面', '内容简介', '是否完结', '最新章节', '漫画页地址']
    header = {
        'cookie': 'Hm_lvt_dbc355aef238b6c32b43eacbbf161c3c=1536981553; Hm_lpvt_dbc355aef238b6c32b43eacbbf161c3c=1536986863',
        'referer': 'https://www.dm5.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'
    }
    wp = Client('http://47.112.130.142/xmlrpc.php', 'admin_wzy', 'admin_wzy19900420')

    # 不带声调的(style=pypinyin.NORMAL)
    def pinyin(self, word):
        pin_yin = ''
        print(self.pinyin(word))
        for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
            pin_yin += ''.join(i)
        return pin_yin

    # 初始化
    def init_spider(self, leimu, begin_line, end_line, step):
        self.leimu = leimu
        self.begin_line = begin_line  # 第几行开始
        self.end_line = end_line  # 结束行
        self.step = step  # 结束行
        self.getDatas2()

    # 获取网页信息
    def get_html(self, url):
        html = requests.get(url, headers=self.header)
        html.encoding = 'utf8'
        soup = bs(html.text, 'lxml')
        return soup

    def getDatas(self):
        with open(self.homepath + '\\' + self.leimu + '\\漫画信息表.csv', 'r', encoding='gbk') as csv_file:
            csv_reader_lines = csv.reader(csv_file)
            index = 1
            for new_blog in csv_reader_lines:
                print(new_blog)
                if self.begin_line <= index <= self.end_line:
                    self.postBlog(new_blog)
                index += 1
            self.saveData()
    def getDatas2(self):
        data = pd.read_csv(self.homepath + '\\' + self.leimu + '\\漫画信息表.csv', encoding='gbk', header=None)
        # 必须添加header=None，否则默认把第一行数据处理成列名导致缺失
        csv_reader_lines = data.values.tolist()
        for index in range(self.begin_line, self.end_line, self.step):
            self.postBlog(csv_reader_lines[index])

    def postBlog(self, new_blog):
        post = WordPressPost()
        # post.post_ID = new_blog[0]
        # post.id = new_blog[0]
        post.title = new_blog[1]
        post.post_status = 'publish'  # 文章状态，不写默认是草稿，private表示私密的，draft表示草稿，publish表示发布

        comic_type = '热血'
        # 漫画封面
        comic_cover = '<img src="'+ new_blog[3] + '" alt="" class="aligncenter size-full wp-image-154" />'

        try:
            # 进入漫画详情页
            comic_html = self.get_html(new_blog[7])
            # 漫画详情信息区域
            comic_detail = comic_html.find('div', {'class': 'banner_detail_form'})

            # 漫画内容简介
            comic_content = comic_detail.find('p', {'class': 'content'}).text
            post.content = '<blockquote style="text-indent: 30px;">' + comic_content.replace('\u3000', '').replace('\xa0', '').replace('[+展开]', '').replace('[-折叠]', '') + '</blockquote>' + comic_cover
            # 连载状态，及分类
            comic_info_list = comic_detail.find_all('span', {'class': 'block'})
            if comic_info_list[1].find('span') != None:
                comic_type = comic_info_list[1].find('span').text
            else:
                comic_type = '其他'
            post.terms_names = {
                'post_tag': [comic_type],  # 文章所属标签，没有则自动创建
                'category': [self.leimu]  # 文章所属分类，没有则自动创建
            }
        except:
            post.content = '<blockquote style="text-indent: 30px;">' + new_blog[4].replace('\u3000', '').replace('\xa0', '').replace('[+展开]', '').replace('[-折叠]', '') + '</blockquote>' + comic_cover
            post.terms_names = {
                'post_tag': [comic_type],  # 文章所属标签，没有则自动创建
                'category': [self.leimu]  # 文章所属分类，没有则自动创建
            }

        post.custom_fields = []  # 自定义字段列表
        # 资源价格
        post.custom_fields.append({'key': 'cao_price', 'value': 1})
        # VIP折扣
        post.custom_fields.append({'key': 'cao_vip_rate', 'value': 0})
        # 仅限永久VIP免费
        post.custom_fields.append({'key': 'cao_is_boosvip', 'value': 0})
        # 启用付费下载资源
        post.custom_fields.append({'key': 'cao_status', 'value': 1})
        post.custom_fields.append({  # 资源类型
            'key': 'wppay_type',
            'value': 4
        })
        post.custom_fields.append({  # 资源下载地址
            'key': 'cao_downurl',
            'value': [{
                'name': '立即下载',
                'url': '#'
            }]
        })
        # 资源下载次数
        post.custom_fields.append({ 'key': 'cao_paynum', 'value': random.randint(20, 100) })
        # 资源下载密码
        post.custom_fields.append({ 'key': 'cao_pwd', 'value': '51zyb' })
        # 自定义按钮
        post.custom_fields.append({ 'key': 'cao_diy_btn', 'value': '查看更多资源|https://www.51zyb.com/' })
        post.custom_fields.append({  # 资源其他信息
            'key': 'cao_info',
            'value': [{
                'title': '作   者',
                'desc': new_blog[2]
            }, {
                'title': '题材类型',
                'desc': comic_type
            }, {
                'title': '最近更新',
                'desc': new_blog[6]
            }, {
                'title': '是否完结',
                'desc': new_blog[5]
            }]
        })
        try:
            new_blog[0] = self.wp.call(posts.NewPost(post))
            self.saveData(new_blog)
        except:
            pass

    def saveData(self, blog):
        with open(self.homepath + '\\' + self.leimu + '\\漫画信息表.txt', 'a', encoding='utf8') as f:
            line_content = ';;'.join((str(x) for x in blog))
            # print(line_content)
            f.write(line_content + '\n')

    # 新建标签
    # tag = WordPressTerm()
    # tag.taxonomy = 'post_tag'
    # tag.name = 'My New Tag12'  # 标签名称
    # tag.slug = 'bieming12'  # 标签别名，可以忽略
    # tag.id = wp.call(taxonomies.NewTerm(tag))  # 返回的id
    #
    # # 新建分类
    # cat = WordPressTerm()
    # cat.taxonomy = 'category'
    # cat.name = 'cat1'  # 分类名称
    # cat.slug = 'bieming2'  # 分类别名，可以忽略
    # cat.id = wp.call(taxonomies.NewTerm(cat))  # 新建分类返回的id

startTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print('开始时间：', startTime)
wpPost = WpPost()
# wpPost.init_spider('港台漫画', 500, 400, -1) # 1
# wpPost.init_spider('欧美漫画', 1770, 1700, -1) # 1
# wpPost.init_spider('日韩漫画', 5200, 5100, -1) # 1
wpPost.init_spider('大陆漫画', 1434, 1400, -1) # 1
endTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print('结束时间：', endTime)
print("##################全部下载完成!##################")