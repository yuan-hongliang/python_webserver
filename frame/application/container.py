

class Container:
    get_mapping={}
    post_mapping={}

    initial_filter_dict = {}
    filter_dict = {}
    reject_ip_list = set()

    HOST = '0.0.0.0'
    POST = 8088
    socket_=None
    thread_poll = None
    request_queue = None
    max_request_queue_len = None





def add_new_interface(name,fn,method='all'):
    '''
    向mapping中添加一个新的接口
    :param name: 接口名，也就是路径名
    :param fn: 方法对象
    :param method: 方法类型
    :return:
    '''
    if method=='get' or method=='all':
        Container.get_mapping[name]=fn
    if method=='post' or method=='all':
        Container.post_mapping[name]=fn

def all_mapping():
    return Container.get_mapping,Container.post_mapping

def set_filter_dict(dic):
    Container.filter_dict = dic

def set_initial_filter(dic):
    Container.initial_filter_dict = dic

def get_filter_dict():
    return Container.filter_dict

def get_initial_filter():
    return Container.initial_filter_dict

def add_reject_list(ip_address):
    '''
    像拦截队列添加一个IP
    :param ip_address:
    :return:
    '''
    Container.reject_ip_list.add(ip_address)

def del_ip_from_reject(ip):
    '''
    从拦截队列中删除一个ip
    :param ip:
    :return:
    '''
    if ip in Container.reject_ip_list:
        Container.reject_ip_list.remove(ip)

def remove_reject_list(ip_address):
    '''
    从拦截队列中删除一个ip
    :param ip_address:
    :return: 删除是否成功
    '''
    if ip_address in Container.reject_ip_list:
        Container.reject_ip_list.remove(ip_address)
        return True
    else:
        return False

def get_reject_list():
    '''
    获取拦截队列
    :return:
    '''
    return Container.reject_ip_list

def set_socket(socket_,HOST='0.0.0.0',POST=8088):
    Container.socket_=socket_
    Container.HOST=HOST
    Container.POST=POST

def get_socket():
    return Container.socket_,Container.HOST, Container.POST

def set_thread_pool(thread_poll):
    Container.thread_poll = thread_poll


def get_thread_pool():
    return Container.thread_poll, Container.thread_poll.get_max_wait_num(), Container.thread_poll.get_max_worker_num()

def set_request_queue(request_queue,max_request_queue_len):
    Container.request_queue = request_queue
    Container.max_request_queue_len = max_request_queue_len

def get_request_queue():
    return Container.request_queue,Container.max_request_queue_len