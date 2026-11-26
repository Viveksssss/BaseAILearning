# import random, time, queue
# from multiprocessing.managers import BaseManager

# task_queue = queue.Queue()
# result_queue = queue.Queue()


# def taskqueuefunc():
#     global task_queue
#     return task_queue


# def resultqueuefunc():
#     global result_queue
#     return result_queue


# class QueueManager(BaseManager):
#     pass


# def ServerStart():
#     QueueManager.register("get_task_queue", callable=taskqueuefunc)
#     QueueManager.register("get_result_queue", callable=resultqueuefunc)

#     manager = QueueManager(address=("127.0.0.1", 5555), authkey=b"abc")
#     manager.start()

#     task = manager.get_task_queue()
#     result = manager.get_result_queue()

#     for i in range(10):
#         n = random.randint(0, 10000)
#         print("Put Task %d..." % n)
#         task.put(n)

#     print("Try get results")
#     for i in range(10):
#         r = result.get(timeout=10)
#         print("Result:%s" % r)

#     manager.shutdown()

#     print("Server exit")


# if __name__ == "__main__":
#     ServerStart()


import socket
import threading
import time


def tcplink(sock,addr):
    print("Accept new connection from %s:%s..." % addr)
    sock.send(b"Welcome!")
    while True:
        data = sock.recv(1024)
        print("from %s : %s"% (addr.port,data))
        time.sleep(1)
        if not data or data.decode("utf-8") == "exit":
            break
        sock.send(("Hello, %s" % data.decode("utf-8")).encode("utf-8"))
    sock.close()
    print("Connection from %s:%s closed." % addr)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 绑定套接字
s.bind(("127.0.0.1", 9999))
# 监听套接字
s.listen(5)
print("Waiting for connection...")
while True:
    # 接收新的连接
    sock, addr = s.accept()
    # 创建新的线程处理TCP
    t = threading.Thread(target=tcplink, args=(sock, addr))
    t.start()
