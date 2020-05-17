import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


class Spider(object):
    headers = {
        'Cookie': 'Hm_lvt_70c370dd3cf0c2f7da21108334204273=1585975807;PHPSESSID=210t5j29ejprasp4k51emrk9a6;wordpress_logged_in_6e13e871cd825952ccb8f46c28fa4b11=bowZanii0OCQANFjCscHXGPA8gzobspO%7C1587196489%7CEQhVxoMpLyxkpkhtDy5G3ea9hcq9L132jO8gCF5h2wc%7C65c6591c991c82d6cc16158e3863e0eea7f1f460ac38a181ffc10c6d80cfca94;Hm_lpvt_70c370dd3cf0c2f7da21108334204273=1585987424',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
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

    def init_spider(self, web_url, save_path, start_page_num, end_page_num):
        post_list = []
        csv_title = ['标题', '内容地址']

        for index in range(start_page_num, end_page_num):
            post_list = []
            url = web_url.format(str(index))
            print(url)
            page = self.get_html(url)
            list_container = page.find('div', {'class': 'poi-row inn-archive__container'})
            comic_list = list_container.find_all('article')
            # print(comic_list)
            for comic in comic_list:
                # print(comic)
                comic_info = comic.find('a', {'class': 'inn-archive__item__title__link inn-card_post-thumbnail__item__title__link'})
                if comic_info:
                    # 漫画标题
                    comic_title = comic_info.text
                    print(comic_title)
                    comic_url = comic_info['href']
                    post_list.append([comic_title, comic_url])

            post_data = pd.DataFrame(columns=csv_title, data=post_list)
            if index == 1:
                post_data.to_csv(save_path, encoding='UTF-8')
            else:
                post_data.to_csv(save_path, mode='a', header=False, encoding='UTF-8')



url1 = 'https://www.macgn.com/archives/category/comic/offprint/page/{}?btwaf=91020540'
url2 = 'https://www.macgn.com/archives/category/comic/aggregation/page/{}?btwaf=14618027'
url3 = 'https://www.macgn.com/archives/category/comic/cg/page/{}?btwaf=91020540'
spider = Spider()
# spider.init_spider(url1, 'ACG萌站单行本列表.csv', 11, 13)
spider.init_spider(url2, 'ACG萌站作品合集列表.csv', 1, 13)
spider.init_spider(url3, 'ACG萌站CG画集列表.csv', 1, 5)
