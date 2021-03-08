'''
# @Author       : Jireh
# @Date         : 2021-03-2 14:21:39
# @LastEditors  : Jireh
# @LastEditTime : 2021-03-05 09:16:39
# @Description  : 后期菌签到逻辑
'''

# -*- coding: utf8 -*-
import requests, os
import json
import random
import string


class randoms():
    # 获取26个大小写字母
    letters = string.ascii_letters
    # 获取26个小写字母
    Lowercase_letters = string.ascii_lowercase
    # 获取26个大写字母
    Capital = string.ascii_uppercase
    # 获取阿拉伯数字
    digits = string.digits


def sign_in_hqj(username: str, password: str, SCKEY: str):
    msg = ""
    try:
        s = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4298.4 Safari/537.36',
            'Cookie': 'PHPSESSID=' + code(),
            'ContentType': 'text/html;charset=gbk',
            'DNT': '1'
        }
        url = "http://www.houqijun.vip/Passport_runLogin.html"
        loginData = {
            "from": "http://www.houqijun.vip/",
            "username": username,
            "password": password,
        }

        login = s.post(url=url, data=loginData, headers=headers)
        msg += "登录成功！,"
        a = s.get('http://www.houqijun.vip/Center_runQiandao.html',
                  headers=headers)
        data = json.loads(a.text)

        if data['code'] == 1:
            msg += username + " 后期菌签到成功！,"
            print(username + " 后期菌签到成功")
        elif data['code'] == 0:
            msg += username + " 后期菌重复签到！,"
            print(username + " 后期菌重复签到")
        else:
            if SCKEY:
                scurl = f"https://sc.ftqq.com/{SCKEY}.send"
                data = {
                    "text": username + " 后期菌签到异常",
                    "desp": data
                }
                requests.post(scurl, data=data)
            print(data)
    except Exception as e:
        print('repr(e):', repr(e))
        msg += '运行出错,repr(e):' + repr(e)
    return msg + "\n"


def code():
    # s是小写字母和数字的集合
    s = randoms.Lowercase_letters + randoms.digits
    # 生成28位小写和数字的集合，并将列表转字符串
    code = ''.join(random.sample(s, 28))
    return code


def variable_hqj(usernames, passwords, SCKEY):
    msg = ""
    ulist = usernames.split("\n")
    plist = passwords.split("\n")
    if len(ulist) == len(plist):
        print("----------后期菌开始尝试签到----------")
        i = 0
        while i < len(ulist):
            msg += f"第 {i + 1} 个账号开始执行任务\n"
            username = ulist[i]
            password = plist[i]
            msg += sign_in_hqj(username, password, SCKEY)
            i += 1
    else:
        msg = "账号密码个数不相符"
        print(msg)

    print("----------后期菌签到执行完毕----------")


def conventional_hqj(houqijun: dict, SCKEY):
    if houqijun:
        print("----------后期菌开始尝试签到----------")
        msg = ""
        for i, item in enumerate(houqijun, 1):
            msg += f"第 {i + 1} 个账号开始执行任务\n"
            msg += sign_in_hqj(item['username'], item['password'], SCKEY)

        print("----------后期菌签到执行完毕----------")
