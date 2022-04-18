import tkinter as tk
import tkinter.scrolledtext
import threading
from frame.application.log import SPLIT_LINE,get_log_list

show_log = None
log_list = None

def create_log(root):
    frame = tk.Frame(root)
    create_show(frame)
    global log_list
    log_list = get_log_list()

    t = threading.Thread(target=add_info)
    t.daemon = True
    t.start()

    return frame

def create_show(root):
    global show_log
    show_log = tkinter.scrolledtext.ScrolledText(root, font=('consolas', 16),height=400,state='disable')# ,state='disable'

    show_log.tag_config('split',foreground='green')
    show_log.tag_config('time',foreground='purple')
    show_log.tag_config('type--info',foreground='blue')
    show_log.tag_config('type--warning',foreground='orange')
    show_log.tag_config('type--error',foreground='red')

    show_log.pack()

def add_info():
    while True:
        data = log_list.get()
        show_log.config(state='normal')

        show_log.see('end')
        current_line_num, current_col_num = map(int, show_log.index(tkinter.INSERT).split('.'))
        if current_line_num>1000:
            show_log.delete('1.0', str(current_line_num-1000)+'.0')


        datas = [item for item in filter(lambda x: x != '', data.split('\n'))]
        show_log.insert('end',datas[0]+'\n','split')
        show_log.insert('end', datas[1]+'\n', 'time')
        show_log.insert('end', datas[2]+'\n', datas[2].strip())
        show_log.insert('end', "\n".join(datas[3:-1])+'\n')
        show_log.insert('end', datas[-1]+'\n\n', 'split')

        show_log.see('end')
        show_log.config(state='disable')

