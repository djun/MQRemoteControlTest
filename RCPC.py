# coding=utf-8

import pika
import win32api


# 接受到消息时的回调函数（里面还是单机测试时的代码）
def callback(ch, method, properties, body):
    command = body.decode('utf-8')

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


if __name__ == "__main__":
    # 连接到MQ
    cred = pika.PlainCredentials("test", "142536")  # 使用测试用户名
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host="X.X.X.X",  # 我的VPS地址
        virtual_host="/testvh",
        heartbeat=600,
        credentials=cred
    ))
    # 开启频道
    channel = connection.channel()
    # 声明消息队列mq_cmd
    channel.queue_declare(queue='mq_cmd')
    # 启动消费队列中的消息，指定回调函数为上面声明好的callback
    channel.basic_consume(callback,
                          queue='mq_cmd',
                          no_ack=True)
    print("[PC] Waiting commands...")
    channel.start_consuming()
