from frame.application import futures
from frame.application.annotation import controller,mapping
import frame.application.annotation as annotation
from time import sleep
from frame.application.log import iLog,eLog,wLog
import datetime

@controller
@mapping(value="/test")
class Test3:
    @mapping(value="/hello")
    def test(self,name,pwd):
        # data={"name":name,"pwd":pwd,1:1}
        # print(data)
        a=[]
        for i in range(100):
            a.append(name*10000)
        sleep(3)
        # iLog(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "test")
        # wLog(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "test")
        # eLog(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"test")
        # cc = 0/0
        data={
            'name':name,
            'pwd':pwd,
            3:3,
            'method':'get'
        }
        return data
        # return name+pwd


    @mapping(value="/helloll")
    def test2(self):
        with open("C:/Users/86132/Desktop/资源/图片资源/background/一/1589473051347.png", "rb") as f:
            bytes = f.read()
        mediaFile = futures.MediaFile(bytes,futures._mold_png)
        return mediaFile
    def test3(self):
        print("test3")
    def test4(self):
        print("test4")
    def test5(self):
        print("test5")

@controller
class Test4:
    def __init__(self):
        self.aaaaa="a"
    @mapping(value="/hello2",method=annotation.POST)
    def test(self, name, pwd):
        # data={"name":name,"pwd":pwd,1:1}
        # print(data)
        data = {
            'name': name,
            'pwd': pwd,
            3: 3,
            "aaaa":self.aaaaa,
            'method':'post'
        }
        return data
        # return name+pwd
    def test2(self):
        print("test2")
    def test3(self):
        print("test3")
    def test4(self):
        print("test4")
    def test5(self):
        print("test5")

class Test5:
    @mapping(value="/hello3")
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

class Test6:
    @mapping(value="/hello4")
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

@controller
class Test25:
    @mapping(value="/hello5",method=annotation.POST)
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