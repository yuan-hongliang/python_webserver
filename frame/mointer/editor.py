import string
from keyword import kwlist as kws
import tkinter
import tkinter.scrolledtext


# print(dir(__builtins__))
bifs=['ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BlockingIOError', 'BrokenPipeError', 'BufferError', 'BytesWarning', 'ChildProcessError', 'ConnectionAbortedError', 'ConnectionError', 'ConnectionRefusedError', 'ConnectionResetError', 'DeprecationWarning', 'EOFError', 'Ellipsis', 'EnvironmentError', 'Exception', 'False', 'FileExistsError', 'FileNotFoundError', 'FloatingPointError', 'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning', 'IndentationError', 'IndexError', 'InterruptedError', 'IsADirectoryError', 'KeyError', 'KeyboardInterrupt', 'LookupError', 'MemoryError', 'ModuleNotFoundError', 'NameError', 'None', 'NotADirectoryError', 'NotImplemented', 'NotImplementedError', 'OSError', 'OverflowError', 'PendingDeprecationWarning', 'PermissionError', 'ProcessLookupError', 'RecursionError', 'ReferenceError', 'ResourceWarning', 'RuntimeError', 'RuntimeWarning', 'StopAsyncIteration', 'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError', 'SystemExit', 'TabError', 'TimeoutError', 'True', 'TypeError', 'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning', 'ValueError', 'Warning', 'WindowsError', 'ZeroDivisionError', '__build_class__', '__debug__', '__doc__', '__import__', '__loader__', '__name__', '__package__', '__spec__', 'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'breakpoint', 'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'compile', 'complex', 'copyright', 'credits', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'exit', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'license', 'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property', 'quit', 'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip']


def create_editor(root):
    frame = tkinter.Frame(root)
    create_workArea(frame)
    return frame

def create_workArea(root):
    def process_key(key):
        current_line_num, current_col_num = map(int, workArea.index(tkinter.INSERT).split('.'))
        # 按下回车键，自动调整缩进
        if key.keycode == 13:
            # 获取上一行输入的内容
            last_line_num = current_line_num - 1
            last_line = workArea.get(f'{last_line_num}.0', tkinter.INSERT).rstrip()
            # 计算最后一行的前导空格数量
            num = len(last_line) - len(last_line.lstrip(' '))
            # 最后一行以冒号结束，或者冒号后面有#单行注释
            if (last_line.endswith(':') or
                    (':' in last_line and last_line.split(':')[-1].strip().startswith('#'))):
                num = num + 4
            elif last_line.strip().startswith(('return', 'break', 'continue', 'pass', 'raise')):
                num = num - 4
            workArea.insert(tkinter.INSERT, ' ' * num)
        # 按下退格键BackSpace
        elif key.keysym == 'BackSpace':
            # 当前行从开始到鼠标位置的内容
            current_line = workArea.get(f'{current_line_num}.0',
                                        f'{current_line_num}. {current_col_num}')
            # 当前光标位置前面的空格数量
            num = len(current_line) - len(current_line.rstrip(' '))
            # 最多删除4个空格
            # 这段代码是按下退格键删除了一个字符之后才执行的，所以还需要再删除最多3个空格
            num = min(3, num)
            if num > 1:
                workArea.delete(f'{current_line_num}.{current_col_num - num} ',
                                f'{current_line_num}. {current_col_num}')
        else:
            lines = workArea.get('0.0', tkinter.END).rstrip('\n').splitlines(keepends=True)
            # 删除原来的内容
            workArea.delete('0.0', tkinter.END)
            # 再把原来的内容放回去，给不同子串加不同标记
            for line in lines:
                # flag1表示当前是否处于单词中
                # flag2表示当前是否处于双引号的包围范围之内
                # flag3表示当前是否处于单引号的包围范围之内
                flag1, flag2, flag3 = False, False, False
                for index, ch in enumerate(line):
                    # 单引号和双引号优先
                    if ch == "'" and not flag2:
                        # 左右引号之间切换
                        flag3 = not flag3
                        workArea.insert(tkinter.INSERT, ch, 'string')
                    elif ch == '"' and not flag3:
                        flag2 = not flag2
                        workArea.insert(tkinter.INSERT, ch, 'string')
                    # 引号之内，直接绿色显示
                    elif flag2 or flag3:
                        workArea.insert(tkinter.INSERT, ch, 'string')
                    # 不是引号，也不在引号之内
                    else:
                        # 当前字符不是字母
                        if ch not in string.ascii_letters:
                            # 但是前一个字符是字母，说明一个单词结束
                            if flag1:
                                flag1 = False
                                # 获取该位置前面的最后一个单词
                                word = line[start:index]
                                # 内置函数，加标记
                                if word in bifs:
                                    workArea.insert(tkinter.INSERT, word, 'bif')
                                # 关键字，加标记
                                elif word in kws:
                                    workArea.insert(tkinter.INSERT, word, 'kw')
                                # 普通字符串，不加标记
                                else:
                                    workArea.insert(tkinter.INSERT, word)
                            # 单行注释，加标记，这一行后面的字符不再处理，全部作为注释内容
                            if ch == '#':
                                workArea.insert(tkinter.INSERT, line[index:], 'comment')
                                break
                            else:
                                workArea.insert(tkinter.INSERT, ch)
                        else:
                            # 一个新单词的开始
                            if not flag1:
                                flag1 = True
                                start = index
                # 考虑该行最后一个字符是字母的情况
                # 正在输入的当前行最后一个字符大部分情况下是字母.
                if flag1:
                    flag1 = False
                    word = line[start:]
                    if word in bifs:
                        workArea.insert(tkinter.INSERT, word, 'bif')
                    elif word in kws:
                        workArea.insert(tkinter.INSERT, word, 'kw')
                    else:
                        workArea.insert(tkinter.INSERT, word)
            # 原来的内容重新着色以后，光标位置会在文本框最后
            # 这一行用来把光标位置移动到指定的位置，也就是正在修改的位置
            workArea.mark_set('insert', f'{current_line_num}.{current_col_num} ')

    workArea = tkinter.scrolledtext.ScrolledText(root, font=('consolas', 16),height=400)

    #side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.BOTH
    workArea.pack(side=tkinter.LEFT, expand=tkinter.YES, fill=tkinter.BOTH)

    def tab_pressed(event: tkinter.Event) -> str:
        # Insert the 4 spaces
        workArea.insert("insert", " " * 4)
        # Prevent the default tkinter behaviour
        return "break"
    workArea.bind("<Tab>", tab_pressed)
    workArea.bind('<KeyRelease>', process_key)

    # 给内置函数、关键字、注释、字符串设置颜色，语法高亮
    workArea.tag_config('bif', foreground='purple')
    workArea.tag_config('kw', foreground='orange')
    workArea.tag_config('comment', foreground='red')
    workArea.tag_config('string', foreground='green')

    return workArea
