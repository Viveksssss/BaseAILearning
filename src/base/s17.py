# with open("src/base/server.py", "r", encoding="utf-8") as f:
#     file_size = f.seek(0,2)
#     print(file_size)
#     f.seek(0,0)
#     chunk_size = 50
#     while True:
#         chunk = f.read(chunk_size)
#         if not chunk:
#             break
#         print(chunk)
#         print("-"*50)


import threading


class A:
    def show(self):
        print("A")


class B:
    def show(self):
        print("B")


class C(A, B):
    pass


c = C()
c.show()
print(C.__mro__)

"""
演示like继承
"""


class Bird:
    def fly(self):
        print("i can fly")


# is 方式继承，Angle一定是Bird
class Angle(Bird):
    def fly(self):
        print("鹰会飞")


# like 方式继承， Go语言特性interface
class Plane:
    def fly(self):
        print("飞机也会飞")


def func_test_bird(bird: Bird):
    bird.fly()


if __name__ == "__main__":
    angle = Angle()
    func_test_bird(angle)
    plane = Plane()
    func_test_bird(plane)


class staticmethod2:
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, objtype=None):
        return self.func


class C:
    @staticmethod2
    def sm(x):
        return x * 2


print(C.sm(2))


class T:
    a = 0
    def __new__(cls):
        print(f"__new__创建:{cls.__name__}")
        return super().__new__(cls)

    def __init__(self):
        print(f"__init__")
        
    def __contains__(self,key):
        if key == "yes":
            return True
        return False
    
    def __iter__(self):
        return self
    
    def __next__(self):
        self.a=self.a+1
        if self.a > 10:
            raise StopIteration
        return self.a
if "ye2s" in T():
    print("yes")

for i in T():
    print(i)


class UniqueLock:
    def __init__(self):
        self.lock = threading.Lock()
        
    def unlock(self):
        self.lock.release()
        
    def __enter__(self):
        print("lock start")
        self.lock.acquire()
        return self
    
    def __exit__(self,exc_type,exc_val,exc_tb):
        print("lock end")
        if self.lock.locked():
            self.lock.release()


lock = UniqueLock()
with lock as l:
    print("123")


class MyDict:
    def __init__(self):
        self.data = {}

    def __str__(self):
        return f"MyDict内容：{self.data}"

    def __repr__(self):
        return f"MyDict({self.data!r})"

    def __len__(self):
        return len(self.data)

    def __getitem__(self, key):
        print(f"正在读取 key：{key}")
        return self.data[key]

    def __setitem__(self, key, value):
        print(f"正在设置 {key} = {value}")
        self.data[key] = value

    def __delitem__(self, key):
        print(f"正在删除 key：{key}")
        del self.data[key]

    def __contains__(self, key):
        return key in self.data

    def __call__(self):
        print("当前数据：", self.data)

    def __iter__(self):
        return iter(self.data)


d = MyDict()

d["name"] = "Tom"
d["age"] = 18

print(d["name"])
print(len(d))
print("age" in d)

for key in d:
    print(key)

d()

del d["age"]

print(d)
print(repr(d))


def out2():
    num1 = 10
    
    def in2():
        nonlocal num1 
        num1 = 20
        
    in2()
    return num1
print(out2())


def outer():
    # 可变对象列表
    data = [1, 2, 3]

    def inner():
        # 仅修改列表内部元素，无整体赋值
        data.append(4)
        print(data)

    return inner


f = outer()
f()
