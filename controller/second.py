from frame.application.annotation import controller
from frame.application.annotation import mapping
from frame.application.annotation import post_mapping
import frame.application.annotation as annotation

@controller
@mapping(value="/second")
class Test:
    @mapping(value="/hello6",method=annotation.GET)
    def test(self):
        print("hello world")
        return "this is test"

    def test2(self):
        print("test2")
    def test3(self):
        print("test3")
    def test4(self):
        print("test4")
    def test5(self):
        print("test5")

@controller
class Test2:
    @post_mapping("/hello7")
    def test(self):
        print("test")
    def test2(self):
        print("test2")
    def test3(self):
        print("test3")
    def test4(self):
        print("test4")
    def test5(self):
        print("test5")