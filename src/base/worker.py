# import os
# import time, sys, queue
# from multiprocessing.managers import BaseManager
# class QueueManager(BaseManager):
#     pass


# QueueManager.register("get_task_queue")
# QueueManager.register("get_result_queue")
# server_addr = "127.0.0.1"
# print("Connect to server %s..." % server_addr)
# m = QueueManager(address=(server_addr, 5555), authkey=b"abc")
# m.connect()
# task = m.get_task_queue()
# result = m.get_result_queue()
# for i in range(10):
#     try:
#         n = task.get(timeout=1)
#         print("run task %d  %d..." % (n, n))
#         r = "%d  %d = %d with %s" % (n, n, n * n,os.getpid())
#         time.sleep(1)
#         result.put(r)
#     except queue.Empty:
#         print("task queue is empty.")
# print("worker exit.")


import socket

# 创建一个socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接:
s.connect(("127.0.0.1", 9999))
# 接收欢迎消息:
print(s.recv(1024).decode("utf-8"))
for data in [b"Michael", b"Tracy", b"Sarah"]:
    # 发送数据:
    s.send(data)
    print(s.recv(1024).decode("utf-8"))
s.send(b"exit")
s.close()
