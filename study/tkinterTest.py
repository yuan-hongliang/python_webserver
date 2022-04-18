from tkinter import *
from tkinter import ttk
import time
#画窗口
root = Tk()
root.geometry('1000x500')
root.resizable(False, False)
graph = Canvas(root, width=1000, height=550, background='black')#后面查点和删点的时候需要画布类
graph.grid()
#初始化点
tracePlot=[20,20,30,30,40,50,56,78]
#实现动态显示
while True:
    t = time.time()
    time.sleep(1)
    tracePlot[3]=int(t % 100) #动态变化的数据
    traceID = graph.create_line(tracePlot, fill='Red', width=2)
    root.update_idletasks()
    root.update()#更新显示
    graphItems = graph.find_all()
    for n in graphItems:
        graph.delete(n) #如果没有删除操作，旧点不消除，新点也会画在上面