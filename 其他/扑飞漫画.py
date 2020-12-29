# coding:utf-8
# pip install bs4
# pip install PyExecJS
# pip install fake-useragent
import os
import re
import bs4
import execjs
import fake_useragent
import requests


class DownloadPage:
    def get_content(self, url):
        ua = fake_useragent.UserAgent()
        headers = { 'User_Agent': ua.random }
        response = requests.get(url, headers=headers)
        response.encoding = response.apparent_encoding # 不加这个会有乱码
        html = response.text
        html = html.encode('gbk', "ignore").decode('gbk')  # 先用gbk编码,忽略掉非法字符,然后再译码
        html = html.encode('utf-8').decode('utf-8')
        return html

    def get_page_chapter(self, url, dir_path):
        content = self.get_content(url)
        sel = bs4.BeautifulSoup(content, 'lxml')
        comic_title = sel.select_one('.titleInfo h1').text
        print('【漫画名称】', comic_title)
        chapter_list = sel.select_one('.max-h200').find_all("a")
        print('【章节列表】', chapter_list)
        dir_path = dir_path + '/' + comic_title
        print('【保存路径】', dir_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        for chapter in chapter_list:
            print(chapter)
            if chapter:
                # print(chapter.get("href"))
                # print(chapter.get_text())
                self.download_chapter('http://ipufei.com' + chapter.get("href"), chapter.get_text(), dir_path)

    def get_js(self):
        f = open("base64decode.js", 'r', encoding='utf-8')
        line = f.readline()
        html_str = ''
        while line:
            html_str = html_str + line
            line = f.readline()
        return html_str

    def base_64_decode(self, data):
        js_str = self.get_js()
        ctx = execjs.compile(js_str)
        return ctx.call('f', data)

    def get_image(self, img_urls):
        response = requests.get(img_urls)
        if response.status_code == 200:
            return response.content

    def download_chapter(self, url, chapter_name, dir_path):
        content = self.get_content(url)
        search_obj = re.findall(r'packed="(.+)";eval', content, re.S)
        print(search_obj[0])
        count = 1
        url_list = self.base_64_decode(search_obj[0])
        print(url_list)
        for url2 in url_list:
            print(url2)
            if isinstance(url2, str):
                if url2:
                    image_path = dir_path + '/' + chapter_name + '/P-%s.jpg' % count
                    if not os.path.exists(dir_path + '/' + chapter_name):
                        os.makedirs(dir_path + '/' + chapter_name)
                    if not os.path.exists(image_path):
                        image = self.get_image("http://res.img.pufei.net/" + url2)
                        if image:
                            with open(image_path, 'wb') as f:
                                f.write(image)
                                count += 1


url = "http://ipufei.com/manhua/419/"
save_path = "D:/manhua"

downloadPage = DownloadPage()
content = downloadPage.get_page_chapter(url, save_path)