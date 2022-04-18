import inspect,sys

class FilterDict:
    _initial_filter_dict={}
    _filter_dict={}
    _reject_ip_list=set()

def get_filter_dict(config=None,get_mapping=None,post_mapping=None):
    if config!=None:
        FilterDict._filter_dict=get_filter_dict_(config,get_mapping,post_mapping)
        init_reject_list(config)
    return FilterDict._filter_dict

def get_initial_filter():
    return FilterDict._initial_filter_dict

def init_reject_list(config):
    '''
    初始化拦截队列
    :param config:
    :return:
    '''
    if "init" in config:
        if "reject_this_IP" in config["init"]:
            for item in config["init"]["reject_this_IP"]:
                add_reject_list(item)

def add_reject_list(ip_address):
    '''
    像拦截队列添加一个IP
    :param ip_address:
    :return:
    '''
    FilterDict._reject_ip_list.add(ip_address)

def get_reject_list():
    '''
    获取拦截队列
    :return:
    '''
    return FilterDict._reject_ip_list

def del_ip_from_reject(ip):
    '''
    从拦截队列中删除一个ip
    :param ip:
    :return:
    '''
    if ip in FilterDict._reject_ip_list:
        FilterDict._reject_ip_list.remove(ip)

def remove_reject_list(ip_address):
    '''
    从拦截队列中删除一个ip
    :param ip_address:
    :return: 删除是否成功
    '''
    if ip_address in FilterDict._reject_ip_list:
        FilterDict._reject_ip_list.remove(ip_address)
        return True
    else:
        return False

def get_filter_dict_(config,get_mapping,post_mapping):
    '''
    连接两个mapping并去重
    按照mapping的值去_filter_name中查找是否存在，也就是这个请求是否需要加强
    :param config:
    :param get_mapping:
    :param post_mapping:
    :return:
    '''
    mapping = set(list(get_mapping.keys())+list(post_mapping.keys()))
    _filter_name = get_filter_name(get_all_class(config))
    filter_dict={}

    if "/" in _filter_name:
        filter_dict['/']=_filter_name['/']

    for item in mapping:
        if item in _filter_name:
            if item in filter_dict:
                filter_dict[item].append(_filter_name[item])
            else:
                filter_dict[item]=_filter_name[item]
        index = item.find('/',1)
        if index>0:
            if item[0:index] in _filter_name:
                if item in filter_dict:
                    filter_dict[item].append(_filter_name[item[0:index]])
                else:
                    filter_dict[item] = _filter_name[item[0:index]]

    FilterDict._initial_filter_dict=filter_dict
    '''
    优化
    '''
    return optimization_filter_dict(filter_dict)

def optimization_filter_dict(filter_dict):
    '''
    filter_dict的键为请求名字
    此方法会将他们的值按照确定好的优先级重新组合排序
    :param filter_dict:
    :return:
    '''
    _filter_dict={}
    for item in filter_dict:
        _filter_dict[item]={}
        for ii in filter_dict[item]:
            if ii[1] in _filter_dict[item]:
                _filter_dict[item][ii[1]].append([ii[0],ii[2]])
            else:
                _filter_dict[item][ii[1]]=[[ii[0], ii[2]]]
        sorted(_filter_dict[item])
    return  _filter_dict

def get_filter_name(class_list):
    '''
    获取所有filter类需要加强的请求
    :param class_list:
    :return:
    '''
    filter_name_map={}
    for clazz in class_list:
        if "filter_value" in clazz.__annotations__:
            if clazz.__annotations__["filter_value"]=="/":
                if "/" in filter_name_map:
                    filter_name_map["/"].append([clazz(),clazz.__annotations__["filter_priority"],clazz.__annotations__["filter_method"]])
                else:
                    filter_name_map["/"]=[[clazz(),clazz.__annotations__["filter_priority"],clazz.__annotations__["filter_method"]]]
            else:
                for item in clazz.__annotations__["filter_value"]:
                    '''
                    ‘/’出现在列表中会显得多余，
                    同时如果出现在列表中会给filter字典的创建造成一定麻烦
                    所以干脆在此处禁止列表中出现‘/’
                    要使用‘/’要单独写出
                    '''
                    if item=="/":
                        err = "If filter_value is a list,'/' cannot be in it!"
                        raise Exception(err)

                    #去除多余的斜杠
                    item = item.replace("//", "/")
                    #开头缺少斜杠就加上
                    if item[0]!='/':
                        item='/'+item
                    #去掉尾部的斜杠
                    while item[-1]=='/':
                        item=item[0:-1]

                    if item in filter_name_map:
                        filter_name_map[item].append([clazz(),clazz.__annotations__["filter_priority"],clazz.__annotations__["filter_method"]])
                    else:
                        filter_name_map[item] = [[clazz(),clazz.__annotations__["filter_priority"],clazz.__annotations__["filter_method"]]]
    return filter_name_map

def get_all_class(config):
    '''
    获取所有filter包下的类
    :param config:
    :return:
    '''
    filter_package = []
    if "init" in config:
        if "filter" in config["init"]:
            filter_package = config["init"]["filter"]

    class_list=[]
    for item in filter_package:
        imp_module = __import__(item)
        for name, _ in inspect.getmembers(sys.modules[item], inspect.isclass):
            obj=getattr(imp_module, name)
            class_list.append(obj)
    return class_list
