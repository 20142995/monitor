#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import os
import redis
import requests

DINGTALK_TOKEN = os.getenv('DINGTALK_TOKEN')
DDDDOCR_URL = os.getenv('DDDDOCR_URL')
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PASS = os.getenv('REDIS_PASS')

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

def check_redis():
    try:
        host, port = REDIS_HOST.split(":")
        rc = redis.Redis(host=host, port=int(port), password=REDIS_PASS,
                        decode_responses=True, charset='UTF-8', encoding='UTF-8')
        return True
    except:
        pass
    return False

if __name__ == '__main__':
    text = '服务监控:'

    text += '\n{}\t{}\t{}'.format("验证码识别接口", DDDDOCR_URL,
                                  '正常' if check_ddddocr() else '异常')
    text += '\n{}\t{}\t{}'.format("redis", REDIS_HOST,
                                  '正常' if check_redis() else '异常')
    send_text(text, DINGTALK_TOKEN)
