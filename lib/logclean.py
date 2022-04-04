import datetime
import os

#清理日志
def clean_log():
    #设置日志存放路径
    path = 'log\\'
    # 获取当前日期
    today_date = str(datetime.date.today())

    for filename in os.listdir(path):
        file_path = path + filename
        #今天月份
        today_m = int(today_date[5:7])
        # 日志月份
        m = int(filename[9:11])
        #今天年份
        today_y = int(today_date[0:4])
        # 日志年份
        y = int(filename[4:8])

        if(m < today_m):
            if (os.path.exists(file_path)):
                os.remove(file_path)
        elif(y < today_y):
            if (os.path.exists(file_path)):
                os.remove(file_path)