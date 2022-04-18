import tkinter as tk
from tkinter import ttk
from frame.mointer.mysystem import create_system_frame
from frame.mointer.editor import create_editor
from frame.mointer.AddController import add_controller
from frame.mointer.AddFilter import add_filter
from frame.mointer.MappingListener import create_mapping_listener
from frame.mointer.setup import create_setup
from frame.mointer.address import create_address
from frame.mointer.log import create_log
from frame.mointer.listener import Listener
from frame.init.init_server import get_thread_pool
import threading
import time


class App:
    modify_thread_pool_ = False
    def __init__(self, master):
        self.master=master
        style = ttk.Style()# tabposition='wn'
        Mysky = "#DCF0F2"
        Myyellow = "#F2C84B"
        style.theme_create("dummy", parent="alt", settings={
            "TNotebook": {"configure": {"tabmargins": [2, 15, 2, 2],"tabposition":'wn',}},
            "TNotebook.Tab": {
                "configure": {"padding": [5, 10], "background": 'white','font':['仿宋', 14],'width':8},
                "map": {"background": [("selected", Mysky)],
                        "expand": [("selected", [1, 1, 1, 0])]}
            }
        })
        style.theme_use("dummy")
        self.notebook = ttk.Notebook(master)
        self.frame1 = create_system_frame(master)
        self.frame2 = create_mapping_listener(master)
        self.frame3 = create_editor(master)
        self.frame4 = create_setup(master)
        self.frame5 = add_controller(master)
        self.frame6 = add_filter(master)
        self.frame7 = create_address(master)
        self.frame8 = create_log(master)

        self.notebook.add(self.frame1, text='system',padding=10)
        self.notebook.add(self.frame2, text='listener',padding=10)
        self.notebook.add(self.frame7, text='address', padding=10)
        self.notebook.add(self.frame5, text='controller', padding=10)
        self.notebook.add(self.frame6, text='filter', padding=10)
        self.notebook.add(self.frame8, text='log', padding=10)
        self.notebook.add(self.frame3, text='editor', padding=10)
        self.notebook.add(self.frame4, text='setup',padding=10)
        self.notebook.pack(padx=10, pady=5, fill=tk.BOTH, expand=True,side='left')

        t = threading.Thread(target=self.modify)
        t.daemon = True
        t.start()



    def create_scroll(self,root):
        canvas = tk.Canvas(root)  # 创建canvas
        vbar = tk.Scrollbar(canvas, orient=tk.VERTICAL)  # 竖直滚动条
        vbar.place()
        vbar.configure(command=canvas.yview)
        hbar = tk.Scrollbar(canvas, orient=tk.HORIZONTAL)  # 水平滚动条
        hbar.place()
        hbar.configure(command=canvas.xview)
        canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)  # 设置
        return canvas

    def modify(self):
        while True:
            time.sleep(1)
            if Listener.Listener_App['thread_pool']:
                thread_pool, _,_ = get_thread_pool()
                thread_pool.modify_size(Listener.Listener_App['max_num'],Listener.Listener_App['task_num'])
                self.notebook.forget(0)
                self.frame1 = create_system_frame(self.master)
                self.notebook.insert(0,self.frame1, text='system',padding=10)
                Listener.Listener_App['thread_pool']=False

        pass



# root = tk.Tk()
# root.title('notebook_test')
# # root.iconbitmap('fa.ico') #设置左上角小图标
# root.geometry('700x500+200+100')
# root.minsize(550,350)
# # root.resizable(0, 0) #设置窗口不可变
# App(root)
# root.mainloop()