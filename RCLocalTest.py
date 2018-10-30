# coding=utf-8

import win32api
from threading import Thread
from queue import Queue

# 模拟MQ的队列，使用Python Queue
my_mq = Queue()


# 模拟PC端程序
def run_PC():
    while True:
        # 从队列里拿出指令
        command = my_mq.get()
        try:
            # 根据ShellExecute()的使用要求，将命令行的第一个参数拆解出来单独传递
            c = command.split(" ")
            c0, c1 = c[0], ' '.join(c[1:])
            # 用ShellExecute()执行指令，达到“运行”命令行的效果（需要安装pywin32模块）
            win32api.ShellExecute(0, 'open', c0, c1, '', 1)

            print("[PC] {} executed.".format(repr(command)))
        except Exception as e:
            # 异常时输出错误信息
            print("[PC] {}".format(str(e)))


# 模拟手机端程序
def run_Mobile():
    while True:
        # 屏幕输入指令
        command = input("[Mobile] Please input a command: ")
        # 把指令放入队列
        my_mq.put(command)

        print("[Mobile] {} sent.".format(repr(command)))


if __name__ == "__main__":
    # 使用线程调度模拟PC端程序
    Thread(target=run_PC, daemon=True).start()
    # 直接调用模拟手机端程序，进行交互
    run_Mobile()
