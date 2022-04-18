'''
设置监听者
'''
import threading
import time
from frame.init.init_server import get_thread_pool,get_request_queue
from frame.init.get_mapping import all_mapping,add_new_interface
from frame.init.init_filter import get_reject_list,add_reject_list,del_ip_from_reject
from frame.sitepackage import psutil
import os

class Listener:
    # 内存
    memory_info=0
    # 系统启动时间
    start_time=0
    # get请求
    get_mapping=None
    # post请求
    post_mapping=None
    # 接口访问情况
    mapping_map={}
    # 像城池
    thread_pool=None
    # 访问者
    visitor_ip={}
    # 拦截队列
    reject_ip=None
    # 系统访问情况
    visit_count=0
    # 被拦截的请求数
    reject_count=0
    # 用于重新启动App某个界面
    Listener_App={
        "thread_pool":False,
        "max_num":0,
        "task_num":0
    }
    pass

def init_listener():
    '''
    初始化监听对象
    :return:
    '''
    Listener.start_time=time.time()
    t = threading.Thread(target=count_info)
    t.daemon = True
    t.start()

    get_mapping,post_mapping = all_mapping()

    Listener.get_mapping=get_mapping
    Listener.post_mapping=post_mapping

    mapping = set(list(get_mapping.keys())+list(post_mapping.keys()))
    for item in mapping:
        Listener.mapping_map[item]=0

    Listener.reject_ip = get_reject_list()


def add_mapping(name,fn,method):
    add_new_interface(name,fn,method)
    if name not in Listener.mapping_map:
        Listener.mapping_map[name] = 0

def this_interface_is_exist(name,method='get'):
    '''
    判断接口是否存在于mapping中
    :param name: 接口名
    :param method: 方法
    :return:
    '''
    if method=='all':
        if (name in Listener.get_mapping) or (name in Listener.post_mapping):
            return True
        else:
            return False
    if method=='get':
        if name in Listener.get_mapping:
            return True
        else:
            return False
    if method=='post':
        if name in Listener.post_mapping:
            return True
        else:
            return False

def get_mapping_map():
    return Listener.mapping_map


def inc_mapping_map(path):
    if path in Listener.mapping_map:
        Listener.mapping_map[path]+=1

def record_visitor_ip(ip):
    Listener.visit_count += 1
    if ip in Listener.reject_ip:
        Listener.reject_count+=1
    if ip in Listener.visitor_ip:
        Listener.visitor_ip[ip] +=1
    else:
        Listener.visitor_ip[ip] = 1

def get_visitor():
    return Listener.visitor_ip

def get_reject():
    return Listener.reject_ip

def add_reject(ip):
    add_reject_list(ip)

def del_reject(ip):
    del_ip_from_reject(ip)

def get_visit_count():
    return Listener.visit_count,Listener.reject_count


def count_info():
    '''
    记录程序运行占用的内存情况
    :return:
    '''
    while True:
        time.sleep(1)
        Listener.memory_info=psutil.Process(os.getpid()).memory_info().rss

def get_system_info():
    '''
    获取程序占用的内存和运行时间
    :return:
    '''
    run_time = time.time()-Listener.start_time
    return Listener.memory_info,run_time









