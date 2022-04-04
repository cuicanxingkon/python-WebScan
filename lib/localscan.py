# coding: utf-8
import os
import time
import random
import threading
import importlib
from lib.log import MyLogger
from concurrent.futures import ThreadPoolExecutor, as_completed, FIRST_EXCEPTION, wait, ALL_COMPLETED

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

threadingLock = threading.Lock()
def loadPlugin(url,cmslist,threads,user_agent,proxies,username=None,password=None):
    url = url.strip("/")
    MyLogger.info('+' * 50)
    MyLogger.info('扫描时间：' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    MyLogger.info("扫描目标: %s" % url)
    MyLogger.info("目标CMS:" + list_str(cmslist) + "\t线程大小: " + str(threads))

    MyLogger.result('+' * 50)
    MyLogger.result('扫描时间：' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    MyLogger.result("扫描目标: %s" % url)
    MyLogger.result("目标CMS:" + list_str(cmslist) + "\t线程大小: " + str(threads))

    plugin_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "plugins")
    if not os.path.isdir(plugin_path):
        MyLogger.warning("%s 漏洞库不存在! " % plugin_path)
        raise EnvironmentError
    MyLogger.info("漏洞库所在路径: %s " % plugin_path)

    items1 = os.listdir(plugin_path)

    for cms in cmslist:
        if cms:
            if cms in items1:
                MyLogger.info('正在导入"%s"内容管理系统插件' % cms)
            else:
                MyLogger.error("%s内容管理系统POC，漏洞库未收录！" % cms)
                continue
            plugin_path_cms = plugin_path + '\\' + cms + '\\'

            # 暴力破解
            logindict={}
            if username and password:
                bruteforceplugin=cms+'_bruteforce'

                plugins_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "plugins")
                plugin_path_cms = plugins_path + '\\' + cms + '\\'
                poclist = os.listdir(plugin_path_cms)

                if bruteforceplugin in str(poclist):

                    wordlist_size = len(username) * len(password)
                    MyLogger.info('-' * 50)
                    MyLogger.info("导入破解模块，开始暴力破解")
                    print("[#] 线程: "+str(threads)+" | 字典大小: "+str(wordlist_size))
                    bruteforcemodule = importlib.import_module("plugins." + cms + '.' + bruteforceplugin)
                    executor = ThreadPoolExecutor(max_workers=threads)
                    tasks = [executor.submit(bruteforcemodule.run, ((url,random.choice(user_agent),proxies, u, p))) for u in username for p in password]

                    wait(tasks, return_when=ALL_COMPLETED)
                    MyLogger.success("破解结果：")
                    MyLogger.result("破解结果：")

                    loginfound=0

                    for i in range(len(tasks)):
                        login=tasks[i].result()
                        if isinstance(login,dict):
                            loginfound+=1
                            logindict.update(login)
                            for k in login.keys():
                                MyLogger.success("用户名："+k+"\t密码："+login[k])
                                MyLogger.result("用户名：" + k + "\t密码：" + login[k])
                    if not loginfound:
                        MyLogger.warning("未找到可用的用户名和密码，破解失败！")
                        MyLogger.result("未找到可用的用户名和密码，破解失败！")
                else:
                    MyLogger.warning("该内容管理系统未配置暴力破解插件")
                    MyLogger.result("该内容管理系统未配置暴力破解插件")
            MyLogger.info('-' * 50)
            #漏洞扫描
            MyLogger.info("导入漏洞扫描模块，开始扫描漏洞")
            MyLogger.result("目标网站漏洞扫描结果：")
            items2 = os.listdir(plugin_path_cms)
            executor = ThreadPoolExecutor(max_workers=threads)
            tasks = [executor.submit(Pluginscan, ((url,item,cms,logindict,random.choice(user_agent),proxies))) for item in items2]

            wait(tasks, return_when=ALL_COMPLETED)

        else:
            MyLogger.error("目标网站CMS未识别!")
            MyLogger.result("目标网站CMS未识别!")
            raise EnvironmentError
    MyLogger.success("目标"+url+"扫描完成！")
    MyLogger.info('+' * 50)
    MyLogger.result("目标"+url+"扫描完成！\n"+'+' * 50)

# 扫描
def Pluginscan(items):
    url,item,cms,logindict,user_agent,proxies=items
    if item.endswith(".py") and not item.startswith('__') and 'bruteforce' not in item:
        plugin_name = item[:-3]
        if cms in plugin_name:
            module = importlib.import_module("plugins." +cms+'.'+ plugin_name)
            result = module.run(url,logindict,user_agent,proxies)
            threadingLock.acquire()
            MyLogger.info("导入POC: %s" % plugin_name)
            if result:
                MyLogger.result(result)
                MyLogger.success(result)
            else:
                MyLogger.warning("目标网站未发现 %s 漏洞" % plugin_name)
            threadingLock.release()

