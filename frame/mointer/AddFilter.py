import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from frame.application.container import get_filter_dict,get_initial_filter


table=None

def add_filter(root):
    frame = tk.Frame(root)
    global table

    tabel_frame = tk.Frame(frame)
    tabel_frame.pack()

    xscroll = tk.Scrollbar(tabel_frame, orient=tk.HORIZONTAL)
    yscroll = tk.Scrollbar(tabel_frame, orient=tk.VERTICAL)

    columns = ['id', 'path', 'filter','priority','method']
    columns_width = [50, 200, 300,50,50]
    table = ttk.Treeview(
        master=tabel_frame,  # 父容器
        height=20,  # 表格显示的行数,height行
        columns=columns,  # 显示的列
        show='headings',  # 隐藏首列
        xscrollcommand=xscroll.set,  # x轴滚动条
        yscrollcommand=yscroll.set,  # y轴滚动条
    )
    set_style()
    table.bind('<Double-1>', treeviewClick)
    info={'id':'项目id','path':'方法路径','filter':'过滤器','priority':'优先级','method':'方法'}
    for column, column_width in zip(columns, columns_width):
        table.heading(column=column, text=column, anchor=tk.CENTER,
                      command=lambda name=column:
                      tk.messagebox.showinfo('', '{}：{}'.format(name,info[name])))  # 定义表头
        table.column(column=column, width=column_width, minwidth=50, anchor=tk.CENTER, )  # 定义列
    xscroll.config(command=table.xview)
    xscroll.pack(side=tk.BOTTOM, fill=tk.X)
    yscroll.config(command=table.yview)
    yscroll.pack(side=tk.RIGHT, fill=tk.Y)
    table.pack(fill=tk.BOTH, expand=True)

    insect()

    return frame


def insect():
    # 插入数据
    info=[]
    i=0
    filter_map = get_initial_filter()
    for item in filter_map:
        for ii in filter_map[item]:
            info.append([i]+[item]+ii)
            i+=1

    for item in table.get_children():
        table.delete(item)

    for index, data in enumerate(info):
        tag='tag_odd' if index%2==1 else 'tag_even'
        table.insert('', tk.END, values=data,tags=tag)  # 添加数据到末尾

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
    if table.selection()!=():
        selectedItem = table.selection()[0]
        path = table.item(selectedItem, 'values')[1]
        name=table.item(selectedItem,'values')[2]
        showinfo("详细",path+"\n"+name)

def odd_even_color():
    for index,row in enumerate(table.get_children()):
        if index%2==1:
            table.item(row,tags='tag_odd')
        else:
            table.item(row, tags='tag_even')

