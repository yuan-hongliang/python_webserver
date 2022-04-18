import inspect
import sys

class_list=[]
class Mapping:
    _get_mapping={}
    _post_mapping={}

def all_mapping(application=None):
    if application!=None:
        get_all_class(application)
        Mapping._post_mapping=post_mapping()
        Mapping._get_mapping=get_mapping()
    return (Mapping._get_mapping,Mapping._post_mapping)

def get_mapping():
    return mapping("get")

def post_mapping():
    return mapping("post")

def mapping(method):
    '''
    这个方法将判断是否为controller类
    同时类中的方法是否有mapping注解
    按照mapping注解的value值以键值对的形式存入字典
    值便是对应的反射，
    使用时直接从对应的get或post队列中取出即用
    :param method:
    :return:
    '''
    mappingDir={}
    for clazz in class_list:

        functionList=[e for e in dir(clazz) if not e.startswith('_')]

        for fn in functionList:

            func=eval("clazz()."+fn)
            # func = clazz.fn

            anno = func.__annotations__
            '''
            此处会判断该方法是否为所要求的
            '''
            if "mapping_value" in anno and (anno["mapping_method"]=="null" or anno["mapping_method"]==method):

                value = func.__annotations__["mapping_value"]

                if "mapping_value" in clazz.__annotations__:
                    value=clazz.__annotations__["mapping_value"]+"/"+value

                #去除多余的斜杠
                value = value.replace("//", "/")
                #开头却上斜杠就加上
                if value[0]!='/':
                    value='/'+value
                #去掉尾部的斜杠
                while value[-1]=='/':
                    value=value[0:-1]

                if mappingDir.__contains__(value):
                    err=str(func.__code__)+"\n"+"="*10+">There are multiple identical 'mapping value'!"
                    raise Exception(err)

                mappingDir[value]=func

    return mappingDir

def get_all_class(application):
    '''
    获取所有controller类
    :param application:
    :return:
    '''
    page_list=["controller"]
    if "init" in application:
        if "controller" in application["init"]:
            page_list=application["init"]["controller"]

    for item in page_list:
        imp_module = __import__(item)
        for name, _ in inspect.getmembers(sys.modules[item], inspect.isclass):
            obj=getattr(imp_module, name)
            class_list.append(obj)

def add_new_interface(name,fn,method='all'):
    '''
    向mapping中添加一个新的接口
    :param name: 接口名，也就是路径名
    :param fn: 方法对象
    :param method: 方法类型
    :return:
    '''
    if method=='get' or method=='all':
        Mapping._get_mapping[name]=fn
    if method=='post' or method=='all':
        Mapping._post_mapping[name]=fn



