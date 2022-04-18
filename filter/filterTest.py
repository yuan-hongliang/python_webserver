from frame.application.futures import Filter
from frame.application.annotation import webFilter
import frame.application.annotation as ann


@webFilter(value=["/test"],priority=0,method=ann.POST)
class filterTest(Filter):
    def before(self, request):
        print("执行了filter before post")
        return request

    def after(self, result):
        print("执行了filter after post")
        pass


@webFilter(value=["/test"],priority=0,method=ann.GET)
class filterTest22(Filter):
    def before(self, request):
        print(request.get_url(),request.get_address())
        p=request.get_parameter()
        # print(p['name'])
        p['name']='袁洪'
        request.set_parameter(p)
        print("执行了filter before get")
        return request

    def after(self, result):
        print("执行了filter after get")
        pass

@webFilter(value=["/test"],priority=1)
class filterTest_s(Filter):
    def before(self, request):
        print("执行了filter before all")
        return request

    def after(self,  result):
        print("执行了filter after all")
        pass



@webFilter(value="/",priority=2)
class filterTest2(Filter):
    def before(self, request):
        return request

    def after(self, result):
        pass

@webFilter(value="/",priority=2)
class filterTest44(Filter):
    def before(self, request):
        return request

    def after(self, result):
        pass


@webFilter(value=["/hello7"])
class filterTest3(Filter):
    def before(self, request):
        return request

    def after(self, result):
        pass
