import queue
import threading
import contextlib
import traceback
import datetime

# 创建空对象,用于停止线程
StopEvent = object()

class ThreadPoolExecutor:

    def __init__(self, max_num, max_task_num=None):
        """
        初始化线程池
        :param max_num: 线程池最大线程数量
        :param max_task_num: 任务队列长度
        """
        # 如果提供了最大任务数的参数，则将队列的最大元素个数设置为这个值。
        if max_task_num:
            self.q = queue.Queue(max_task_num)
        # 默认队列可接受无限多个的任务
        else:
            self.q = queue.Queue()
        self.max_task_num = max_task_num
        # 设置线程池最多可实例化的线程数
        self.max_num = max_num
        # 任务取消标识
        self.cancel = False
        # 任务中断标识
        self.terminal = False
        # 已实例化的线程列表
        self.generate_list = []
        # 处于空闲状态的线程列表
        self.free_list = []
    #fn, /, *args, **kwargs
    def put(self, func,/, *args, callback=None):
        """
        往任务队列里放入一个任务
        :param func: 任务函数
        :param args: 任务函数所需参数
        :param callback: 任务执行失败或成功后执行的回调函数，回调函数有两个参数
        1、任务函数执行状态；2、任务函数返回值（默认为None，即：不执行回调函数）
        :return: 如果线程池已经终止，则返回True否则None
        """
        # 先判断标识，看看任务是否取消了
        if self.cancel:
            return
        # 如果没有空闲的线程，并且已创建的线程的数量小于预定义的最大线程数，则创建新线程。
        if len(self.free_list) == 0 and len(self.generate_list) < self.max_num:
            self.generate_thread()
        # 构造任务参数元组，分别是调用的函数，该函数的参数，回调函数。
        w = (func, args, callback,)
        # 将任务放入队列
        self.q.put(w,block=True)

    def generate_thread(self):
        """
        创建一个线程
        """
        # 每个线程都执行call方法
        t = threading.Thread(target=self.call)
        t.start()

    def call(self):
        """
        循环去获取任务函数并执行任务函数。在正常情况下，每个线程都保存生存状态，
        直到获取线程终止的flag。
        """
        # 获取当前线程的名字
        current_thread = threading.currentThread().getName()
        # 将当前线程的名字加入已实例化的线程列表中
        self.generate_list.append(current_thread)
        # 从任务队列中获取一个任务
        event = self.q.get()
        # 让获取的任务不是终止线程的标识对象时
        while event != StopEvent:
            # 解析任务中封装的三个参数
            func, arguments, callback = event
            # 抓取异常，防止线程因为异常退出
            try:
                # 正常执行任务函数
                # result = func(current_thread, *arguments)
                # print("执行任务")
                # print(eval())
                # print(*arguments)
                result = func(*arguments)
                success = True
            except Exception as e:
                # 当任务执行过程中弹出异常
                # if self.exception_list!=None:
                #     now = datetime.datetime.now()
                #     t = now.strftime("%Y-%m-%d %H:%M:%S")
                #     tt = "\n==============================>\n"
                #     self.exception_list.put(tt + t + "\n" + traceback.format_exc() + tt)
                result = None
                success = False
                print(e)
            # 如果有指定的回调函数
            if callback is not None:
                # 执行回调函数，并抓取异常
                try:
                    callback(success, result)
                except Exception as e:
                    pass
            # 当某个线程正常执行完一个任务时，先执行worker_state方法
            with self.worker_state(self.free_list, current_thread):
                # 如果强制关闭线程的flag开启，则传入一个StopEvent元素
                if self.terminal:
                    event = StopEvent
                # 否则获取一个正常的任务，并回调worker_state方法的yield语句
                else:
                    # 从这里开始又是一个正常的任务循环
                    event = self.q.get()
        else:
            # 一旦发现任务是个终止线程的标识元素，将线程从已创建线程列表中删除
            self.generate_list.remove(current_thread)

    def close(self):
        """
        执行完所有的任务后，让所有线程都停止的方法
        """
        # 设置flag
        self.cancel = True
        # 计算已创建线程列表中线程的个数，然后往任务队列里推送相同数量的终止线程的标识元素
        full_size = len(self.generate_list)
        while full_size:
            self.q.put(StopEvent)
            full_size -= 1

    def modify_size(self,max_num, max_task_num=None):
        '''
        该方法将修改线程池大小
        :param max_num: 最大线程数
        :param max_task_num: 等待队列长度
        :return:
        '''
        # 创世关闭线程
        self.close()
        # 等待线程全部退出
        while len(self.generate_list)>0:
            pass
        # 修改等待队列的大小
        if max_task_num:
            self.q = queue.Queue(max_task_num)
        self.max_task_num=max_task_num
        # 修改线程池最大线程数线程数
        self.max_num = max_num
        # 关闭任务取消标志
        self.cancel = False
        # 重新初始化线程列表
        self.generate_list = []
        # 初始化空闲状态的线程列表
        self.free_list = []


    def terminate(self):
        """
        在任务执行过程中，终止线程，提前退出。
        """
        self.terminal = True
        # 强制性的停止线程
        while self.generate_list:
            self.q.put(StopEvent)

    # 该装饰器用于上下文管理
    @contextlib.contextmanager
    def worker_state(self, state_list, worker_thread):
        """
        用于记录空闲的线程，或从空闲列表中取出线程处理任务
        """
        # 将当前线程，添加到空闲线程列表中
        state_list.append(worker_thread)
        # 捕获异常
        try:
            # 在此等待
            yield
        finally:
            # 将线程从空闲列表中移除
            state_list.remove(worker_thread)

    def get_max_worker_num(self):
        '''
        获取最大线程数量
        :return:
        '''
        return self.max_num
    def get_max_wait_num(self):
        '''
        获取最大等待队列长度
        :return:
        '''
        return self.max_task_num

    def get_generate_list_num(self):
        '''
        获取已经创建的线程数量
        :return:
        '''
        return len(self.generate_list)

    def get_free_list_num(self):
        '''
        获取当前空闲线程数
        :return:
        '''
        len1=len(self.generate_list)
        len2=len(self.free_list)
        if len1<self.max_num:
            return self.max_num-(len1-len2)
        return len2

    def get_worker_num(self):
        '''
        获取当前工作线程数
        :return:
        '''
        len1 = len(self.generate_list)
        len2 = len(self.free_list)
        return len1-len2

    def get_wait_num(self):
        '''
        获取等待队列长度
        :return:
        '''
        return self.q.qsize()