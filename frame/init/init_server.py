import socket
import queue
from frame.thread.thread_pool import ThreadPoolExecutor
# from frame.application.get_applicationJSON import getJson

class Server:
    thread_poll=None
    max_workers=None
    wait_queue=None
    request_queue=None
    max_request_queue_len=None


def get_socket(config):
    '''
    创建socket连接
    :param config:
    :return:
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # with open("../../application.json", 'r', encoding='UTF-8') as f:
    #     config = json.load(f)
    # config = getJson()

    HOST='0.0.0.0'
    POST=8088

    if config.__contains__("server") :

        server=config["server"]

        if server.__contains__("host") :
            HOST=server["host"]

        if server.__contains__("post") :
            if isinstance(server["post"], str):
                POST=int(server["post"])
            else: POST=server["post"]

    s.bind((HOST, POST))
    return (s,HOST, POST)

def get_thread_pool(config=None):
    '''
    初始化线程池
    :param config:
    :return:
    '''
    if config!=None:
        max_workers=50
        wait_queue =50
        if "server" in config:
            if "thread_pool_max_workers" in config["server"]:
                max_workers=int(config["server"]["thread_pool_max_workers"])
            if "wait_queue_maximum" in config["server"]:
                wait_queue=int(config["server"]["wait_queue_maximum"])
        Server.thread_poll = ThreadPoolExecutor(max_workers, wait_queue)
        Server.wait_queue=Server.thread_poll.get_max_wait_num
        Server.max_workers=Server.thread_poll.get_max_worker_num

    return (Server.thread_poll,Server.max_workers(),Server.wait_queue())

def get_request_queue(config=None):
    '''
    初始化请求队列
    :param config:
    :return:
    '''
    if config!=None:
        max_request_queue_len=50
        if "server" in config:
            if "request_queue_maximum" in config["server"]:
                max_request_queue_len = int(config["server"]["request_queue_maximum"])

        Server.request_queue = queue.Queue(max_request_queue_len)
        Server.max_request_queue_len=max_request_queue_len
    return (Server.request_queue,Server.max_request_queue_len)

def get_max_minotor(config):
    '''
    获取最大监听者数量
    :param config:
    :return:
    '''
    _max_minotor=1000
    if "server" in config:
        if "monitor" in config["server"]:
            _max_minotor = int(config["server"]["monitor"])

    return _max_minotor