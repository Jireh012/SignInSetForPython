'''
# @Author       : Jireh
# @Date         : 2021-03-02 10:21:39
# @LastEditors  : Jireh
# @LastEditTime : 2021-03-05 09:17:39
# @Description  : 后期菌签到逻辑
'''
# -*- coding: utf8 -*-

import requests
from bs4 import BeautifulSoup
from utils.log import get_logger

logger = get_logger('SignIn52cxy')


def sign_in_52cxy(cookie: str, tag: str, SCKEY: str) -> str:
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

        url = "https://www.52programer.com/plugin.php?id=k_misign:sign"
        get_form_hash = s.get(url=url, headers=headers)
        b = BeautifulSoup(get_form_hash.text, 'html.parser')
        form_hash = b.find('input', {"name": "formhash"})["value"]
        sign_url = "https://www.52programer.com/plugin.php?id=k_misign:sign&operation=qiandao&formhash=" + form_hash + "&from=insign&inajax=1&ajaxtarget=JD_sign"
        get_sign = s.get(url=sign_url, headers=headers)
        bs = BeautifulSoup(get_sign.text, 'html.parser')

        if bs.text in "成功":
            if SCKEY:
                url = f"https://sc.ftqq.com/{SCKEY}.send"
                data = {
                    "text": "吾爱程序员 标识为：" + tag + " Cookie过期",
                    "desp": bs.text
                }
                requests.post(url, data=data)
            logger.info(f'cookie_52cxy失效，需重新获取,标识为：', tag)
            print("cookie_52cxy失效，需重新获取,标识为：", tag)
            msg += "cookie_52cxy失效，需重新获取,标识为：" + tag
        elif "成功" in bs.text:
            print("吾爱程序猿签到成功标识为：", tag)
            msg += "吾爱程序猿签到成功标识为：" + tag
        elif "\n今日已签" in bs.text:
            print("吾爱程序猿已经签到,标识为：", tag)
            msg += "吾爱程序猿已经签到标识为：" + tag
        else:
            print(bs.text)
    except:
        print("吾爱程序猿出错标识为：", tag)
        msg += "吾爱程序猿出错标识为：" + tag
    return msg + "\n"


def variable_52cxy(cookie, SCKEY):
    if cookie:
        print("----------吾爱程序猿开始尝试签到----------")
        msg = ""
        clist = cookie.split("\n")
        i = 0
        while i < len(clist):
            msg += f"第 {i + 1} 个账号开始执行任务\n"
            cookie = clist[i]
            msg += sign_in_52cxy(cookie, "", SCKEY)
            i += 1
        print("----------吾爱程序猿签到执行完毕----------")
        return msg


def conventional_52cxy(cookie: dict, SCKEY):
    if cookie:
        print("----------吾爱程序猿开始尝试签到----------")
        msg = ""
        for i, item in enumerate(cookie, 1):
            msg += f"第 {i + 1} 个账号开始执行任务\n"
            msg += sign_in_52cxy(item['cookie'], item['tag'], SCKEY)

        print("----------吾爱程序猿签到执行完毕----------")
