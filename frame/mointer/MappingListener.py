import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.messagebox import showinfo,showerror
from frame.mointer.listener import get_mapping_map

table=None

def create_mapping_listener(root):
    frame=tkinter.Frame(root)

    global table

    tabel_frame = tkinter.Frame(frame)
    tabel_frame.pack()

    xscroll = Scrollbar(tabel_frame, orient=HORIZONTAL)
    yscroll = Scrollbar(tabel_frame, orient=VERTICAL)


    columns = ['id','path', '访问次数']
    columns_width = [100,250,170]
    table = ttk.Treeview(
        master=tabel_frame,  # 父容器
        height=20,  # 表格显示的行数,height行
        columns=columns,  # 显示的列
        show='headings',  # 隐藏首列
        xscrollcommand=xscroll.set,  # x轴滚动条
        yscrollcommand=yscroll.set,  # y轴滚动条
    )
    set_style()
    table.bind('<Double-1>',treeviewClick)
    for column,column_width in zip(columns,columns_width):
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

    return frame

def renew():
    # 插入数据
    info=[]
    i=0
    mapping_map = get_mapping_map()
    mapping_map_sort = sorted(mapping_map.items(),key= lambda x:x[1],reverse=True)
    for item in mapping_map_sort:
        info.append([i,item[0],item[1]])
        i+=1

    for item in table.get_children():
        table.delete(item)

    for index, data in enumerate(info):
        tag='tag_odd' if index%2==1 else 'tag_even'
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

    # 奇偶行设置不同颜色
    table.tag_configure('tag_odd',background='#F5FFFA',foreground='black')
    table.tag_configure('tag_even',background='#F5F5F5',foreground='black')
    # 选中时颜色
    style.map('Treeview',background=[('selected','#00aa00')],foreground=[('selected','white')])

def treeviewClick(event):
    if table.selection() != ():
        selectedItem = table.selection()[0]
        name=table.item(selectedItem,'values')[1]
        showinfo("注意",'你选中了'+name)

def odd_even_color():
    for index,row in enumerate(table.get_children()):
        if index%2==1:
            table.item(row,tags='tag_odd')
        else:
            table.item(row, tags='tag_even')

