# coding:utf-8
# # 发布带有自定义栏目字段的发布文章代码
# pip install python-wordpress-xmlrpc
# pip install xlrd
# import datetime
import csv
import random
import requests
from wordpress_xmlrpc import Client, WordPressPost
# from wordpress_xmlrpc.methods.users import GetUserInfo
from wordpress_xmlrpc.methods import posts
# from wordpress_xmlrpc.methods import taxonomies
# from wordpress_xmlrpc import WordPressTerm
import importlib, sys
import pandas as pd
import xlrd
from datetime import datetime

importlib.reload(sys)

class WpPost(object):
    begin_line = 2 # 第几行开始
    end_line = 100 # 结束行
    step = 1
    comic_path = 'comic_list.csv'
    header = {
        'cookie': 'Hm_lvt_dbc355aef238b6c32b43eacbbf161c3c=1536981553; Hm_lpvt_dbc355aef238b6c32b43eacbbf161c3c=1536986863',
        'referer': 'http://51mhb.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'
    }
    wp = Client('http://51mhb.com/xmlrpc.php', 'admin_wzy', 'wzy19900420wzy')

    # 初始化
    def init_spider(self, begin_line, end_line, step, comic_path):
        self.begin_line = begin_line  # 第几行开始
        self.end_line = end_line  # 结束行
        self.step = step  # 结束行
        self.comic_path = comic_path
        self.getDatas()

    def getDatas(self):
        workbook = xlrd.open_workbook(self.comic_path)
        sheet = workbook.sheet_by_index(0)
        for row in range(self.begin_line, self.end_line, self.step):
            row_data = sheet.row_values(row)
            # print(row_data)
            self.postBlog(row_data)

    def postBlog(self, new_blog):
        print('正在发布：', new_blog[1])
        post = WordPressPost()
        kuohao = '【{}】'
        post.title = new_blog[1] + kuohao.format(new_blog[2]) + kuohao.format(new_blog[8])
        post.post_status = 'publish'  # 文章状态，不写默认是草稿，private表示私密的，draft表示草稿，publish表示发布
        comic_cover = '<img src="' + new_blog[6] + '" alt="" class="aligncenter size-full wp-image-154" />'
        post.content = comic_cover + '<h5>漫画简介：</h5><blockquote style="text-indent: 30px;">' + new_blog[7] + '</blockquote>'

        serial_status = '精彩连载,' if '连载' in new_blog[5] else '经典完结,'
        categorys = serial_status + new_blog[3]
        post.terms_names = {
            'post_tag': new_blog[4].split(','),  # 文章所属标签，没有则自动创建
            'category': categorys.split(',') + new_blog[5].split('+') # 文章所属分类，没有则自动创建
        }

        post.custom_fields = []  # 自定义字段列表
        # 资源价格
        price = int(new_blog[11]) * 10 if new_blog[11] else 2 * 10
        post.custom_fields.append({'key': 'cao_price', 'value': price})
        # VIP折扣
        post.custom_fields.append({'key': 'cao_vip_rate', 'value': 0})
        # 仅限永久VIP免费
        post.custom_fields.append({'key': 'cao_is_boosvip', 'value': 0})
        # 启用付费下载资源 
        post.custom_fields.append({'key': 'cao_status', 'value': 1})
        post.custom_fields.append({'key': 'wppay_type', 'value': 4})
        # 资源下载地址
        post.custom_fields.append({'key': 'cao_downurl', 'value': new_blog[9]})
        # 资源下载密码
        post.custom_fields.append({'key': 'cao_pwd', 'value': new_blog[10]})
        # 资源下载次数
        post.custom_fields.append({'key': 'cao_paynum', 'value': random.randint(1, 50)})
        post.custom_fields.append({  # 资源其他信息
            'key': 'cao_info',
            'value': [{
                'title': '作   者',
                'desc': new_blog[2]
            }, {
                'title': '题材类型',
                'desc': new_blog[4]
            }, {
                'title': '是否完结',
                'desc': new_blog[8]
            }]
        })
        try:
            self.wp.call(posts.NewPost(post))
            print('发布成功：', new_blog[1])
        except:
            print('发布失败：', new_blog[1])
            pass

    def updateBlog(self, begin, end, comic_path):
        # 必须添加header=None，否则默认把第一行数据处理成列名导致缺失
        data = pd.read_csv(self.comic_path, encoding='gbk', header=None)
        csv_reader_lines = data.values.tolist()
        print(csv_reader_lines[0])
        for index in range(begin, end):
            post = WordPressPost()
            blog = csv_reader_lines[index]
            post.title = blog[1]
            post.custom_fields = {
                'cao_downurl': blog[5]
            }  # 自定义字段列表
            print(blog[1])
            print(blog[5])
            print(int(blog[0]))
            # post.post_status = 'publish'
            self.wp.call(posts.EditPost(int(blog[0]), post))


startTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print('开始时间：', startTime)
wpPost = WpPost()

start_num = int(input('请输入开始行数：'))
end_num = int(input('请输入结束行数：'))

wpPost.init_spider(start_num, end_num, 1, 'D:\python_spider\\51漫画吧\\完结漫画列表.xlsx')
# wpPost.updateBlog(1, 2, 'comic_list.csv')
endTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print('结束时间：', endTime)
print("##################全部下载完成!##################")