# coding: utf-8
import os
import time
import sys
import argparse
import datetime
from lib.localscan import loadPlugin
from lib.CmsFinger import bannerscan
from lib.logclean import clean_log
from lib.log import MyLogger

def file_read(filename):
    content=[]
    with open(filename, mode='r') as f:
        for url in f:
            url = url.strip("\n")
            content.append(url)
    return content

def list_str(cmslist):
    cmsstr=''
    l=0
    for cms in cmslist:
        l+=1
        if l<len(cmslist):
            cmsstr+=cms+','
        else:
            cmsstr += cms
    return cmsstr

def cmdLineParser():
    parser = argparse.ArgumentParser(description='web漏洞扫描工具',usage='python webscan.py')
    target = parser.add_argument_group("Target")
    target.add_argument("-u", '--url', metavar="", dest="url", type=str, default='',help="目标URL")
    target.add_argument("-r", '--reading',metavar="",dest="reading", type=str, default='',help="扫描给定文件中列出的多个目标")
    module = parser.add_argument_group("Module")
    module.add_argument("-t", '--threads',metavar="",dest="threads",default=5,help="线程大小, 默认为 5")
    module.add_argument("-c", '--cms',metavar="",dest="cms", type=str, default='',help="已知目标网站的CMS，默认会调用CMS识别函数判断")
    module.add_argument("-C", '--CMS',dest="CMS",action='store_true',help="CMS banner判断，只进行简单的判断，不扫描漏洞")
    module.add_argument("-e", '--noedb',dest="noedb",action='store_true',default=False,help="枚举插件而不搜索漏洞")
    module.add_argument("-o", "--output",metavar="",dest="output",help="将输出保存到文件中，默认在data/result.txt")
    module.add_argument("-d", "--dictattack",dest="dictattack",action="store_true", default=False, help="扫描期间运行低强度字典攻击（默认不使用）")
    module.add_argument("-U", "--username", metavar="",dest="username", help="指定用户名字典攻击")
    module.add_argument("-P", "--password",metavar="",dest="password", help="指定密码字典攻击")
    module.add_argument('--user-agent',metavar="",dest="user_agent",default='',help="自定义user-agent")
    module.add_argument('--random-agent',dest="random_agent",action='store_true',default=False,help="随机生成user-agent，默认为False")
    module.add_argument('--proxies',metavar="",dest="proxies",default='',help="添加代理，例：127.0.0.1:8080")
    if len(sys.argv) == 1:
        sys.argv.append('-h')
    args = parser.parse_args()
    return args

def main():
    args = cmdLineParser()
    #删除一个月前的日志
    clean_log()
    f=open("data/result.txt",mode='w')
    f.truncate()
    f.close()
    plugins=''
    plugin_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "plugins")
    pluginlist = os.listdir(plugin_path)
    for plugin in pluginlist:
        if not plugin.startswith('__'):
            plugins+=plugin+'  '
    print("[#] 扩展：" + plugins)
    today_date = str(datetime.date.today())
    if args.output:
        print("[#] 输出文件：" + args.output)
    else:
        print("[#] 输出文件：" + os.getcwd() + '\data\\result.txt')
    print("[#] 日志文件：" + os.getcwd() + "\log\log_" + today_date + ".log")

    urls=[]# url列表
    if args.noedb:
        plugins_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "plugins")
        pluginlist=os.listdir(plugins_path)
        for plugin in pluginlist:
            noedb=""
            if not plugin.startswith('__'):
                noedb=plugin+"内容管理系统插件：\n"
                plugin_path = plugins_path + '\\' + plugin + '\\'
                poclist=os.listdir(plugin_path)
                for poc in poclist:
                    if poc.endswith(".py") and not poc.startswith('__'):
                        noedb+="      "+poc+"\n"
            if noedb:
                MyLogger.success(noedb)
    elif args.url and not args.reading:
        urls=[args.url]
    elif args.reading and not args.url:
        urls = file_read(args.reading)
    else:
        MyLogger.error('输入格式错误,请输入正确格式!')

    #user_agent
    user_agent=['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11']
    if args.user_agent:
        user_agent.remove('')
        user_agent.append(args.user_agent)
    elif args.random_agent:
        user_agent.remove('')
        user_agent=file_read('data/user_agent.txt')
    #代理
    proxies=''
    if args.proxies:
        proxies=args.proxies

    cms_name=[]
    for url in urls:
        if args.CMS:
            try:
                if args.threads:
                    start = datetime.datetime.now()
                    cms_name,banner_all = bannerscan(url,args.threads)
                    end = datetime.datetime.now()
                else:
                    start = datetime.datetime.now()
                    cms_name,banner_all = bannerscan(url)
                    end = datetime.datetime.now()
            except:
                raise EnvironmentError

            if not cms_name:
                cms_name.append('cms扫描结果不存在')

            MyLogger.result('+' * 50)
            MyLogger.result('扫描时间：' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            MyLogger.result("扫描目标：" + url + "\n    扫描结果：\n    banner：" + banner_all + "\n    CMS_finger：" + list_str(cms_name))
            MyLogger.result('+' * 50)

            MyLogger.info('+' * 50)
            MyLogger.info('扫描时间：' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            MyLogger.info("扫描目标：" + url + "\n    扫描结果：\n    banner：" + banner_all + "\n    CMS_finger：" + list_str(cms_name))
            MyLogger.info("扫描时间：" + str((end - start).seconds) + '秒')
            MyLogger.info('+' * 50)

        else:
            if not args.cms:
                try:
                    if args.threads:
                        cms_name,banner_all = bannerscan(url,args.threads)
                    else:
                        cms_name,banner_all = bannerscan(url)
                except:
                    raise EnvironmentError
            else:
                cms_name.append(args.cms)
            if args.dictattack:
                usernamelist=file_read("data/userlist.txt")
                passwordlist=file_read("data/passwdlist.txt")
                loadPlugin(url, cms_name, args.threads,user_agent,proxies, usernamelist, passwordlist)
            elif args.username and args.password:
                username=args.username
                password=args.password
                usernamelist=passwordlist=None
                if type(username) is str:
                    try:
                        usernamelist = [line.strip() for line in open(username)]
                    except IOError:
                        usernamelist = [username]
                if type(password) is str:
                    try:
                        passwordlist = [line.strip() for line in open(password)]
                    except IOError:
                        passwordlist = [password]
                loadPlugin(url, cms_name, args.threads,user_agent,proxies,usernamelist,passwordlist)
            else:
                loadPlugin(url,cms_name,args.threads,user_agent,proxies)

    if args.output:
        try:
            with open(args.output, 'ab') as f:
                f.write(open('data/result.txt', 'rb').read())
        except IOError:
            MyLogger.error('输入文件名'+args.output+'打开出现错误!')


