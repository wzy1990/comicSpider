# This Python file uses the following encoding: utf-8
import requests
import json
import time
import os
from lxml import etree
from bs4 import BeautifulSoup


def main():
    file = 'D:/非人哉'
    if not os.path.exists(file):
        os.mkdir(file)
        print('创建文件夹：',file)
    r_url="http://www.manhuadao.cn/"
    url = "http://www.manhuadao.cn/Home/ComicDetail?id=58ddb07827a7c1392c234628"
    headers = {  # 模拟浏览器访问网页
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \\Chrome/75.0.3770.142 Safari/537.36'}
    response = requests.get(url=url, headers=headers)
    response.encoding = response.apparent_encoding
    html = response.text
    html = html.encode('gbk', "ignore").decode('gbk')  # 先用gbk编码,忽略掉非法字符,然后再译码
    html = html.encode('utf-8').decode('utf-8')
    print(html)   # 输出网页源码
    data = etree.HTML(html)
    # tp = data.xpath('//ul[@class="read-chapter"]/li/a[@class="active"]/@href')
    tp = data.xpath('//*[@class="yesReader"]/@href')
    zhang_list = tp
    i=1
    for next_zhang in zhang_list:
        i=i+1
        j=0
        hui_url = r_url+next_zhang
        name1 = "第"+str(i)+"回"
        file = 'E:/非人哉' + '/{}/'.format(name1)    # 这里需要自己设置路径
        if not os.path.exists(file):
            os.makedirs(file)
            print('创建文件夹：', file)
        response = requests.get(url=hui_url, headers=headers)
        data = etree.HTML(response.text)
        # tp = data.xpath('//div[@class="no-pic"]//img/@src')
        tp = data.xpath('//div[@class="main-content"]//ul//li//div[@class="no-pic"]//img/@src')
        ye_list = tp
        for k in ye_list:
            download_url = tp[j]
            print(download_url)
            j=j+1
            file_name="第"+str(j)+"页"
            response = requests.get(url=download_url)
            with open(file+file_name+".jpg","wb") as f:
                f.write(response.content)


if __name__ == '__main__':
    main()