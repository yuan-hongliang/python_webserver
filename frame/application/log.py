import queue
from collections import deque
import datetime
import threading
import time

INFO_LOG = 'info'
WARN_LOG = 'warn'
ERROR_LOG = 'error'
SPLIT_LINE = "==============================>"

class Log:
    type_map={INFO_LOG:'type--info',WARN_LOG:'type--warning',ERROR_LOG:'type--error'}
    _storage_address = "log.text"
    _log_max_len = 100
    log_list=queue.SimpleQueue()
    log_deque=deque([])


def init_log_list(_storage_address='log.txt',_log_max_len=100):

    Log._storage_address = _storage_address
    Log._log_max_len = _log_max_len

    '''
    创建一个空的的log文件
    '''
    with open(Log._storage_address, mode='w', encoding='utf-8') as file_obj:
        file_obj.write("服务器启动于："+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"\n")

    '''
    启动一个线程监听log队列，实施保存
    '''
    t = threading.Thread(target=storage_log)
    t.daemon = True
    t.start()

def get_log_list():
    '''
    获取日志队列
    :return:
    '''
    return Log.log_list

def log(text,type):
    '''
    创建一个日志信息
    :param text: 日志内容
    :param type: 日志类型 {INFO_LOG:'type--info',WARN_LOG:'type--warning',ERROR_LOG:'type--error'}
    :return:
    '''
    if type not in Log.type_map:
        err="type must be:"+list(Log.type_map.keys())
        raise Exception(err)
    now = datetime.datetime.now()
    t = now.strftime("%Y-%m-%d %H:%M:%S")
    tt="\n"+SPLIT_LINE+"\n"
    log_info=tt+t+"\n"+Log.type_map[type]+"\n"+text+tt
    Log.log_list.put(log_info)
    Log.log_deque.append(log_info)

def iLog(text):
    '''
    信息类日志
    :param text:
    :return:
    '''
    log(text,INFO_LOG)

def eLog(text):
    '''
    警告类日志
    :param text:
    :return:
    '''
    log(text,ERROR_LOG)

def wLog(text):
    '''
    异常或错误类日志
    :param text:
    :return:
    '''
    log(text,WARN_LOG)

def storage_log():
    '''
    持久化保存日志信息
    当日志队列达到一定长度时，自动将数据持久化保存到硬盘
    :return:
    '''
    while True:
        time.sleep(5)
        while len(Log.log_deque) > Log._log_max_len:
            storage(Log.log_deque.popleft())

def storage(data):
    '''
    打开相应日志文件写入数据
    :param data:
    :return:
    '''
    with open(Log._storage_address, mode='a', encoding='utf-8') as file_obj:
        file_obj.write(data+"\n")

def storage_all_data():
    '''
    将日志队列的数据全部持久化
    :return:
    '''
    while len(Log.log_deque) > 0:
        storage(Log.log_deque.popleft())
