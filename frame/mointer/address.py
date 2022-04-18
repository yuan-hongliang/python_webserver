import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.messagebox import showinfo,showerror,askyesno
from frame.mointer.listener import get_reject,get_visitor,add_reject,del_reject

table=None
reject_set=set()
visitor_map = {}
listbox=None
var_entry=None

def create_address(root):
    global reject_set,visitor_map,table,listbox,var_entry
    frame = Frame(root)

    reject_set = get_reject()
    visitor_map = get_visitor()

    tabel_frame = tkinter.Frame(frame)
    tabel_frame.pack()

    xscroll = Scrollbar(tabel_frame, orient=HORIZONTAL)
    yscroll = Scrollbar(tabel_frame, orient=VERTICAL)

    columns = ['id', 'ip','count', '标记']
    columns_width = [100, 150,150,100 ]
    table = ttk.Treeview(
        master=tabel_frame,  # 父容器
        height=10,  # 表格显示的行数,height行
        columns=columns,  # 显示的列
        show='headings',  # 隐藏首列
        xscrollcommand=xscroll.set,  # x轴滚动条
        yscrollcommand=yscroll.set,  # y轴滚动条
    )
    set_style()
    table.bind('<Double-1>', treeviewClick)
    for column, column_width in zip(columns, columns_width):
        table.heading(column=column, text=column, anchor=CENTER,
                      command=lambda name=column:
                      messagebox.showinfo('', '{}描述信息~~~'.format(name)))  # 定义表头
        table.column(column=column, width=column_width, minwidth=50, anchor=CENTER, )  # 定义列
    xscroll.config(command=table.xview)
    xscroll.pack(side=BOTTOM, fill=X)
    yscroll.config(command=table.yview)
    yscroll.pack(side=RIGHT, fill=Y)
    table.pack(fill=BOTH, expand=True)

    renew()
    btn_frame = Frame(frame)
    btn_frame.pack()
    Button(btn_frame, text='刷新', width=20, command=renew).pack()

    reject_frame=Frame(frame,bg='#F5F5F5')
    reject_frame.pack(pady=30)
    listbox = Listbox(reject_frame,height=15,font=14)
    scr = Scrollbar(reject_frame)
    listbox .config(yscrollcommand=scr.set)
    scr.config(command=listbox .yview)
    scr.pack(side=RIGHT, fill=Y)
    for item in reject_set:
        listbox.insert('end',item)
    listbox.pack(side='left')


    reject_btn_frame=Frame(reject_frame,bg='#F5F5F5')
    reject_btn_frame.pack(side='left')
    var_entry=StringVar()
    Label(reject_btn_frame,text='已被拦截的IP地址',font=14).pack(padx=100,pady=10)
    Button(reject_btn_frame, text='删除', width=20, command=del_reject_ip).pack(padx=100, pady=10)
    Entry(reject_btn_frame,width=20,textvariable=var_entry,font=14).pack(pady=10,padx=100)
    Button(reject_btn_frame, text='添加', width=20, command=insert_reject_ip).pack(padx=100,pady=10)

    return frame

def del_reject_ip():
    if listbox.curselection() and listbox.get(listbox.curselection()) in reject_set\
            and askyesno(title='注意',message='你将从拦截队列中删除这个IP\n'+listbox.get(listbox.curselection())):
        del_reject(listbox.get(listbox.curselection()))
        listbox.delete(ACTIVE)

def insert_reject_ip():
    if var_entry.get() not in reject_set\
            and askyesno(title='注意',message='添加这个IP后，这个IP将不能正常访问你的服务器'):
        listbox.insert('end', var_entry.get())
        add_reject(var_entry.get())

def renew():
    # 插入数据
    info=[]
    i=0
    for item in visitor_map:
        tag = 'reject' if item in reject_set else ''
        info.append([i, item,visitor_map[item], tag])
        i+=1
    for item in table.get_children():
        table.delete(item)

    for index, data in enumerate(info):
        tag = 'reject' if data[3]=='reject' else 'default'
        table.insert('', END, values=data,tags=tag)  # 添加数据到末尾

def set_style():
    style=ttk.Style()
    def fixed_map(option):
        return [elm
                for elm in style.map('Treeview',query_opt=option)
                if elm[:2]!=('!disable','!selected')]
    style.map('Treeview',
              foreground=fixed_map('foreground'),
              background=fixed_map('background'))
    style.configure('Treeview.Heading',font=14)
    style.configure('Treeview',rowheight=20,font=12)

    # 行设置不同颜色
    table.tag_configure('reject',background='red',foreground='black')
    table.tag_configure('default',background='#F5F5F5',foreground='black')
    # 选中时颜色
    style.map('Treeview',background=[('selected','#00aa00')],foreground=[('selected','white')])

def treeviewClick(event):
    if table.selection() != ():
        selectedItem = table.selection()[0]
        name=table.item(selectedItem,'values')[1]
        showinfo("注意",'你选中了'+name)


