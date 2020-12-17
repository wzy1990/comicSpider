import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class Spider(object):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    web_site ='https://bbs.2046acg.com/'
    # browser = webdriver.Chrome()
    comic_save_path = ''
    chapter_save_path = ''

    # # 获取网页信息
    # def get_html(self, url):
    #     # 打开chrome浏览器（需提前安装好chromedriver）
        
    #     # browser = webdriver.PhantomJS()
    #     print("正在打开网页...")
    #     self.browser.get(url)
    #     print("等待网页响应...")
    #     # 需要等一下，直到页面加载完成
    #     wait = WebDriverWait(self.browser, 10)
        
    #     print("正在获取网页数据...")
    #     soup = bs(self.browser.page_source, "lxml")
    #     return soup

        # 获取网页信息
    def get_html(self, url):
        html = requests.get(url, headers=self.headers, timeout=5000)
        html.encoding = html.apparent_encoding  # 'utf8'
        html = html.text
        html = html.encode('gbk', "ignore").decode('gbk')  # 先用gbk编码,忽略掉非法字符,然后再译码
        html = html.encode('utf-8').decode('utf-8')
        soup = bs(html, 'lxml')
        return soup

    def init_spider(self, web_url, save_path, start_page, end_page):
        post_list = []
        csv_title = ['标题', '内容简介', '分类', '标签', '下载链接', '提取码', '解压密码', '来源地址']

        for index in range(start_page, end_page):
            post_list = []
            url = web_url.format(str(index))
            print('正在解析第{}页：'.format(str(index)) + url)
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
                        
                    # 缓存这一条文章的全部信息，以备保存到CSV
                    post_list.append([comic_title, comic_content, '漫画', '', '', '', '', comic_url])

            post_data = pd.DataFrame(columns=csv_title, data=post_list)
            if index == 1:
                post_data.to_csv(save_path, encoding='UTF-8')
            else:
                post_data.to_csv(save_path, mode='a', header=False, encoding='UTF-8')
        
        # self.browser.close()        


spider = Spider()
# spider.init_spider('https://bbs.2046acg.com/forum-37-{}.html', 'ACG次元网_漫画.csv', 1, 123)
spider.init_spider('https://bbs.2046acg.com/forum-39-{}.html', 'ACG次元网_动画.csv', 1, 21)
spider.init_spider('https://bbs.2046acg.com/forum-36-{}.html', 'ACG次元网_游戏.csv', 1, 230)
# spider.init_spider('https://bbs.2046acg.com/forum-48-{}.html', 'ACG次元网_有声本.csv', 1, 123)
