# # from multiprocessing import Process,Pool
# # import os
# # import time,random

# # # def processFunc(name):
# # #     print("child process is %s ,pis is %s" % (name,os.getpid()))
# # #     return
# # # if __name__ == "__main__":
# # #     print("parent Process is %s." %(os.getpid()))
# # #     p = Process(target =processFunc,args=('test',))
# # #     print("child will start")
# # #     p.start()
# # #     p.join()
# # #     print("child stop")


# # def long_time_task(name):
# #     print("run task name is %s" % (name))
# #     start = time.time()
# #     time.sleep(random.random() * 3)
# #     end = time.time()
# #     print("Task %s runs %0.2f seconds." % (name, (end - start)))

# # import subprocess

# # if __name__ == "__main__":

# #     print("$ nslookup www.python.org")
# #     r = subprocess.call(["nslookup", "www.python.org"])
# #     print("Exit code:", r)
# # # print("Parent pid is %s" % (os.getpid()))
# # # p = Pool(4)

# # # for i in range(5):
# # #     p.apply_async(long_time_task, args=(str(i),))
# # # print("Waiting all processes!!!")
# # # p.close()
# # # p.join()
# # # print("All subprocess done")


# from multiprocessing import Process, Queue
# import os, time, random


# def write(q):
#     print("Process to Write pid is %s" % (os.getpid()))
#     for i in ["A", "B", "C"]:
#         q.put(i)
#         time.sleep(random.random())


# def read(q):
#     print("Process to Read pid is %s" % (os.getpid()))
#     while True:
#         value = q.get(True)
#         print("Get %s from queue " % (value))


# if __name__ == "__main__":
#     q = Queue()
#     pw = Process(target=write, args=(q,))
#     pr = Process(target=read, args=(q,))
#     pw.start()
#     pr.start()
#     pw.join()
#     pr.terminate()


import threading,time

def loop():
    print("thread %s is running ..." % threading.current_thread().name)
    n = 0
    while n < 5:
        n = n + 1
        print("thread %s >>> %s" % (threading.current_thread().name, n))
        time.sleep(1)
    print("thread %s ended. " % (threading.current_thread().name))


if __name__ == "__main__":
    print("Thread %s is running..." % threading.current_thread().name)
    t = threading.Thread(target=loop, name="LoopThread")
    t.start()
    t.join()
    print("Thread %s ended." % threading.current_thread().name)
