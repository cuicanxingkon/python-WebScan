import logging
import os
import sys
import datetime
import colorlog

class CustomLogging:
    ERROR = 900
    SUCCESS = 800
    SYSINFO = 700
    WARNING = 600
    DEBUG=500


log_colors_config = {
    '+': 'cyan',
    '*': 'green',
    '!': 'yellow',
    '-': 'red',
    '#':'white'
}

logging.addLevelName(CustomLogging.SYSINFO, "*")
logging.addLevelName(CustomLogging.SUCCESS, "+")
logging.addLevelName(CustomLogging.ERROR, "-")
logging.addLevelName(CustomLogging.WARNING, "!")
logging.addLevelName(CustomLogging.DEBUG, "#")

today_date=str(datetime.date.today())

filename = 'log/log_'+today_date+'.log'
resultfile='data/result.txt'

LOGGER = logging.getLogger()
OUTPUTLOG = logging.getLogger()
# 创建一个文件控制对象
LOGGER_HANDLER_file = logging.FileHandler(filename,encoding='utf-8')
OUTPUT_HANDLER_file = logging.FileHandler(resultfile,encoding='utf-8')
# 创建一个屏幕控制对象
LOGGER_HANDLER_steeam = logging.StreamHandler(sys.stdout)

FORMATTER_file = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
FORMATTER_output = logging.Formatter('%(message)s')
FORMATTER_steeam=colorlog.ColoredFormatter("%(log_color)s[%(levelname)s] %(message)s",log_colors=log_colors_config)
# 给处理器创建格式
LOGGER_HANDLER_file.setFormatter(FORMATTER_file)
OUTPUT_HANDLER_file.setFormatter(FORMATTER_output)#结果输出
LOGGER_HANDLER_steeam.setFormatter(FORMATTER_steeam)
# 记录器设置处理器
LOGGER.addHandler(LOGGER_HANDLER_file)
LOGGER.addHandler(LOGGER_HANDLER_steeam)
LOGGER.setLevel(CustomLogging.DEBUG)
OUTPUTLOG.addHandler(OUTPUT_HANDLER_file)




class MyLogger:
    @staticmethod
    def success(msg):
        return LOGGER.log(CustomLogging.SUCCESS, msg)

    @staticmethod
    def info(msg):
        return LOGGER.log(CustomLogging.SYSINFO, msg)

    @staticmethod
    def warning(msg):
        return LOGGER.log(CustomLogging.WARNING, msg)

    @staticmethod
    def error(msg):
        return LOGGER.log(CustomLogging.ERROR, msg)

    @staticmethod
    def debug(msg):
        return LOGGER.log(CustomLogging.DEBUG, msg)

    @staticmethod
    def result(msg):
        return OUTPUTLOG.info(msg)