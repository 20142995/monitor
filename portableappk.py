#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import os
import requests

PORTABLEAPPK_USER = os.getenv('PORTABLEAPPK_USER')
PORTABLEAPPK_PASSWD = os.getenv('PORTABLEAPPK_PASSWD')
DDDDOCR_URL = os.getenv('DDDDOCR_URL')
DINGTALK_TOKEN = os.getenv('DINGTALK_TOKEN')


def send_text(text, token):
    headers = {'Content-Type': 'application/json'}
    data = {"msgtype": "text", "text": {"content": text},
            "at": {"atMobiles": [], "isAtAll": False}, }
    url = "https://oapi.dingtalk.com/robot/send?access_token={}".format(token)
    r = requests.post(url, json=data, headers=headers)
    return r.json()


def portableappk():
    session = requests.session()
    wp_login_url = "https://portableappk.com/wp-login.php"
    headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"105\", \"Not)A;Brand\";v=\"8\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Upgrade-Insecure-Requests": "1",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.54 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "https://portableappk.com/portable-wps-office/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9"}
    session.get(wp_login_url, headers=headers)
    retry = 0
    while True:
        gen_captcha_img_url = "https://portableappk.com/wp-content/plugins/wordpress-hack-bundle/addons/gen-captcha-img.php"
        headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"105\", \"Not)A;Brand\";v=\"8\"", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.54 Safari/537.36", "Sec-Ch-Ua-Platform": "\"Windows\"",
                   "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Dest": "image", "Referer": "https://portableappk.com/wp-login.php", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9"}
        r1 = session.get(gen_captcha_img_url, headers=headers)
        code = requests.post(
            "{}/ocr/file".format(DDDDOCR_URL), files={'image': r1.content}).text
        # 登录
        headers = {"Cache-Control": "max-age=0", "Sec-Ch-Ua": "\"Chromium\";v=\"105\", \"Not)A;Brand\";v=\"8\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Upgrade-Insecure-Requests": "1", "Origin": "https://portableappk.com", "Content-Type": "application/x-www-form-urlencoded",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.54 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "https://portableappk.com/wp-login.php", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9"}
        login_data = {"log": PORTABLEAPPK_USER, "pwd": PORTABLEAPPK_PASSWD, "phrase": code, "wp-submit": "\xe7\x99\xbb\xe5\xbd\x95",
                      "redirect_to": "https://portableappk.com/wp-admin/", "testcookie": "1"}
        r2 = session.post(wp_login_url, headers=headers,
                          data=login_data, allow_redirects=False)
        if r2.status_code == 302:
            break
        else:
            retry += 1
        if retry > 15:
            send_text("portableappk: 多次尝试登录失败", os.getenv('DINGTALK_TOKEN'))
            break

    retry = 0
    while True:
        # 获取验证码
        headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"105\", \"Not)A;Brand\";v=\"8\"", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.54 Safari/537.36", "Sec-Ch-Ua-Platform": "\"Windows\"",
                   "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "no-cors", "Sec-Fetch-Dest": "image", "Referer": "https://portableappk.com/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9"}
        r3 = session.get(gen_captcha_img_url, headers=headers)
        code = requests.post(
            "{}/ocr/file".format(DDDDOCR_URL), files={'image': r3.content}).text
        # 签到
        verify_checkin_url = "https://portableappk.com/wp-content/plugins/wordpress-hack-bundle/addons/verify-checkin.php"
        headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"105\", \"Not)A;Brand\";v=\"8\"", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.54 Safari/537.36", "Sec-Ch-Ua-Platform": "\"Windows\"", "Content-Type": "application/x-www-form-urlencoded",
                   "Accept": "*/*", "Origin": "https://portableappk.com", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://portableappk.com/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9"}
        qiandao_data = {"phrase": code}
        r4 = session.post(verify_checkin_url,
                          headers=headers, data=qiandao_data)
        if r4.json()['success'] == 1:
            send_text("portableappk: 签到成功\n"+r4.text, DINGTALK_TOKEN)
            break
        else:
            retry += 1
        if retry > 15:
            send_text("portableappk: 签到失败", DINGTALK_TOKEN)
            break


if __name__ == '__main__':
    portableappk()
