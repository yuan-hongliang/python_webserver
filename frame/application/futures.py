from frame.execute.http import content_type_dict,http_success

_mold_html="html"
_mold_png="png"
_mold_text="text"
_mold_gif="gif"
_mold_jpg="jpg"
_mold_pdf="pdf"
_mold_word="word"
_mold_xml="xml"

class MediaFile:

    def __init__(self,data=None,mold=_mold_text):
        if not isinstance(data,bytes):
            err="data must be bytes"
            raise Exception(err)
        self.data=data
        self.mold=mold

    def get_http(self):
        if self.data==None:
            pass
        http_head=content_type_dict[self.mold]
        return (http_success+http_head).encode()+self.data

    def get_mold(self):
        return self.mold

    def get_data(self):
        return self.data

    def set_data(self,data):
        if not isinstance(data,bytes):
            err = "data must be bytes"
            raise Exception(err)
        self.data=data

    def set_mold(self,mold):
        self.mold=mold

class Request:
    def __init__(self,head,body,method,address,parameter,url):
        self.head=head
        self.body=body
        self.method=method
        self.address=address
        self.parameter=parameter
        self.url=url
        self.prohibit=False

    def prohibit_this_request(self):
        self.prohibit=True

    def get_prohibit(self):
        return self.prohibit

    def get_head(self):
        return self.head

    def get_body(self):
        return self.body

    def get_method(self):
        return self.method

    def get_address(self):
        return self.address

    def get_parameter(self):
        return self.parameter

    def get_url(self):
        return self.url

    def set_head(self,head):
        self.head=head

    def set_body(self,body):
        self.body=body

    def set_method(self,method):
        self.method=method

    def set_address(self,address):
        self.address=address

    def set_parameter(self,parameter):
        self.parameter=parameter

    def set_url(self,url):
        self.url=url



import abc #利用abc模块实现抽象类

class Filter(metaclass=abc.ABCMeta):
    @abc.abstractmethod #定义抽象方法，无需实现功能
    def before(self,request):
        '''
        在方法执行前启动
        :param request: 请求体
        :return: 加工后后的请求体
        '''
        pass

    @abc.abstractmethod #定义抽象方法，无需实现功能
    def after(self,result):
        '''
        在方法执行后启动
        :param request: 请求体
        :param result: 方法执行后的结果
        :return: 加工后的结果
        '''
        pass

