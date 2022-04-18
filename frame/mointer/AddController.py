import tkinter as tk
from frame.mointer.editor import create_workArea
from tkinter import messagebox
from frame.mointer.listener import this_interface_is_exist,add_mapping
from frame.application.log import iLog

def add_controller(root):
    frame = tk.Frame(root)

    var_path=tk.StringVar()
    frame1 = tk.Frame(frame,height=120,width=550)
    tk.Label(frame1,text="   path:",font=14).place(x=0,y=0,anchor='nw')
    tk.Entry(frame1,font=14,width=30,textvariable=var_path).place(x=120,y=0,anchor='nw')
    #_path.get()

    def var_method_fn():
        var_method.get()
    var_method=tk.StringVar()
    var_method.set('all')
    tk.Label(frame1, text="  method:",font={'',14}).place(x=0,y=30,anchor='nw')
    tk.Radiobutton(frame1,text='all',variable=var_method,value='all',font=14,command=var_method_fn)\
        .place(x=120,y=30,anchor='nw')
    tk.Radiobutton(frame1, text='get', variable=var_method, value='get',font=14,command=var_method_fn)\
        .place(x=180, y=30, anchor='nw')
    tk.Radiobutton(frame1, text='post', variable=var_method, value='post',font=14,command=var_method_fn)\
        .place(x=240, y=30, anchor='nw')

    var_parameter=tk.StringVar()
    tk.Label(frame1, text="parameter:", font={'', 14}).place(x=0, y=60, anchor='nw')
    tk.Entry(frame1,font=14,width=30,textvariable=var_parameter).place(x=120, y=60, anchor='nw')
    var_returnData = tk.StringVar()
    tk.Label(frame1, text="returnData:", font={'', 14}).place(x=0, y=90, anchor='nw')
    tk.Entry(frame1, font=14, width=30, textvariable=var_returnData).place(x=120, y=90, anchor='nw')

    frame1.pack(pady=10,padx=10)
    frame1.pack_propagate(0)


    frame2 = tk.Frame(frame,height=300,width=550)
    workArea = create_workArea(frame2)
    frame2.pack()
    frame2.pack_propagate(0)

    def submit():
        if var_path.get()=='':
            messagebox.askokcancel(title='注意',message="path不能为空")
            return
        if var_returnData.get()=='':
            messagebox.askokcancel(title='注意',message="returnData不能为空")
            return

        name=var_path.get()
        method=var_method.get()
        que="这个接口已经存在，如果继续将覆盖原来的的代码"
        if this_interface_is_exist(name,method) and not messagebox.askyesno(title='注意',message=que):
            return
        elif not messagebox.askyesno(title='注意',message="你将添加一个新的接口，添加后将无法删除"):
            return
        parameter = var_parameter.get()
        code = workArea.get(1.0, 'end')
        return_data = var_returnData.get()
        fn=create_new_fn(code, parameter, return_data)
        iLog("添加了一个controller\n"+name+"---"+method+'\n'+code)
        add_mapping(name,fn,method)
        que=name+"接口已被添加"+"，接口类型为"+method+"\n点击‘是’将会清空界面"
        if messagebox.askyesno(title='注意', message=que):
            clear()

    def clear():
        if messagebox.askyesno(title='注意',message='你将清空你输入的内容，确定继续吗'):
            var_parameter.set('')
            var_path.set('')
            var_method.set('all')
            var_returnData.set('')
            workArea.delete('1.0','end')

    frame3 = tk.Frame(frame,height=50,width=550)
    tk.Button(frame3,text='submit',font=14,command=submit).pack(padx=100,side='left')
    tk.Button(frame3, text='clear',font=14,command=clear).pack(padx=100,side='right')
    frame3.pack()
    frame3.pack_propagate(0)

    return frame


def add_filter(root):
    frame = tk.Frame(root)

    return frame



def create_new_fn(code,parameter,returnData):
    par = parameter.split(',')
    code +='''\n_system_mapping_return_data = '''+returnData+"\n"
    task = '''class Task:
'''
    scope = {'function': code}

    funName="def task(self"
    funScope = "scope={"
    for item in par:
        funName += ","+item
        funScope += "'"+item+"':"+item+','
    funName+="):\n"
    funScope+="}\n"

    task+="    "+funName+"        "+funScope+'''
        exec(function,scope)
        return scope['_system_mapping_return_data']
fn=Task().task
    '''
    # print(code)
    # print(task)

    exec(task, scope)


    return scope["fn"]




