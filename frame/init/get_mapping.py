import inspect
import sys
from frame.application.container import add_new_interface

class_list=[]

def init_mapping(application=None):
    get_all_class(application)
    _post_mapping = post_mapping()
    _get_mapping = get_mapping()
    for item in _post_mapping:
        add_new_interface(item,_post_mapping[item],'post')
    for item in _get_mapping:
        add_new_interface(item,_get_mapping[item],'get')
    return _post_mapping,_get_mapping

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




