import requests
from bs4 import BeautifulSoup
import os
from pathlib import Path
from multiprocessing import Pool

comic_name = ''


def get_header(referer):
    header ={
        'cookie':'Hm_lvt_dbc355aef238b6c32b43eacbbf161c3c=1536981553; Hm_lpvt_dbc355aef238b6c32b43eacbbf161c3c=1536986863',
        'referer': referer,
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.92 Safari/537.36'
        }
    return header

def get_pics_for_one(url):
    print('page_url: ', url)
    header = get_header(url)
    pages_link = []

    try:
        web_data = requests.get(url, headers=header)
        web_data.encoding = 'utf8'

        soup = BeautifulSoup(web_data.text,'lxml')
        page_num_text = soup.select('.breadcrumb li.active')[0].text
        page_num = page_num_text.split('页・共')[1].replace('页', '').strip()
        print('page_num: ' + page_num)

        base_link = url.replace('.html', '')
        print('base_link: ' + base_link)
        print(int(page_num))

        for num in range(248, 249):
            current_url = base_link + '_p' + str(num) + '.html'
            pages_link.append(current_url)
    except:
        pass
    return pages_link


def download_pics(pic_page, path):

    try:
        page_data = requests.get(pic_page, headers=header)
        page_data.encoding = 'utf8'

        soup = BeautifulSoup(page_data.text,'lxml')
        image_url = soup.select('img.show-pic')[0].get('src')
        print('image_url: ', image_url)

        try:
            pic_name_list = image_url.split('/')
            list_len = len(pic_name_list)
            pic_name = pic_name_list[list_len - 1]
            print(pic_name)
            pic_save_path = path + "\\" + pic_name
            print(pic_save_path)

            pic_data = requests.get(image_url, headers=header)
            pic_data.encoding = 'utf8'

            if os.path.isfile(pic_save_path):
                print("########此图已经下载########")
            else:
                with open(str(pic_save_path), 'wb') as f:
                    f.write(pic_data.content)
        except:
            pass
    except:
        pass


def get_pics_for_one_pages(url, header, pool_num):
    try:
        web_data = requests.get(url, headers=header)
        web_data.encoding = 'utf8'
        soup = BeautifulSoup(web_data.text, 'lxml')
        comic_name = soup.select('h1.comic-title')[0].text
        pages_url = soup.select('#version ol li a')
        print('===============当前漫画：', comic_name + "==============")
        comic_save_path = "comic\\" + comic_name
        path = Path(comic_save_path)
        if path.exists():
            pass
        else:
            path.mkdir()

        count_num = 1
        for page_url in pages_url:
            if count_num == 2:
                print('===============开始下载：', page_url.text + "==============")
                print("当前章节链接地址", 'https://www.manhuadb.com' + page_url.get('href'))
                url_list = get_pics_for_one('https://www.manhuadb.com' + page_url.get('href') )
                img_save_path = comic_save_path + '\\' + page_url.text.strip()
                path = Path(img_save_path)
                print('img_save_path:', path)
                print('url_list:', url_list)
                if path.exists():
                    pass
                else:
                    path.mkdir()

                for img_url in url_list:
                    download_pics(img_url, img_save_path)
                # pool = Pool(pool_num)
                # pool.map(download_pics,url_list)
                # pool.close()
                # pool.join()
                print("======================下载完成======================")
                print("")
            count_num += 1
    except:
        pass


if __name__ == '__main__':
    print("                     |-----------------------------|")
    print("                     | 欢迎使用无界面多进程美图下载器！ |")
    print("                     | 此项目只供个人学习使用，请勿用于 |")
    print("                     |       其他商业用途，谢谢！     |")
    print("                     |       如若侵权，联系立删！     |")
    print("                     |-----------------------------|")
    pool_num = 1 # int(input('请输入启动进程数: '))
    print("           漫画下载器开始运行...           ")
    header = get_header("referer")
    try:
        base_url = 'https://www.manhuadb.com/manhua/4122'
        get_pics_for_one_pages(base_url, header, pool_num)

    except:
        print("网络连接错误...")
    print("")
    print("##################全部下载完成!##################")