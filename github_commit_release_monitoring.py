#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import json
import redis
import time
import requests
requests.packages.urllib3.disable_warnings()

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PASS = os.getenv('REDIS_PASS')
DINGTALK_TOKEN = os.getenv('DINGTALK_TOKEN')
GH_TOKEN = os.getenv('GH_TOKEN')


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
    data = rc.get('repos')
    if data is None:
        data = {
            'BeichenDream/Godzilla':{},
        }
    else:
        data = json.loads(data)
    headers = {"Authorization": "token {}".format(GH_TOKEN)}
    for name in data:
        try:
            rj = requests.get('https://api.github.com/repos/{}/commits'.format(name), headers=headers, verify=False).json()
            for commit in rj[:1]:
                date = time.strftime("%Y-%m-%d %H:%M:%S",time.strptime(commit['commit']['committer']['date'], "%Y-%m-%dT%H:%M:%SZ"))
                message = commit['commit']['message']
                if data[name].get('commit','') != date:
                    send_text("{}:\n{} commit {}".format(name,date,message), DINGTALK_TOKEN)
                    data[name]['commit'] = date
            time.sleep(1)
            rj = requests.get('https://api.github.com/repos/{}/releases/latest'.format(name), headers=headers, verify=False).json()
            version = rj['name']
            if data[name].get('version','') != version:
                send_text("{}:\nversion {}".format(name,version), DINGTALK_TOKEN)
                data[name]['version'] = version
            time.sleep(1)
        except:
            pass
    rc.set('repos', json.dumps(data))
