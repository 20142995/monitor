#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import os
import socket
import requests

DINGTALK_TOKEN = os.getenv('DINGTALK_TOKEN')
HOSTS = os.getenv('HOSTS')


def check(host_port):
    host, port = host_port.split(':')
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((str(host), int(port)))
        sock.close()
        return True
    except:
        return False


def send_text(text, token):
    headers = {'Content-Type': 'application/json'}
    data = {"msgtype": "text", "text": {"content": text},
            "at": {"atMobiles": [], "isAtAll": False}, }
    url = "https://oapi.dingtalk.com/robot/send?access_token={}".format(token)
    r = requests.post(url, json=data, headers=headers)
    return r.json()


fail = []
for host_port in HOSTS.split('\n'):
    if ':' in host_port:
        if not check(host_port):
            fail.append(host_port)
if fail:
    text = '服务监控告警:\n{}\n无法访问'.format('\n'.join(fail))
    send_text(text, DINGTALK_TOKEN)
