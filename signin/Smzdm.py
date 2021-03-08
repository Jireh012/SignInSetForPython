'''
# @Author       : Jireh
# @Date         : 2021-03-08 16:12:39
# @LastEditors  : Jireh
# @LastEditTime : 2021-03-05 09:16:39
# @Description  : 什么值得买签到逻辑
'''

# -*- coding: utf8 -*-
import requests, os
import json
import time
import string


def sign_in_smzdm(cookie: str, tag: str, SCKEY: str):
    try:
        msg = ""
        s = requests.Session()
        s.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'})
        t = round(int(time.time() * 1000))
        url = f'https://zhiyou.smzdm.com/user/checkin/jsonp_checkin?_={t}'

        headers = {
            "cookie": cookie,
            'Referer': 'https://www.smzdm.com/'
        }

        r = s.get(url, headers=headers, verify=False)
        print(r.text.encode('latin-1').decode('unicode_escape'))
        if r.json()["error_code"] != 0:
            if SCKEY:
                url = f"https://sc.ftqq.com/{SCKEY}.send"
                data = {
                    "text": "什么值得买 标识为：" + tag + " Cookie过期",
                    "desp": r.text
                }
                requests.post(url, data=data)
            msg += "smzdm 标识为：" + tag + "cookie失效"
        else:
            msg += "smzdm标识为：" + tag + "签到成功"
    except Exception as e:
        print('repr(e):', repr(e))
        msg += '运行出错,repr(e):' + repr(e)
    return msg + "\n"


def variable_smzdm(cookie, SCKEY):
    if cookie:
        print("----------什么值得买开始尝试签到----------")
        msg = ""
        clist = cookie.split("\n")
        i = 0
        while i < len(clist):
            msg += f"第 {i + 1} 个账号开始执行任务\n"
            cookie = clist[i]
            msg += sign_in_smzdm(cookie, "", SCKEY)
            i += 1
        print("----------什么值得买签到执行完毕----------")
        return msg


def conventional_smzdm(wuaipojie: dict, SCKEY):
    if wuaipojie:
        print("----------什么值得买开始尝试签到----------")
        msg = ""
        for i, item in enumerate(wuaipojie, 1):
            msg += f"第 {i + 1} 个账号开始执行任务\n"
            msg += sign_in_smzdm(item['cookie'], item['tag'], SCKEY)

        print("----------什么值得买签到执行完毕----------")
