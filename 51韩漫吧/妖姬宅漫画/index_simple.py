import requests
import json
import os
from pathlib import Path

class Spider(object):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    url_all = 'http://m.18hm.cc/home/api/cate/tp/1-0-2-1-{}' # 全部
    url_over = 'http://m.18hm.cc/home/api/cate/tp/1-0-1-1-{}' # 已完结的
    url_serialize = 'http://m.18hm.cc/home/api/cate/tp/1-0-0-1-{}' # 连载中
    url_chapter_list = 'http://m.18hm.cc/home/api/chapter_list/tp/{}-1-1-200'
    url_image_download = 'https://img.toptoon.club/'
    comic_save_path = ''
    chapter_save_path = ''
    had_download_comic = ['媳妇的诱惑', '退货女友', 'Run away', '女上男下', '前女友', '密室逃脱', '爱情店到店', '报告夫人', '我要抢走她', '那家伙的女人', '玩转女上司', 
    '荒淫同学会', '阿姨的秘密情事', '女大生世晶:无法自拔', '恋人模式', '新媳妇', '隐秘的诱惑', '人夫的悸动', '共享情人', '初恋陷阱', '性溢房屋', '小裤裤精灵', '低速男高速女', 
    '甜蜜假期', '夺爱的滋味', '三姐妹', '窥视', '流浪猫', '意外的邂逅（真人漫画）', '异乡人:意外桃花源', '混混痞痞 派遣員', '曖昧女剧场', '鸭王', '青涩男孩初体验', '我的M属性学姐', 
    '老婆回来了', '两个女人', '梦魇', '虐妻游戏', '熟女的滋味', '恋爱宝境', '啪啪啪调教所', '哥哥的秘书', '母猪养成计划', '无法自拔的口红胶', '激情开麦拉', '甜美女孩', 'Bodychange', 
    '销魂之手', '学妹别放肆', '成人的滋味', 'SEED The Beginning', '养女', '私生:爱到痴狂', '朋友的妻子：有妳在的家', '爸爸的女人', '制服的诱惑', '堕落游戏', '罪与罚', '敏希', 
    'LOVE 爱的导航G', '合理怀疑', '危险的女人', '湿家侦探', '开发性味蕾', '性癖好', '初恋物語', '那里的香气', '死亡天使', '淫荡的妻子们', '索多玛俱乐部', '夏美我的爱', 
    '神的礼物', '人妻性解放', '关系', '交往的条件', '腥红之壁', '青春:逆齡小鮮肉', '代理孕母', '奇怪的超商', '他的女人', '朋友妻', '噓！姐姐的诱惑', '新生淫乱日记', '姐夫,硬起來']

    def get_comic_list(self, list_url, comic_root_path):
        flag = True
        index = 1
        while flag:
            url = list_url.format(str(index))
            response = requests.get(url, headers=self.headers, timeout=50)
            html = response.text
            # html = html.encode('gbk', "ignore").decode('gbk')  # 先用gbk编码,忽略掉非法字符,然后再译码
            html = html.encode('utf-8').decode('utf-8')
            response_data = json.loads(html)
            # print(json.loads(html))
            if response_data['code'] == 1:
                result = response_data['result']
                lastPage = result['lastPage']
                list = result['list']
                # print(list)
                for comic in list:
                    if comic['title'] not in self.had_download_comic:
                        self.get_comic_detail(comic['title'], comic['id'], comic_root_path)
                    else: 
                        print(comic['title'] + ' -- 已下载')   
                if lastPage:
                    flag = False
                else:
                    index += 1

            else:
                flag = False

    def get_comic_detail(self, comic_title, comic_id, comic_root_path):
        self.comic_save_path = comic_root_path + comic_title.replace(':', '：').replace('?', '？')
        path = Path(self.comic_save_path)
        if path.exists():
            pass
        else:
            path.mkdir()
        self.get_comic_chapter(comic_id)

    def save_comic_detail(self, list_url, save_path):
        post_list = []
        csv_title = ['漫画ID', '标题', '作者', '封面', '内容简介', '是否完结', '最新章节', '题材类型', '关键字', '评分']
        flag = True
        index = 1
        while flag:
            url = list_url.format(str(index))
            response = requests.get(url, headers=self.headers, timeout=50)
            response_data = json.loads(response.text)
            if response_data['code'] == 1:
                result = response_data['result']
                lastPage = result['lastPage']
                list = result['list']
                for comic in list:
                    post_list.append(comic['title'])

                if lastPage:
                    flag = False
                else:
                    index += 1

            else:
                flag = False
        print(post_list)
        print(len(post_list))

    def get_comic_chapter(self, comic_id):
        url = self.url_chapter_list.format(comic_id)
        response = requests.get(url, headers=self.headers, timeout=50)
        response.encoding = response.apparent_encoding
        response_data = json.loads(response.text)
        result = response_data['result']
        # print(result)
        list = result['list']
        # print(list)
        # print(len(list))
        for item in list:
            title = item['title'].replace(':', '：').replace('?', '？').replace('...', '').strip()
            # print('当前章节：', item['title'])
            self.chapter_save_path = self.comic_save_path + '\\' + title
            path = Path(self.chapter_save_path)
            if path.exists():
                pass
            else:
                path.mkdir()
            self.down_img(item['imagelist'])

    def down_img(self, image_list):
        print(image_list.split(','))
        index = 1
        image_list = image_list.split(',')
        for img_url in image_list:
            if index < 10:
                pic_name = '00{}.jpg'.format(str(index))
            elif index < 100:
                pic_name = '0{}.jpg'.format(str(index))
            else:
                pic_name = '{}.jpg'.format(str(index))
            image_path = self.chapter_save_path + '\\' + pic_name
            if os.path.isfile(image_path):
                print("此图已经存在:", pic_name)
            else:
                print("图片正在下载:", image_path)
                img_url = self.url_image_download + img_url.replace('./', '')
                print('图片下载地址：', img_url)
                # urllib.request.urlretrieve(img_url, image_path)
                try:
                    pic_data = requests.get(img_url, headers=self.headers, timeout=50)
                    with open(image_path, 'wb') as f:
                        f.write(pic_data.content)
                except:
                    print('图片下载失败：：：', img_url)
            index += 1

    def init_spider(self):
        print("    | ---------------------------------  |")
        print("    |     欢迎使用妖姬宅漫画下载器！         |")
        print("    |       目标站点：m.18hm.cc            |")
        print("    | 作者:zhiyong_wang(946455381@qq.com) |")
        print("    | ================================== |")
        print("    |    1. 下载完结漫画(D:\manhua\完结韩漫) |")
        print("    |    2. 下载连载漫画(D:\manhua\连载韩漫) |")
        print("    |    3. 下载指定漫画                   |")
        print("    |    4. 保存漫画列表信息到本地           |")
        # 选择功能
        option = int(input('请您通天塔选择功能选项：'))
        if option == 1:
            self.get_comic_list(self.url_over, 'D:\manhua\完结韩漫\\')
        elif option == 2:
            self.get_comic_list(self.url_serialize, 'D:\manhua\连载韩漫\\')
        elif option == 3:
            # 漫画名称
            comic_title = input('请输入你需要下载的漫画名称：')
            # 漫画ID
            comic_id = input('请输入你需要下载的漫画ID：')
            # 漫画保存路径
            comic_root_path = 'D:\manhua\完结韩漫\\'
            self.get_comic_detail(comic_title, comic_id, comic_root_path)
        else:
            self.save_comic_detail(self.url_over, '完结漫画列表.csv')
            self.save_comic_detail(self.url_serialize, '连载漫画列表.csv')

spider = Spider()
spider.init_spider()