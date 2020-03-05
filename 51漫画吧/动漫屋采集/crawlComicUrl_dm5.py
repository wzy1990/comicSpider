# 爬取动漫屋https://www.dm5.com/
# 通过TXT里设置好的分类及对应URL遍历
# 首先爬取类别链接并创建大类文件夹
# pip install beautifulSoup4
# pip install pandas
import requests
import os
import time
import pandas as pd

from numpy import *
from bs4 import BeautifulSoup as bs

URL = 'https://www.dm5.com'
save_path = 'comic资源/'
header = {
    'Referer': 'https://www.dm5.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36'
}
DATA_LIST = [{'directory': '欧美漫画_连载', 'url': 'https://www.dm5.com/manhua-list-area52-st1'}]
# {'directory': '港台漫画_完结', 'url': 'https://www.dm5.com/manhua-list-area35-st2' }, {
# 'directory': '日韩漫画_完结', 'url': 'https://www.dm5.com/manhua-list-area36-st2'}, {
# 'directory': '大陆漫画_完结', 'url': 'https://www.dm5.com/manhua-list-area37-st2'}, {
# 'directory': '欧美漫画_完结', 'url': 'https://www.dm5.com/manhua-list-area52-st2'}, {
# 'directory': '港台漫画_连载', 'url': 'https://www.dm5.com/manhua-list-area35-st1' }, {
# 'directory': '日韩漫画_连载', 'url': 'https://www.dm5.com/manhua-list-area36-st1'}, {
# 'directory': '大陆漫画_连载', 'url': 'https://www.dm5.com/manhua-list-area37-st1'}, {
# 'directory': '欧美漫画_连载', 'url': 'https://www.dm5.com/manhua-list-area52-st1'}


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

# 用于爬取每个类目下的漫画信息
def CrawModel(new_path, url):
    post_list = []
    csv_title = ['标题', '作者', '封面', '内容简介', '是否完结', '最新章节', '漫画页地址']
    page_num = 1
    flag = True  # 控制跳出循环
    while flag:
        if page_num == 1:
            curl = url  # 分类的第一页，可以不用构造
        else:
            curl = url + '-p' + str(page_num) # 该分类的其他页，非第一页

        try:  # 第一种URL格式，带有ppt_
            print(curl)
            page = get_html(curl)
            ul = page.find('ul', {'class': 'mh-list'})
            li = ul.find_all('li')
            list_len = len(ul.find_all('li'))
            print(list_len)
            if list_len > 0:
                for i in li:
                    # 漫画封面
                    comic_cover = i.find('p', {'class': 'mh-cover'})['style'].split('url(')[1].split(')')[0]
                    # 漫画详情页
                    comic_detail = i.find('div', {'class': 'mh-item-tip-detali'})
                    # 漫画详情页地址
                    href = comic_detail.find('h2').find('a')['href']
                    comic_url = URL + href
                    # 漫画标题
                    comic_title = comic_detail.find('h2').find('a')['title']
                    # 漫画作者
                    comic_author = comic_detail.find('p', {'class': 'author'}).find('a').text
                    # 漫画内容简介
                    comic_content = comic_detail.find('div', {'class': 'desc'}).text
                    comic_content = comic_content.replace('\u3000', '').replace('\xa0', '').strip()
                    # 章节信息
                    comic_chapter = comic_detail.find('p', {'class': 'chapter'})
                    comic_isover = '完结' if comic_chapter.find('span').text == '完结' else '连载中'
                    comic_currChapter = comic_chapter.find('a').text
                    # 缓存这一条文章的全部信息，以备保存到CSV
                    # print(comic_title + "; " + comic_author + "; " + comic_content + '; ' + comic_isover + "; " + comic_currChapter)
                    post_list.append([comic_title, comic_author, comic_cover, comic_content, comic_isover, comic_currChapter, comic_url])
                time.sleep(0.4)
                page_num += 1
            else:
                flag = False
                print('结束')
        except:
            flag = False
            print('结束')
            break

    print(time.ctime() + "; 爬取" + curl + "页")
    post_data = pd.DataFrame(columns=csv_title, data=post_list)
    post_data.to_csv(save_path + new_path + '.csv',encoding='UTF-8')


def main():
    for item in DATA_LIST:
        path_leimu = item['directory']
        url_leimu = item['url']
        # 爬取模板
        CrawModel(path_leimu, url_leimu)


if __name__ == "__main__":
    main()