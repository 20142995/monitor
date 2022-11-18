#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import os
import requests

DINGTALK_TOKEN = os.getenv('DINGTALK_TOKEN')
DDDDOCR_URL = os.getenv('DDDDOCR_URL')

def send_text(text, token):
    headers = {'Content-Type': 'application/json'}
    data = {"msgtype": "text", "text": {"content": text},
            "at": {"atMobiles": [], "isAtAll": False}, }
    url = "https://oapi.dingtalk.com/robot/send?access_token={}".format(token)
    r = requests.post(url, json=data, headers=headers)
    return r.json()

def check_ddddocr():
    try:
        rt = requests.get('{}/ping'.format(DDDDOCR_URL)).text
        if rt == 'pong':
            return True
    except:
        pass
    return False

if __name__ == '__main__':
    text = '服务监控:'
    text += '\n{}\t{}\t{}'.format("验证码识别接口",DDDDOCR_URL,'正常' if check_ddddocr() else '异常')
    send_text(text, DINGTALK_TOKEN)



