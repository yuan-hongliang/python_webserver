GET = "get"
POST = "post"

def controller(clazz):
    clazz.__annotations__["controller"] = "controller"
    return clazz

def mapping(value,method="null"):
    def Mapping(fn):
        fn.__annotations__["mapping_value"]=value
        fn.__annotations__["mapping_method"]=method
        return fn
    return Mapping

def get_mapping(value):
    def Mapping(fn):
        fn.__annotations__["mapping_value"]=value
        fn.__annotations__["mapping_method"]=GET
        return fn
    return Mapping

def post_mapping(value):
    def Mapping(fn):
        fn.__annotations__["mapping_value"]=value
        fn.__annotations__["mapping_method"]=POST
        return fn
    return Mapping

import frame
def webFilter(value='/',priority=1,method="all"):
    def f(clazz):
        '''
        判断该方法是否是Filter的子类，不是则弹出异常
        '''
        if not ischildof(clazz,frame.application.futures.Filter):
            err = "This class must inherit from 'application.futures.Filter' !"
            raise Exception(err)
        '''
        判断value值是否为’/‘或者列表，不是则弹出异常
        '''
        if value=='/' or isinstance(value,list):
            clazz.__annotations__["filter_value"]=value
            clazz.__annotations__["filter_priority"]=priority
            clazz.__annotations__["filter_method"] = method
        else:
            err = "Filter value must be list or '/'  !"
            raise Exception(err)
        return clazz
    return f

def ischildof(obj, cls):
    '''
    判断一个类是否是另一个类的子类
    :param obj: 需要判断的类
    :param cls: 目标类
    :return:
    '''
    try:
        for i in obj.__bases__:
            if i is cls or isinstance(i, cls):
                return True
        for i in obj.__bases__:
            if ischildof(i, cls):
                return True
    except AttributeError:
        return ischildof(obj.__class__, cls)
    return False

