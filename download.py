# -*- coding: utf-8 -*-
#导入requests模块，模拟发送请求
import requests
#导入线程池模块，创建30个线程同时做
from concurrent.futures import ThreadPoolExecutor
#导入ssl模块，处理https请求失败问题
import ssl
#导入json
import json
#导入re
import re
import os
#定义请求头
headers="{'Accept': '*/*', 'Accept-Language': 'en-US,en;q=0.5', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}"
headers={
    'Accept':'*/*',
    'Accept-Language':'en-US,en;q=0.5',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
}
# 定义一个池，大小为30
pool = ThreadPoolExecutor(30)
# 生成证书上下文(unverified 就是不验证https证书)
ssl._create_default_https_context = ssl._create_unverified_context
res_json = requests.get('https://api.bilibili.com/x/player/pagelist?aid=73342471').json()


# 正则表达式，根据条件匹配出值
def my_match(text, pattern):
    match = re.search(pattern, text)
    # print(match.group(1))
    # print()
    return json.loads(match.group(1))


# 下载并合并视频的函数
def download_video(old_video_url, video_url, audio_url, video_name):
    headers.update({"Referer": old_video_url})
    print("开始下载视频：%s" % video_name)
    video_content = requests.get(video_url, headers=headers)
    print('%s视频大小：' % video_name, video_content.headers['content-length'])
    audio_content = requests.get(audio_url, headers=headers)
    print('%s音频大小：' % video_name, audio_content.headers['content-length'])
    # 下载视频开始
    received_video = 0
    with open('%s_video.mp4' % video_name, 'ab') as output:
        while int(video_content.headers['content-length']) > received_video:
            headers['Range'] = 'bytes=' + str(received_video) + '-'
            response = requests.get(video_url, headers=headers)
            output.write(response.content)
            received_video += len(response.content)
    # 下载视频结束
    # 下载音频开始
    audio_content = requests.get(audio_url, headers=headers)
    received_audio = 0
    with open('%s_audio.mp4' % video_name, 'ab') as output:
        while int(audio_content.headers['content-length']) > received_audio:
            # 视频分片下载
            headers['Range'] = 'bytes=' + str(received_audio) + '-'
            response = requests.get(audio_url, headers=headers)
            output.write(response.content)
            received_audio += len(response.content)
    # 下载音频结束
    return video_name


def make_all(result):
    # 视频音频合并
    video_name = result.result()
    import subprocess
    video_final = video_name.replace('video', 'video_final')
    ss = 'ffmpeg -i %s_video.mp4 -i %s_audio.mp4 -c copy %s.mp4' % (video_name, video_name, video_final)
    subprocess.Popen(ss, shell=True)
    # 删除视频和音频
    # os.remove('%s_video.mp4'%video_name)
    # os.remove('%s_audio.mp4'%video_name)
    print("视频下载结束：%s" % video_name)

def main_download():
    for i, video_content in enumerate(res_json['data']):
        video_name = ('./video/' + video_content['part']).replace(" ", "-")
        old_video_url = 'https://www.bilibili.com/video/av73342471' + '?p=%d' % (i + 1)
        # print('视频地址为：',old_video_url)
        # print('视频名字为：',video_name)
        # 加载上面拼凑的视频地址
        res = requests.get(old_video_url, headers=headers)
        # 解析出当前页面下所有视频的json
        # initial_state = my_match(res.text, r'__INITIAL_STATE__=(.*?);\(function\(\)')
        # 解析出视频详情的json
        playinfo = my_match(res.text, '__playinfo__=(.*?)</script><script>')
        # 列表套字典，拼凑出视频和音频的字典（这里只下载1080p的视频）
        video_info_list = []
        for i in range(4):
            video_info = {}
            video_info['quality'] = playinfo['data']['accept_description'][i]
            video_info['acc_quality'] = playinfo['data']['accept_quality'][i]
            video_info['video_url'] = playinfo['data']['dash']['video'][i]['baseUrl']
            video_info['audio_url'] = playinfo['data']['dash']['audio'][0]['baseUrl']
            video_info_list.append(video_info)
        # 1080p视频的地址为，分片加载的
        video_url = video_info_list[0]['video_url']
        # 1080p视频的音频为，分片加载的
        audio_url = video_info_list[0]['audio_url']
        # download_cov(old_video_url,video_url,audio_url,video_name)
        pool.submit(download_video, old_video_url, video_url, audio_url, video_name).add_done_callback(make_all)
    pool.shutdown(wait=True)


if __name__ == '__main__':
    main_download()
