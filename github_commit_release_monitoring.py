#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import json
import redis
import time
import requests
import traceback
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
    repos = [
        'BeichenDream/Godzilla',
        'tpt11fb/AttackTomcat',
        'LittleBear4/OA-EXPTOOL',
        'ybdt/poc-hub',
        'doimet/AuxTools',
        'guchangan1/All-Defense-Tool',
        'jiaocoll/BeeScan-web',
        'ExpLangcn/InfoSearchAll',
        'tpt11fb/AttackTomcat',
        "0x727/ShuiZe_0x727",
        "yaklang/yakit",
        "b0bac/ApolloScanner",
        "lcvvvv/kscan",
        "broken5/bscan",
        "78778443/QingScan",
        "1in9e/gosint",
        "P1-Team/AlliN",
        "hanc00l/nemo_go",
        "CTF-MissFeng/bayonet",
        "r3curs1v3-pr0xy/vajra",
        "six2dez/reconftw",
        "yogeshojha/rengine",
        "lz520520/railgun",
        "iceyhexman/onlinetools",
        "x364e3ab6/AWVS-13-SCAN-PLUS"
        "projectdiscovery/nuclei", 
        "zan8in/afrog",
        "chaitin/xray",
        "gobysec/Goby",
        "knownsec/pocsuite3",
        "Anonymous-ghost/AttackWebFrameworkTools",
        "jweny/pocassist",
        "zhzyker/vulmap",
        "Liqunkit/LiqunKit_",
        "SummerSec/SpringExploit",
        "wyzxxz/shiro_rce_tool",
        "SummerSec/ShiroAttack2",
        "j1anFen/shiro_attack",
        "c0ny1/FastjsonExploit",
        "wyzxxz/fastjson_rce_tool",
        "mrknow001/fastjson_rec_exploit",
        "joaomatosf/jexboss",
        "rabbitmask/WeblogicScan",
        "0xn0ne/weblogicScanner",
        "0nise/weblogic-framework",
        "threedr3am/dubbo-exp",
        "0x48piraj/Jiraffe",
        "xwuyi/STS2G",
        "HatBoy/Struts2-Scan",
        "kozmer/log4j-shell-poc",
        "BeichenDream/CVE-2022-26134-Godzilla-MEMSHELL",
        "Summer177/seeyon_exp",
        "God-Ok/SeeyonExploit-GUI",
        "xinyu2428/TDOA_RCE",
        "yuanhaiGreg/LandrayExploit",
        "z1un/weaver_exp",
        "Tas9er/EgGateWayGetShell",
        "Dionach/CMSmap",
        "blackbinn/wprecon",
        "wpscanteam/wpscan",
        "n00py/WPForce",
        "zangcc/Aazhen-v3.1",
        "Lotus6/ThinkphpGUI",
        "bewhale/thinkphp_gui_tools",
        "UzJu/Cloud-Bucket-Leak-Detection-Tools",
        "wyzxxz/aksk_tool",
        "jayus0821/swagger-hack",
        "wyzxxz/heapdump_tool",
        "rtcatc/Packer-Fuzzer",
        "BugScanTeam/GitHack",
        "kost/dvcs-ripper",
        "lijiejie/ds_store_exp",
        "admintony/svnExploit",
        "arthaud/git-dumper",
        "obheda12/GitDorker",
        "m4ll0k/SecretFinder",
        "KathanP19/JSFScan.sh",
        "Ice3man543/SubOver",
        "SafeGroceryStore/MDUT",
        "uknowsec/SharpSQLTools",
        "blackarrowsec/mssqlproxy",
        "quentinhardy/odat",
        "n0b0dyCN/redis-rogue-server",
        "Ridter/redis-rce",
        "yuyan-sec/RedisEXP",
        "zyylhn/redis_rce",
        "i11us0ry/goon",
        "shack2/SNETCracker",
        "koutto/web-brutator",
        "yzddmr6/WebCrack",
        "kitabisa/ssb",
        "TheKingOfDuck/fuzzDicts",
        "gh0stkey/Web-Fuzzing-Box",
        "c0ny1/upload-fuzz-dic-builder",
        "danielmiessler/SecLists",
        "sh377c0d3/Payloads",
        "fuzz-security/SuperWordlist",
        "lutfumertceylan/top25-parameter",
        "r35tart/RW_Password",
        "hahwul/dalfox",
        "dwisiswant0/findom-xss",
        "beefproject/beef",
        "WhiteHSBG/JNDIExploit",
        "wyzxxz/jndi_tool",
        "Nefcore/CRLFsuite",
        "HXSecurity/DongTai",
        "wh1t3p1g/tabby",
        "jeremylong/DependencyCheck",
        "ecriminal/phpvuln",
        "github/codeql-cli-binaries",
        "PyCQA/bandit",
        "zsdlove/Hades"
        ]
    data = rc.get('repos')
    if data is None:
        data = {}
    else:
        data = json.loads(data)
    for r in repos:
        if r not in data:
            data[r] = {}
    headers = {"Authorization": "token {}".format(GH_TOKEN)}
    for name in data:
        msg = {}
        try:
            rj1 = requests.get('https://api.github.com/repos/{}'.format(name),
                              headers=headers, verify=False).json()
            msg['description'] = 'description:{}'.format(rj1['description'])
        except:
            pass

        try:
            rj2 = requests.get('https://api.github.com/repos/{}/commits'.format(name),
                              headers=headers, verify=False).json()
            for commit in rj2[:1]:
                date = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(
                    commit['commit']['committer']['date'], "%Y-%m-%dT%H:%M:%SZ"))
                message = commit['commit']['message']
                if data[name].get('commit', '') != date:
                    msg['commit'] = "commit:{}:{}".format(date, message)
                    data[name]['commit'] = date
            time.sleep(1)
        except:
            pass
        try:
            rj3 = requests.get('https://api.github.com/repos/{}/releases/latest'.format(
                name), headers=headers, verify=False).json()
            version = rj3['name']
            if data[name].get('version', '') != version:
                msg['version'] = "version:{}->{}".format(data[name].get('version', ''), version)
                data[name]['version'] = version
            time.sleep(1)
        except:
            pass
        if 'version' in msg or 'commit' in msg:
            send_text('\n'.join([name,msg.get('description',''),msg.get('commit',''),msg.get('version','')]), DINGTALK_TOKEN)
    rc.set('repos', json.dumps(data))
