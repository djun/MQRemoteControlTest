# coding=utf-8

import pika

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

    try:
        # （单机测试时的代码）
        while True:
            # 屏幕输入指令
            command = input("[Mobile] Please input a command: ")
            # 把指令放入队列
            channel.basic_publish(exchange='',
                                  routing_key='mq_cmd',
                                  body=command.encode('utf-8'))

            print("[Mobile] {} sent.".format(repr(command)))
    finally:
        # 退出前关闭MQ连接
        connection.close()
