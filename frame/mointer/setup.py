import tkinter as tk

from frame.mointer.listener import Listener
from tkinter.messagebox import askyesno
from time import sleep
import threading

def create_setup(root):
    frame = tk.Frame(root)
    modify_thread_pool(frame)

    return frame

def modify_thread_pool(root):
    frame = tk.Frame(root)
    frame.pack(anchor='w',padx=20,pady=20)
    tk.Label(frame, text='修改线程池', font=14,fg = 'red').pack(anchor='w',padx=15)

    progressbarOne = tk.ttk.Progressbar(root, length=200, mode='indeterminate', orient=tk.HORIZONTAL)
    progressbarOne.start()

    def start():
        progressbarOne.pack()
        sleep(1)
        while Listener.Listener_App['thread_pool']:
            sleep(0.1)
            continue
        else:
            progressbarOne.pack_forget()

    frame1 = tk.Frame(frame)
    frame1.pack()
    var_max_num = tk.IntVar()
    var_task_num = tk.IntVar()
    tk.Label(frame1,text='最大线程数：',font=12).grid(row=1,column=1,sticky='w',pady=5,padx=15)
    tk.Entry(frame1,textvariable=var_max_num,font=12).grid(row=1,column=2,sticky='w',pady=5,padx=5)
    tk.Label(frame1, text='等待队列长度：',font=12).grid(row=2,column=1,sticky='w',pady=5,padx=15)
    tk.Entry(frame1, textvariable=var_task_num,font=12).grid(row=2,column=2,sticky='w',pady=5,padx=5)


    def modify():
        if askyesno(title='注意',message='你将修改线程池大小，确定继续吗'):
            t = threading.Thread(target=start)
            t.daemon = True

            Listener.Listener_App['max_num']=int(var_max_num.get())
            Listener.Listener_App['task_num'] = int(var_task_num.get())
            Listener.Listener_App['thread_pool']=True

            t.start()
    # tk.Button(frame,text='修改',compound=modify).pack()
    tk.Button(frame, text='modify', font=14, command=modify).pack(anchor='w',padx=20,pady=10)

