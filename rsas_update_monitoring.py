#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import re
import json
import redis
import requests

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PASS = os.getenv('REDIS_PASS')
DINGTALK_TOKEN = os.getenv('DINGTALK_TOKEN')


def send_text(text, token):
    headers = {'Content-Type': 'application/json'}
    data = {"msgtype": "text", "text": {"content": text},
            "at": {"atMobiles": [], "isAtAll": False}, }
    url = "https://oapi.dingtalk.com/robot/send?access_token={}".format(token)
    r = requests.post(url, json=data, headers=headers)
    return r.json()


if __name__ == '__main__':
    host, port = REDIS_HOST.split(":")
    rc = redis.Redis(host=host, port=int(port), password=REDIS_PASS,
                     decode_responses=True, charset='UTF-8', encoding='UTF-8')
    data = rc.get('rsas')
    if data is None:
        data = [
            {
                'name': '远程安全评估系统(RSAS)6.0系统插件', 'url': 'http://update.nsfocus.com/update/listRsasDetail/v/vulsys', 'version': '', 'uptime': ''
            },
            {
                'name': '远程安全评估系统(RSAS)6.0系统', 'url': 'http://update.nsfocus.com/update/listRsasDetail/v/rsassys', 'version': '', 'uptime': ''
            },
            {
                'name': '远程安全评估系统(RSAS6.0)Web插件', 'url': 'http://update.nsfocus.com/update/listRsasDetail/v/vulweb', 'version': '', 'uptime': ''
            }
        ]
    else:
        data = json.loads(data)
    for i in range(len(data)):
        r = requests.get(data[i]['url'])
        r.encoding = r.apparent_encoding
        for version, uptime in re.findall(r'版本：</span>\s+(.*?)</td>.*?发布时间：</span>(.*?)</td>', r.text, re.S)[:1]:
            if version != data[i].get('version', ''):
                text = '{}:\n更新版本:{}\n更新时间:{}'.format(
                    data[i]['name'], version, uptime)
                send_text(text, DINGTALK_TOKEN)
                data[i]['version'] = version
                data[i]['uptime'] = uptime
    rc.set('rsas', json.dumps(data))
