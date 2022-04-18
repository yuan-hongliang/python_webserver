import time
from frame.execute.parse import *
from frame.execute.http import *
from frame.application.futures import MediaFile
from frame.mointer.listener import inc_mapping_map,record_visitor_ip
from frame.application.log import eLog
import traceback

#503 Service Unavailable

def start_response(conn,address,get_mapping,post_mapping,filter_dict,reject_list):
    try:
        result=http_servererror
        '''
        接受传递的参数，
        将其解析打包
        '''
        request = parse_request(conn.recv(1024).decode(),address)
        '''
        记录访问者ip
        '''
        record_visitor_ip(request.get_address()[0])
        '''
        拒绝该请求
        '''
        if request.get_address()[0] in reject_list:
            request.prohibit_this_request()
        '''
        处理Filter.before()
        '''
        if not request.get_prohibit():
            request = execute_filter_before(request,filter_dict)
        '''
        先判断请求是否被阻止
        '''
        if request.get_prohibit():
            result = http_serverforbidden
        #判断是get请求还是post请求
        elif request.get_method()=="GET":
            # print("执行了一个get方法")
            result=execute_method(request,get_mapping)
        else:
            # print("执行了一个post方法")
            result=execute_method(request,post_mapping)
    except Exception as ex:
        print(ex)
        eLog(traceback.format_exc())
    finally:
        if not request.get_prohibit():
            result=execute_filter_after(request,filter_dict,result)
        conn.sendall(result)
        conn.close()

def response_failed(conn):
    print("拒绝了一个请求")
    conn.recv(1024).decode()
    conn.sendall(http_busy)
    conn.close()

def execute_filter_before(request,filter_dict):
    '''
    执行filter.before方法
    :param request:
    :param filter_dict:
    :return:
    '''
    #flag循环结束
    flag = False
    '''
    如果request的url不在字典中，
    说明该方法没有被加强，直接退出
    '''
    if request.get_url() not in filter_dict:
        return request
    for filter_method in filter_dict[request.get_url()]:
        for item in filter_dict[request.get_url()][filter_method]:
            clazz = item[0]
            met = item[1]
            if met == 'all' or met == request.get_method().lower():
                '''
                执行方法
                '''
                tem = clazz.before(request)
                '''
                若方法返回结果不为空则赋值给request，说明其已经被覆盖
                '''
                if tem != None:
                    request = tem
                '''
                如果请求被禁止，则直接退出循环
                '''
                if request.get_prohibit():
                    flag = True
                    break
        if flag: break
    return request

def execute_filter_after(request,filter_dict,result):
    '''
    如果request的url不在字典中，
    说明该方法没有被加强，直接退出
    '''
    if request.get_url() not in filter_dict:
        return result
    for filter_method in filter_dict[request.get_url()]:
        for item in filter_dict[request.get_url()][filter_method]:
            clazz = item[0]
            met = item[1]
            if met == 'all' or met == request.get_method().lower():
                tem = clazz.after(result)
                if tem!=None:
                    result=tem
    return result

def execute_method(request,mapping):
    '''
    在mapping中寻找方法
    若没有找到就返回一个404
    '''
    if request.get_url() not in mapping:
        return http_notfound

    '''
    监听模块数据更新
    '''
    # 记录访问的接口
    inc_mapping_map(request.get_url())
    '''
    获取方法
    '''
    fn = mapping.get(request.get_url())
    '''
    执行方法
    '''
    result = execute_function(fn, request.get_parameter(), request)
    '''
    将方法返回的结果打包
    '''
    result = set_result(result)
    return result


def execute_function(fn,parameter_map,request):
    '''
    按照方法的参数在请求体的参数中寻找，
    若找到则按顺序添加，
    若未找到则将插入一个None值
    若方法的请求参数里有request，则将此参数传给他
    '''
    args = ""
    _count = count = fn.__code__.co_argcount
    for item in fn.__code__.co_varnames:
        if count != _count:
            if item in parameter_map:
                args += "\"" + str(parameter_map[item]) + "\","
            elif item == "request":
                args += "\"" + request + "\""
            else:
                args += "None,"
        count -= 1
        if count == 0: break
    if len(args) > 0:
        args = args[:-1]

    '''
    所有参数以字符串的形式添加到方法后，
    通过eval函数执行
    '''
    # result=eval(fn+"("+args+")")
    if args=="":
        return fn()
    args = eval(args)
    return fn(*args)

def set_result(result):
    if result==None:
        return http_success.encode()

    if isinstance(result,MediaFile):
        return result.get_http()
    '''
    解析返回结果，将结果转换为字符串
    '''
    ty, result = parse_data(result)
    if ty:
        result = http_success + content_type_json + result
    else:
        result = http_success + content_type_text + result
    return result.encode()
