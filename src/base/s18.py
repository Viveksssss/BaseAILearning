# # # # from __future__ import annotations
# # # # import asyncio

# # # # import time
# # # # from typing import Any, Callable, Coroutine


# # # # async def hello_coroutine():
# # # #     print("start")
# # # #     await asyncio.sleep(2)
# # # #     print("协程内部代码被执行")


# # # # async def task(name, delay):
# # # #     print(f"任务{name} 启动, 需要等待 {delay} s")
# # # #     await asyncio.sleep(delay)
# # # #     print(f"任务{name} 执行完毕")
# # # #     return f"{name} 执行结果"


# # # # async def gather_main():
# # # #     start = time.time()
# # # #     # 打包所有协程，等待他们都执行结束
# # # #     result_list = await asyncio.gather(
# # # #         task("A", 2),
# # # #         task("B", 3),
# # # #         task("C", 1),
# # # #     )
# # # #     print(f"所有任务返回结果: ", result_list)
# # # #     print(f"总耗时: {time.time() - start:.2f} s")


# # # # # 启动事件循环，调用gather main协程
# # # # asyncio.run(gather_main())


# # # # """
# # # # 这里是串行

# # # # """
# # # # # async def async_seq_main():
# # # # #     # 也可不包裹成任务 直接等待协程执行结束
# # # # #     t1 = task("C", 3)
# # # # #     t2 = task("D", 5)
# # # # #     # 相当于串行
# # # # #     res3 = await t1
# # # # #     res4 = await t2


# # # # # asyncio.run(async_seq_main())


# # # # def get_coroutine()->Callable[[int],Coroutine[Any,Any,str]]:
# # # #     async def get_res(value:int)->str:
# # # #         print("Strat")
# # # #         await asyncio.sleep(value)
# # # #         return "asd"
# # # #     return get_res
# # # # t1 = get_coroutine()
# # # # print(asyncio.run(t1(3)))


# # # import asyncio


# # # async def task(name, delay):
# # #     print(f"任务{name} 启动, 需要等待 {delay} s")
# # #     await asyncio.sleep(delay)
# # #     print(f"任务{name} 执行完毕")
# # #     return f"{name} 执行结果"


# # # async def main():
# # #     # 创建耗时5s的长任务
# # #     t = asyncio.create_task(task("耗时任务", 5))
# # #     # 等待1s后取消任务
# # #     await asyncio.sleep(1)
# # #     # 取消协程t的任务
# # #     t.cancel()
# # #     try:
# # #         # 执行任务会报错
# # #         await t
# # #     except asyncio.CancelledError:
# # #         print("协程任务已被手动取消")


# # # asyncio.run(main())


# # import asyncio
# # import aiohttp

# # # sem = asyncio.Semaphore(3)


# # # async def crawl_page(session: aiohttp.ClientSession, url):
# # #     async with session.get(url) as resp:
# # #         html = await resp.text()
# # #         print(f"{url}字节大小:{len(html)}")


# # # async def main():
# # #     async with aiohttp.ClientSession() as session:
# # #         url_list = ["https://baidu.com"] * 8
# # #         tasks = [crawl_page(session,url) for url in url_list]
# # #         await asyncio.gather(*tasks)

# # # asyncio.run(main())


# # # event = asyncio.Event()
# # # async def wait_event_task():
# # #     print("start")
# # #     await event.wait()
# # #     print("end")

# # # async def send_event_task():
# # #     await asyncio.sleep(3)
# # #     print("after 3 s")
# # #     event.set()

# # # async def main():
# # #     t1 = asyncio.create_task(wait_event_task())
# # #     t2 = asyncio.create_task(send_event_task())
# # #     await t1
# # #     await t2

# # # asyncio.run(main())


# # # import asyncio

# # # # 异步队列：存放生产的数据，设置最大容量3（缓冲区大小）
# # # queue = asyncio.Queue(maxsize=3)


# # # # 生产者协程
# # # async def producer():
# # #     for i in range(6):  # 一共生产6个商品
# # #         item = f"商品-{i}"
# # #         # 队列满时，此处会自动暂停协程，让出事件循环
# # #         await queue.put(item)
# # #         print(f" 生产者：生产 {item}，当前队列大小：{queue.qsize()}")
# # #         await asyncio.sleep(0.5)  # 模拟生产耗时


# # # # 消费者协程
# # # async def consumer():
# # #     while True:
# # #         # 队列为空时，协程阻塞等待数据
# # #         item = await queue.get()
# # #         print(f" 消费者：消费 {item}，剩余队列：{queue.qsize()}")
# # #         await asyncio.sleep(1)  # 模拟消费耗时
# # #         queue.task_done()  # 标记一个任务消费完成


# # # async def main():
# # #     # 创建生产者、消费者任务
# # #     prod_task = asyncio.create_task(producer())
# # #     cons_task = asyncio.create_task(consumer())

# # #     # 等待生产者全部生产完毕
# # #     await prod_task
# # #     # 等待队列里所有剩余商品全部被消费完
# # #     await queue.join()
# # #     # 取消无限循环的消费者任务
# # #     cons_task.cancel()


# # # if __name__ == "__main__":
# # #     asyncio.run(main())


# # import aiohttp
# # import asyncio

# # # 全局配置
# # MAX_CONCURRENT = 2
# # sem = asyncio.Semaphore(MAX_CONCURRENT)
# # headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}


# # TIMEOUT = aiohttp.ClientTimeout(total=3)  # 请求超时3秒


# # async def fetch_url(session: aiohttp.ClientSession, url: str):
# #     """单个网页异步请求函数"""
# #     async with sem:
# #         try:
# #             async with session.get(url, headers=headers, timeout=TIMEOUT) as resp:
# #                 page_html = await resp.text()
# #                 return f"✅ {url} | 状态码:{resp.status} | 页面长度:{len(page_html)}"
# #         except Exception as e:
# #             return f"❌ {url} | 请求失败: {str(e)}"


# # async def main():
# #     # 待爬取链接列表
# #     url_list = [
# #         "https://llfc.club",
# #         "https://www.baidu.com",
# #         "https://www.bing.com",
# #         "https://www.qq.com",
# #         "https://www.zhihu.com",
# #         "https://www.163.com",
# #     ]
# #     # 全局复用ClientSession，性能远高于频繁创建会话
# #     async with aiohttp.ClientSession() as session:
# #         task_list = [fetch_url(session, url) for url in url_list]
# #         result_list = await asyncio.gather(*task_list)
# #     # 遍历打印所有爬取结果
# #     for res in result_list:
# #         print(res)
# # if __name__ == "__main__":
# #     asyncio.run(main())


# import asyncio
# from typing import Dict
# import struct
# import asyncio
# from asyncio import Queue

# # 全局业务消息队列：IO协程生产消息，逻辑协程消费消息
# MSG_QUEUE = Queue(maxsize=1000)


# class TLVProtocol:
#     # T=2字节，L=2字节，头部固定4字节
#     HEADER_LEN = 4

#     @classmethod
#     def encode(cls, msg_type: int, body: str) -> bytes:
#         """
#         TLV消息打包：对外发送完整数据包
#         :param msg_type: 消息ID(T)
#         :param body: 业务消息内容(V)
#         :return: 二进制TLV数据包
#         """
#         body_bytes = body.encode("utf-8")
#         body_len = len(body_bytes)
#         # 网络字节序打包：2字节消息类型 + 2字节消息长度
#         header = struct.pack("!HH", msg_type, body_len)
#         return header + body_bytes

#     @classmethod
#     def decode(cls, buffer: bytes) -> tuple[list[dict], bytes]:
#         """
#         TLV消息解包：处理缓冲区数据，解析完整消息，返回未用完的半包数据
#         :param buffer: 累计接收的缓冲区原始字节
#         :return: 完整消息列表、剩余半包数据
#         """
#         messages = []
#         # 循环解析，支持一次多条消息+半包残留
#         while len(buffer) >= cls.HEADER_LEN:
#             # 解析头部，获取消息体长度
#             msg_type, body_len = struct.unpack("!HH", buffer[: cls.HEADER_LEN])
#             total_pkg_len = cls.HEADER_LEN + body_len

#             # 数据不完整，直接退出，保留当前所有数据等待下次接收
#             if len(buffer) < total_pkg_len:
#                 break

#             # 截取完整消息体
#             body_data = buffer[cls.HEADER_LEN : total_pkg_len].decode("utf-8")
#             messages.append(
#                 {"msg_type": msg_type, "body": body_data, "body_len": body_len}
#             )
#             # 截断已解析数据，保留剩余字节继续解析
#             buffer = buffer[total_pkg_len:]
#         return messages, buffer


# # 导入上方TLV工具与全局队列
# # 客户端连接池：保存所有在线客户端读写对象
# CLIENT_POOL: Dict[str, asyncio.StreamWriter] = dict()


# async def client_logic_worker():
#     """
#     全局逻辑处理协程（独立后台线程）
#     专门消费消息队列，执行业务逻辑，不阻塞网络IO
#     """
#     print("业务逻辑处理协程启动成功")
#     while True:
#         # 阻塞获取队列消息
#         msg_info = await MSG_QUEUE.get()
#         client_addr = msg_info["client_addr"]
#         msg_type = msg_info["msg_type"]
#         msg_body = msg_info["body"]

#         # ========== 自定义业务逻辑区域 ==========
#         print(f"【业务处理】客户端{client_addr} 消息类型:{msg_type} 内容:{msg_body}")
#         # 根据消息ID(T)分发不同业务
#         if msg_type == 1:
#             resp_body = f"[聊天回执]已收到消息：{msg_body}"
#         elif msg_type == 2:
#             resp_body = f"[心跳回执]心跳检测正常"
#         else:
#             resp_body = f"[未知指令]暂不支持消息类型{msg_type}"
#         # ======================================

#         # 封装响应消息，交给发送协程
#         if client_addr in CLIENT_POOL:
#             resp_pkg = TLVProtocol.encode(msg_type=msg_type, body=resp_body)
#             writer = CLIENT_POOL[client_addr]
#             writer.write(resp_pkg)
#             await writer.drain()

#         # 标记队列任务完成
#         MSG_QUEUE.task_done()


# async def client_handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
#     """单个客户端连接总调度协程"""
#     client_addr = f"{writer.get_extra_info('peername')}"
#     CLIENT_POOL[client_addr] = writer
#     print(f"新客户端接入：{client_addr}，当前在线：{len(CLIENT_POOL)}")

#     # 客户端私有缓冲区：永久保存半包数据，直至数据接收完整
#     recv_buffer = b""

#     try:
#         while True:
#             # 异步接收数据，单次最大4096字节
#             recv_data = await reader.read(4096)
#             if not recv_data:
#                 break  # 客户端主动断开连接

#             # 累加数据到缓冲区（保留上次半包数据）
#             recv_buffer += recv_data

#             # TLV解析：获取完整消息、剩余半包数据
#             full_msgs, recv_buffer = TLVProtocol.decode(recv_buffer)

#             # 完整消息全部投入逻辑队列，交由后台协程处理
#             for msg in full_msgs:
#                 msg["client_addr"] = client_addr
#                 await MSG_QUEUE.put(msg)

#     except Exception as e:
#         print(f"客户端{client_addr}连接异常：{e}")
#     finally:
#         # 连接断开，清理资源
#         del CLIENT_POOL[client_addr]
#         writer.close()
#         await writer.wait_closed()
#         print(f"客户端{client_addr}已断开，当前在线：{len(CLIENT_POOL)}")


# async def main():
#     # 启动后台业务逻辑协程（常驻运行）
#     asyncio.create_task(client_logic_worker())

#     # 启动TLV-TCP服务
#     server = await asyncio.start_server(client_handle, host="0.0.0.0", port=8888)
#     print("【工业级TLV全双工TCP服务启动成功】")
#     print("服务监听端口：8888 | 协议格式：T(2B)+L(2B)+V(NB)")

#     await server.serve_forever()


# if __name__ == "__main__":
#     asyncio.run(main())


data = 123

val = data.to_bytes(2,'little')

print(val[0])
print(val[1])
