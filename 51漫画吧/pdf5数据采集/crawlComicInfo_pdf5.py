# pip install pandas
import requests
import time
import pandas as pd
from numpy import *
from bs4 import BeautifulSoup as bs

header = {
    'Referer': 'https://www.pdf5.net/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36'
}

# 获取网页信息
def get_html(url):
    html = requests.get(url, headers=header)
    html.encoding = 'utf8'
    soup = bs(html.text, 'lxml')
    return soup

# 判断文件名
def judgeName(name):
    fh = ['?', '\\', '/', '：', '*', '"', '<', '>', '|']
    for fh_ in fh:
        if fh_ in name:
            name = name.replace(fh_, '_')
    return name

# 用于爬取的漫画信息
def CrawModel(url):
    post_list = []
    csv_title = ['标题', '作者', '类型', '是否完结', '下载地址', '密码', '内容', '漫画页地址']

    for page_num in range(1, 3):
        if page_num == 1:
            curl = url.format('')  # 分类的第一页，可以不用构造
        else:
            curl = url.format('/page/' + str(page_num))  # 该分类的其他页，非第一页

        try:  # 第一种URL格式，带有ppt_
            page = get_html(curl)
        except:
            print('error:', curl)
        print(time.ctime() + "; 爬取" + curl + "页")
        # print(page)

        try:
            ul= page.find('div', {'id': 'posts'})
            li = ul.find_all('div', {'class': 'post grid'})
            i_num = 1
            for i in li:
                a = i.find('h3').find('a')
                title = a['title']
                print(time.ctime() + "; 打印第" + str(page_num) + "页第" + str(i_num) + "个漫画: " + title)
                # 漫画详情页地址
                comic_url = a['href']
                # 进入漫画详情页
                comic_html = get_html(comic_url)
                # 漫画标题
                comic_title = title
                # 漫画内容简介
                comic_detail = comic_html.find('div', {'class': 'article-content'})
                comic_detail.style.decompose()
                comic_detail.find('div', {'class': 'erphpdown-box'}).decompose()
                comic_content = comic_detail.prettify()
                # print(comic_content)
                # 缓存这一条文章的全部信息，以备保存到CSV
                post_list.append([comic_title, '', '其他', '完结', '', '', comic_content, comic_url])

                time.sleep(0.4)
                i_num += 1
        except:
            print('异常')

    post_data = pd.DataFrame(columns=csv_title, data=post_list)
    post_data.to_csv('comic_list4.csv', encoding='UTF-8')


def main():
   CrawModel('https://www.pdf5.net/category/manhua{}?c2=10&c3&t')


if __name__ == "__main__":
    main()