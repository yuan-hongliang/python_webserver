par=('name','pwd')
function='''
import math
def ppp():
    print(math.pi)
    print("hhhhhh")
ppp()
print("hello world by "+name)'''+"\nreturnData = name"
# task='''
# class Task:
#     def printf(self,name):
#         scope={'name':name}
#         exec(function,scope)
#         return scope['returnData']
# fn=Task().printf
# '''
# scope={'function':function}
#
#
# code='''
# class Task:'''+'''
#     def printf(self,name):'''+'''
#         scope={'name':name}
#         exec(function,scope)
#         return scope['returnData']
# '''
# print({'name':'sss',})
# # exec(task,scope)
# #
# # fn=scope["fn"]
# # print(fn)
# # print(fn("袁洪亮"))
# #
# # tt={
# #     'yuan':111,
# #     'hong':234
# # }
# # print(len(tt))
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
root = Tk()
root.title('notebook_test')
# root.iconbitmap('fa.ico') #设置左上角小图标
root.geometry('700x550+200+100')
# root.resizable(0, 0) #设置窗口不可变

myframe = Frame(root, relief = GROOVE, width = 384, height = 512)
myframe.place(relx = 0, rely = 0)
canbot = Canvas(myframe, bg='white', height=512, width=360, confine=False)
canbot.place(relx = 0, rely = 0)
frame = Frame(canbot, width=360, height = 300, bg = 'white')
canbot.create_window((0, 0), window = frame,anchor = 'nw')

vbar = Scrollbar(myframe, orient = VERTICAL, takefocus = 0.5)
vbar.place(relwidth = 0.05, relheight = 1, relx = 0.9375, rely = 0)
vbar.config(command = canbot.yview)
canbot.config(yscrollcommand = vbar.set)

root.mainloop()