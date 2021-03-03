# -*- coding: utf8 -*-

import requests
from bs4 import BeautifulSoup
from utils.log import get_logger

logger = get_logger('SignIn52pj')


def sign_in_52pj(cookie: str, tag: str, SCKEY: str) -> str:
    global msg
    try:
        msg = ""
        if tag.strip() == '':
            tag = cookie[0:8]
        s = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
            'Cookie': cookie,
            'ContentType': 'text/html;charset=gbk'
        }
        s.get('https://www.52pojie.cn/home.php?mod=task&do=apply&id=2', headers=headers)
        a = s.get('https://www.52pojie.cn/home.php?mod=task&do=draw&id=2', headers=headers)
        b = BeautifulSoup(a.text, 'html.parser')
        c = b.find('div', id='messagetext').find('p').text

        if "您需要先登录才能继续本操作" in c:
            if SCKEY:
                url = f"https://sc.ftqq.com/{SCKEY}.send"
                data = {
                    "text": "吾爱破解 标识为：" + tag + " Cookie过期",
                    "desp": c
                }
                requests.post(url, data=data)
            logger.info(f'cookie_52pj失效，需重新获取,标识为：', tag)
            print("cookie_52pj失效，需重新获取,标识为：", tag)
            msg += "cookie_52pj失效，需重新获取,标识为：" + tag
        elif "恭喜" in c:
            print("吾爱破解签到成功")
            msg += "吾爱破解签到成功"
        elif "不是进行中的任务" in c:
            print("吾爱破解已经签到")
            msg += "吾爱破解已经签到"
        else:
            print(c)
    except:
        print("吾爱破解出错")
        msg += "吾爱破解出错"
    return msg + "\n"


def variable_52pj(cookie, SCKEY):
    if cookie:
        print("----------吾爱破解开始尝试签到----------")
        msg = ""
        clist = cookie.split("\n")
        i = 0
        while i < len(clist):
            msg += f"第 {i + 1} 个账号开始执行任务\n"
            cookie = clist[i]
            msg += sign_in_52pj(cookie, "", SCKEY)
            i += 1
        print("----------吾爱破解签到执行完毕----------")
        return msg


def conventional_52pj(pojie52: dict, SCKEY):
    if pojie52:
        print("----------吾爱破解开始尝试签到----------")
        msg = ""
        for i, item in enumerate(pojie52, 1):
            msg += f"第 {i + 1} 个账号开始执行任务\n"
            msg += sign_in_52pj(item['cookie'], item['tag'], SCKEY)

        print("----------吾爱破解签到执行完毕----------")
