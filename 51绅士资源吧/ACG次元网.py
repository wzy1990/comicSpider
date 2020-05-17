import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


class Spider(object):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    web_site ='https://bbs2.ongacg.com/'
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

    def init_spider(self, web_url, page_num):
        post_list = []
        csv_title = ['标题', '内容简介', '下载链接', '提取码', '解压密码']

        for index in range(22, page_num):
            post_list = []
            url = web_url.format(str(index))
            print(url)
            page = self.get_html(url)
            # print(page)
            list_container = page.find('table', {'id': 'threadlisttableid'})
            # print(list_container)
            comic_list = list_container.find_all('tbody')
            # print(comic_list)
            for comic in comic_list:
                # print(comic)
                comic_info = comic.find('a', {'class': 's xst'})
                if comic_info:
                    # 漫画标题
                    comic_title = comic_info.text
                    print(comic_title)
                    # 漫画详情
                    comic_content = ''
                    # # 漫画作者
                    # author_list = ''
                    # # 漫画详情页地址
                    comic_url = self.web_site + comic_info['href']
                    comic_html = self.get_html(comic_url)
                    # 漫画简介
                    comic_content = comic_html.find('td', {'class': 't_f'})

                    # 缓存这一条文章的全部信息，以备保存到CSV
                    post_list.append([comic_title, comic_content, '', '', ''])

            post_data = pd.DataFrame(columns=csv_title, data=post_list)
            if index == 1:
                post_data.to_csv('ACG次元网列表2.csv', encoding='UTF-8')
            else:
                post_data.to_csv('ACG次元网列表2.csv', mode='a', header=False, encoding='UTF-8')



url = 'https://bbs2.ongacg.com/forum-37-{}.html'
spider = Spider()
spider.init_spider(url, 97)
