import json
from frame.execute.http import _content_type_form,_content_type_json
from frame.application.futures import Request

def parse_request(request,address):
    method = request.split(" ")[0]
    if method == "GET":
        http_head = request
        http_body = None
        method="GET"
        request_s = request.split(" ")
        # 取出请求体并解析
        url = request_s[1].split("?")
        '''
        获取请求地址，并将其中的”//“转换为”/“，在去掉末尾的”/“
        '''
        url_ = url[0]
        url_ = url_.replace("//", "/")
        while len(url_) > 1 and url_[-1] == "/":
            url_ = url_[:-1]
        '''
        解析请求体中的参数
        若请求中不包含参数，创造一个空的字典
        '''
        if len(url) == 2:
            parameter = url[1]
            parameter_map = parse_parameter_form(parameter)
        else:
            parameter_map = {}
    else:
        method = "POST"
        '''
        按照"\n\r"分离请求，得到http头和请求体
        '''
        request_s = request.split("\n\r")
        http_head = request_s[0]
        http_body = request_s[1]
        # 取出请求体并解析
        http_head_s = http_head.split(" ")
        url_ = http_head_s[1]
        '''
        获取请求地址，并将其中的”//“转换为”/“，在去掉末尾的”/“
        '''
        url_ = url_.replace("//", "/")
        while url_[-1] == "/":
            url_ = url_[:-1]
        '''
        按照请求头获取http的content-type
        '''
        type = parse_http_head_type(http_head)
        '''
        按照content-type类型解析请求体
        '''
        parameter_map = parse_parameter(type, http_body)
    return Request(http_head,http_body,method,address,parameter_map,url_)

'''
通过递归来解析数据
将数据解析为字符串
'''
def parse_data(data):

    if data==None:
        return (False, str(data))
    '''
    如果使字符串直接返回
    '''
    if isinstance(data,str):
        return (False,data)

    '''
    如果是字典，解析字典的每一个值，将其转换为字符串
    并标记is_dict=True
    再借助json.dumps(data)将字典转换为字符串
    '''
    if isinstance(data,dict):
        for key in data.keys():
            _, data[key] = parse_data(data[key])
        # print(data)
        res=json.dumps(data,ensure_ascii=False)
        return (True, res)

    '''
    如果是int和float直接转换
    '''
    if isinstance(data,int) or isinstance(data,float):
        res = str(data)
        return (False, res)

    '''
    如果是列表
    解析每一个元素将他们转换为字符串
    在借助join连接所有元素
    '''
    if isinstance(data,list):
        for i in range(0,len(data)):
            _, data[i] = parse_data(data[i])
        res = ",".join(data)
        res = '{' + res + "}"
        return (True, res)

    '''
    如果是元组或集合
    解析每一个元素将他们转换为字符串，
    然后放入一个列表中,在借助join连接所有元素
    '''
    if isinstance(data,tuple) or isinstance(data,set):
        s=[]
        for item in data:
            _, t = parse_data(item)
            s.append(t)
        res = " ".join(s)
        res='{'+res+"}"
        return (True, res)

    '''
    如果不是基本数据类型
    则认为是类
    通过__dict__获取类的所有成员的字典
    然后便利每一个成员将他们变成字符串
    最后借助json.dumps
    '''
    tmap = data.__dict__
    for key in tmap.keys():
        _, tmap[key] = parse_data(tmap[key])
    res = json.dumps(tmap,ensure_ascii=False)
    return (True,res)

'''
解析请求头，判断请求方式
'''
def parse_http_head_type(http_head):
    type="text/html"
    for item in http_head.split("\n"):
        if item.find(_content_type_form)>=0:
            type="form"
            break
        elif item.find(_content_type_json)>=0:
            type="json"
            break
    return type

'''
解析参数
'''
def parse_parameter(type,parameter):
    parameter=parameter.replace("\n","")
    if type=="json":
        return json.loads(parameter)

    return parse_parameter_form(parameter)



def parse_parameter_form(parameter):
    parameter_map = {}
    for item in parameter.split("&"):
        item_s = item.split("=")
        key = item_s[0]
        value = item_s[1]
        parameter_map[key] = value
    return parameter_map


