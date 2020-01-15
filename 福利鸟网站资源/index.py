import requests
from lxml import etree
from pathlib import Path
import time
import pandas as pd


class Spider(object):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    web_url = 'https://www.mkzhan.com'
    comic_save_path = ''
    chapter_save_path = ''

    def init_spider(self, url):
        for index in range(1, 100):
            print(url.format(index))
            r = requests.get(url.format(index), headers=self.headers, timeout=50)
            r.encoding = r.apparent_encoding
            html = r.text
            html = html.encode('gbk', "ignore").decode('gbk')  # 先用gbk编码,忽略掉非法字符,然后再译码
            html = html.encode('utf-8').decode('utf-8')
            ret = etree.HTML(html)
            archive_list = ret.xpath('//div[@id="post_list_box"]/article[@class="archive-list"]/figure/a/@href')
            print(archive_list)
            self.chapter_request(archive_list)

    # 遍历章节列表
    def chapter_request(self, archive_list):
        for link in archive_list:
            print(link)
            try:
                t = requests.get(link)
                parse = t.text
                parse = parse.encode('gbk', "ignore").decode('gbk')  # 先用gbk编码,忽略掉非法字符,然后再译码
                parse = parse.encode('utf-8').decode('utf-8')
                html = etree.HTML(parse)
                chapter_title = html.xpath('//h1[@class="comic-title"]/a[@class="last-crumb"]/text()')

                image = html.xpath('//div[@class="rd-article__pic hide"]/img[@class="lazy-read"]/@data-src')
                self.CrawModel(image)
            except Exception as e:
                print(e)

    def CrawModel(new_path, url):
        post_list = []
        csv_title = ['标题', '作者', '封面', '内容简介', '是否完结', '最新章节', '漫画页地址']
        page_num = 1
        flag = True  # 控制跳出循环
        while flag:
            if page_num == 1:
                curl = url  # 分类的第一页，可以不用构造
            else:
                curl = url + '-p' + str(page_num)  # 该分类的其他页，非第一页

            try:  # 第一种URL格式，带有ppt_
                page = get_html(curl)
                ul = page.find('ul', {'class': 'mh-list'})
                li = ul.find_all('li')
                print(len(ul.find_all('li')))
                if len(ul.find_all('li')) > 0:
                    for i in li:
                        # 漫画封面
                        comic_cover = i.find('p', {'class': 'mh-cover'})['style'].split('url(')[1].split(')')[0]
                        print(comic_cover)
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
                        print(
                            comic_title + "; " + comic_author + "; " + comic_cover + "; " + comic_content + '; ' + comic_isover + "; " + comic_currChapter + "; " + comic_url)
                        post_list.append(
                            [comic_title, comic_author, comic_cover, comic_content, comic_isover, comic_currChapter,
                             comic_url])
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
        post_data.to_csv(new_path + '\漫画信息表.csv', encoding='UTF-8')


url = 'http://www.2y2y.net/media/{}/'
spider = Spider()
spider.init_spider(url)
