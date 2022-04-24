from frame.application import container
from frame.init import engine
from frame.execute.task import *
from frame.thread.thread_pool import ThreadPoolExecutor
from frame.application.log import init_log_list,storage_all_data
import json
import threading
import os
import tkinter as tk
from frame.mointer.listener import init_listener
from frame.mointer.listenerApp import App
import sys
from time import sleep

'''
标志主程序是否正常运行
'''
_system_is_running=True

def run():
    '''
    服务器启动入口
    :return:
    '''
    # 初始化
    print("正在启动服务器")
    init_()
    '''
    初始化监听模块
    '''
    init_listener()

    print("开始监听请求..............")
    '''
    启动一个线程，开始监听端口
    '''
    t1 = threading.Thread(target=start_server)
    t1.daemon = True
    t1.start()
    '''
    启动第二个线程处理请求
    '''
    t2 = threading.Thread(target=response_request)
    t2.daemon = True
    t2.start()
    '''
    开启第三个线程监控线程池中子线程所有抛出的异常
    '''
    # 不需要了
    '''
    开启第四个线程来监控服务器运行状态
    '''
    t4 = threading.Thread(target=listener_app)
    t4.start()

    '''
    _system_is_running==True时表示程序正常运行中
    当他编程False表示程序正常退出
    '''
    while _system_is_running:
        sleep(0.5)

    '''
    程序正常退出时将log全部持久化保存
    '''
    storage_all_data()
    '''
    程序终止
    '''
    sys.exit()

# 配置文件
application=None
# get方法和post方法
get_mapping,post_mapping=None,None
# 过滤器
filter_dict = None
# 拦截队列
reject_list = None
# 请求队列
request_queue,_request_queue_len=None,None
# 线程池
thread_poll,_max_workers,_wait_queue=None,None,None
# 请求队列满了之后使用这个线程池来拒绝请求
thread_poll_error=None
# socket来凝结
socket,HOST, POST=None,None,None
# 监听者
_max_monitor=1000

def init_():
    pass
    '''
    获取application配置文件的绝对位置
    解析application
    '''
    global application
    application_realpath=os.path.split(os.path.realpath(__file__))[0]+"\\..\\application.json"
    with open(application_realpath, 'r', encoding='UTF-8') as f:
        application = json.load(f)

    '''
    初始化容器
    '''
    engine.init(application)

    '''
    get_mapping get方法的方法列表
    post_mapping post方法的方法列表
    通过init.controller判断扫描的包
    '''
    global get_mapping,post_mapping
    get_mapping,post_mapping = container.all_mapping()

    '''
    filter_list 过滤器列表
    通过init.filter判断扫描的包
    '''
    global filter_dict,reject_list
    filter_dict = container.get_filter_dict()
    reject_list = container.get_reject_list()

    '''
    request_queue 请求队列，最大长度在application.json的 server.request_queue_maximum 设置
    '''
    global request_queue,_request_queue_len
    request_queue,_request_queue_len = container.get_request_queue()

    '''
    初始化日志队列日志队列
    '''
    init_log_list(application)
    print("日志队列初始成功")

    '''
    thread_poll 线程池，可以设置最大线程数和最大任务等待队列
    最大线程数和等待队列在application.json的 server.thread_pool_max_workers和server.wait_queue_maximum设置
    '''
    global thread_poll,_max_workers,_wait_queue,thread_poll_error
    thread_poll,_max_workers,_wait_queue = container.get_thread_pool()
    thread_poll_error = ThreadPoolExecutor(_max_workers//2,_wait_queue//2)
    print("线程池创建成功")

    '''
    创建socket连接
    '''
    global socket,HOST, POST
    socket,HOST, POST = container.get_socket()
    print("socket连接创建成功，服务器启动在"+str(POST)+"端口")

    '''
    可以同时监听多少个请求
    '''
    global _max_monitor
    if "server" in application:
        if "monitor" in application["server"]:
            _max_monitor = int(application["server"]["monitor"])


'''
启动端口并监听请求，将请求放入请求队列
若请求队列已满，则会丢弃请求，并向客户端发送503服务不可用错误
'''
def start_server():
    sem = threading.Semaphore(_max_monitor)
    socket.listen(max(_max_monitor*10,10000))
    with sem:
        while _system_is_running:
            '''
            接受一个请求
            '''
            conn = socket.accept()
            '''
            若请求队列未满，则将请求放入请求池
            '''
            if not request_queue.full():
                request_queue.put(conn,block=True)
            #否则返回一个504服务器繁忙错误
            else:
                conn1,_=conn
                thread_poll_error.put(response_failed,conn)

'''
启动请求相应程序，每次从请求队列中取出一个请求
'''
def response_request():
    while _system_is_running:
        conn,address = request_queue.get(block=True)
        thread_poll.put(start_response,conn,address,get_mapping,post_mapping,filter_dict,reject_list)

'''
启动监控平台
'''
def listener_app():
    root = tk.Tk()
    root.title('系统监控平台')
    # root.iconbitmap('fa.ico') #设置左上角小图标
    root.geometry('800x650+200+100')
    root.minsize(700, 550)
    # root.resizable(0, 0) #设置窗口不可变
    App(root)
    '''
    窗口进入循环监听
    '''
    root.mainloop()
    '''
    窗口退出时意味着程序结束
    '''
    global _system_is_running
    _system_is_running=False
