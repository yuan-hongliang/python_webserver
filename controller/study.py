
from frame.application.annotation import controller,mapping

@controller
@mapping(value='/firstserver')
class FirstServer:
    @mapping(value='hello')
    def hello(self,name):
        data = "hello "+name
        return data


