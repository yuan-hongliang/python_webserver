import tkinter as tk
import tkinter.ttk
from frame.init.init_server import get_thread_pool,get_request_queue
import threading
from time import sleep
from frame.mointer.listener import get_visit_count,get_system_info

thread_pool= None
max_num= None
wait_queue = None
request_queue= None
request_queue_len = None

def create_system_frame(root):
    global thread_pool, max_num, wait_queue,request_queue, request_queue_len
    thread_pool, max_num, wait_queue = get_thread_pool()
    request_queue, request_queue_len = get_request_queue()
    frame = tk.Frame(root)

    add_head(frame)

    add_progressbar(frame)

    add_bottom_info(frame)

    return frame

def add_head(frame):
    frame1 = tk.Frame(frame)
    tk.Label(frame1, text="线程池做大线程数：" + str(max_num),font=12).pack()
    tk.Label(frame1, text="响应队列长度：" + str(wait_queue),font=12).pack()
    tk.Label(frame1, text="等待响应队列长度：" + str(request_queue_len),font=12).pack()
    frame1.pack(pady=30)

def add_progressbar(frame):
    frame2 = tk.Frame(frame)
    A = tkinter.ttk.Style()
    A.configure("my0.Horizontal.TProgressbar", troughcolor='white', background='lightblue')

    progressbar1 = tkinter.ttk.Progressbar(frame2, orient=tkinter.VERTICAL, length=200,
                                           style="my0.Horizontal.TProgressbar")
    progressbar1.grid(row=1, column=1, padx=30, pady=10)
    progressbar1['maximum'] = thread_pool.get_max_worker_num()
    progressbar1['value'] = thread_pool.get_free_list_num()
    var1 = tk.StringVar()
    tk.Label(frame2, textvariable=var1).grid(row=2, column=1)
    tk.Label(frame2, text="空闲线程").grid(row=3, column=1)

    progressbar2 = tkinter.ttk.Progressbar(frame2, orient=tkinter.VERTICAL, length=200,
                                           style="my0.Horizontal.TProgressbar")
    progressbar2.grid(row=1, column=2)
    progressbar2['maximum'] = thread_pool.get_max_worker_num()
    progressbar2['value'] = thread_pool.get_worker_num()
    var2 = tk.StringVar()
    tk.Label(frame2, textvariable=var2).grid(row=2, column=2)
    tk.Label(frame2, text="工作线程").grid(row=3, column=2)

    progressbar3 = tkinter.ttk.Progressbar(frame2, orient=tkinter.VERTICAL, length=200,
                                           style="my0.Horizontal.TProgressbar")
    progressbar3.grid(row=1, column=3)
    progressbar3['maximum'] = wait_queue
    progressbar3['value'] = thread_pool.get_wait_num()
    var3 = tk.StringVar()
    tk.Label(frame2, textvariable=var3).grid(row=2, column=3)
    tk.Label(frame2, text="响应队列").grid(row=3, column=3)

    progressbar4 = tkinter.ttk.Progressbar(frame2, orient=tkinter.VERTICAL, length=200,
                                           style="my0.Horizontal.TProgressbar")
    progressbar4.grid(row=1, column=4)
    progressbar4['maximum'] = request_queue_len
    progressbar4['value'] = request_queue.qsize()
    var4 = tk.StringVar()
    tk.Label(frame2, textvariable=var4).grid(row=2, column=4)
    tk.Label(frame2, text="等待响应队列").grid(row=3, column=4)

    def work_num():
        while True:
            sleep(1)
            num1 = thread_pool.get_free_list_num()
            progressbar1['value'] = num1
            var1.set("{:}%".format(int(num1 / max_num * 100)))

            num2 = thread_pool.get_worker_num()
            progressbar2['value'] = num2
            var2.set("{:}%".format(int(num2 / max_num * 100)))

            num3 = thread_pool.get_wait_num()
            progressbar3['value'] = num3
            var3.set("{:}%".format(int(num3 / wait_queue * 100)))

            num4 = request_queue.qsize()
            progressbar4['value'] = num4
            var4.set("{:}%".format(int(num4 / request_queue_len * 100)))

    t1 = threading.Thread(target=work_num)
    t1.daemon = True
    t1.start()

    frame2.pack()

def add_bottom_info(frame):
    frame_root=tk.Frame(frame)
    frame_root.pack(pady=10)

    var_visit = tk.StringVar()
    var_reject = tk.StringVar()
    var_memery = tk.StringVar()
    var_runtime = tk.StringVar()
    v,r=get_visit_count()
    var_visit.set(v)
    var_reject.set(r)
    def listen_():
        while True:
            sleep(1)
            v, r = get_visit_count()
            var_visit.set(v)
            var_reject.set(r)
            me,ru = get_system_info()
            me/=1024*1024
            if me<1024:
                var_memery.set("{:.2f}MB".format(me))
            else:
                var_memery.set("{:.4f}GB".format(me/1024))

            m, s = divmod(ru, 60)
            h, m = divmod(m, 60)
            d, h = divmod(h, 24)
            var_runtime.set("%d天  %d:%02d:%02d" % (d, h, m, s))
    t = threading.Thread(target=listen_)
    t.daemon = True
    t.start()

    tk.Label(frame_root, text='服务器访问量', font=12).grid(row=1,column=1,sticky='w',pady=5,padx=15)
    tk.Label(frame_root, textvariable=var_visit, font=12,justify='left').grid(row=1,column=2,sticky='w',pady=5,padx=15)

    tk.Label(frame_root, text='被拦截的请求', font=12).grid(row=2,column=1,sticky='w',pady=5,padx=15)
    tk.Label(frame_root, textvariable=var_reject, font=12).grid(row=2,column=2,sticky='w',pady=5,padx=15)

    tk.Label(frame_root, text='系统占用内存', font=12).grid(row=3,column=1,sticky='w',pady=5,padx=15)
    tk.Label(frame_root, textvariable=var_memery, font=12).grid(row=3,column=2,sticky='w',pady=5,padx=15)

    tk.Label(frame_root, text='系统运行时间', font=12).grid(row=4,column=1,sticky='w',pady=5,padx=15)
    tk.Label(frame_root, textvariable=var_runtime, font=12).grid(row=4,column=2,sticky='w',pady=5,padx=15)




