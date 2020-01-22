import requests
import json
from lxml import etree

class Spider(object):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    url_all = 'http://m.18hm.cc/home/api/cate/tp/1-0-2-1-{}' # 全部
    url_near = 'http://m.18hm.cc/home/api/cate/tp/1-0-1-1-{}' # 已完结的
    url_click = 'http://m.18hm.cc/home/api/cate/tp/1-0-0-1-{}' # 连载中

    def init_spider(self):
        flag = True
        index = 1
        while flag:
            url = self.url_click.format(str(index))
            response = requests.get(url, headers=self.headers, timeout=50)
            response_data = json.loads(response.text)
            print(response_data)
            if response_data['code'] == 1:
                result = response_data['result']
                lastPage = result['lastPage']
                list = result['list']
                # print(list)
                if lastPage:
                    flag = False
                else:
                    index += 1

            else:
                flag = False

    def get_chapter(self):
        url = 'http://m.18hm.cc/home/api/chapter_list/tp/13736-1-1-10'
        response = requests.get(url, headers=self.headers, timeout=50)
        print(json.loads(response.text))

spider = Spider()
spider.get_chapter()