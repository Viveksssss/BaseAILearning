a = 2
b = 2
c = a + 0
c += 2
c -= 2
print(id(a), id(b), id(2))  # id都相同
print(c is b)  # True


astr = "good"
bstr = "good"
cstr = astr + ""
print(cstr is bstr)  # True
print(id(astr), id(bstr), id("good"))  # 三个id相同


a = "aaa"
b = a
c = "aaa"
# a = "bbb"
print(a,b,c)
print(a is b)

lis = [1, 2, 3]
lis2 = [1, 2, 3]
# 虽然它们的内容一样，但是它们指向的是不同的内存地址
print(lis is lis2)
print(id(lis), id(lis2), id([1, 2, 3]))  # 三个id都不同


def singleton(cls):
    instances = {}
    def wrapped(*args,**kwargs):
        if cls not in instances:
            instances[cls] = cls(*args,**kwargs)
        return instances[cls]
    return wrapped

@singleton
class Foo():
    def __init__(self,name):
        self.name = name
        
    def __str__(self):
        return "Foo-%s" % self.name

foo1 = Foo("bos")
foo2 = Foo("aaa")
print(foo1)
print(foo2)


"""

相同点：都是“第一次造，之后返回缓存”
两边核心逻辑一样：

python
if not hasattr(cls, "_instance"):
    cls._instance = ...
return cls._instance
都是“第一次创建并存起来，之后直接返回”。所以 foo1 is foo2 都是 True。

不同点：插手的位置不同
继承版（__new__）	元类版（_
_call__
）
写在哪	普通基类 
Singleton
 的 __new__	元类 Singleton2 的 __call__
用法	class Foo(Singleton)	class Foo2(metaclass=Singleton2)
拦截的是	造对象（Foo.__new__）	调用类（Foo2() 这个动作本身）
谁调 __init__	type.__call__ 每次都会调	第一次调，第二次不调
适合	简单单例，Foo 可以同时继承别的类	需要控制“调用类”整个流程，或不想污染继承链
关键区别：第二次 Foo2() 时 __init__ 会不会跑
这是最实质的差别。

继承版：

python
class Singleton:
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls)
        return cls._instance

class Foo(Singleton):
    def __init__(self):
        print("Foo.__init__ 被调用")

Foo()
Foo()
输出：

text
Foo.__init__ 被调用
Foo.__init__ 被调用      ← 第二次也调了！
因为 Foo() 走的是默认 type.__call__，它先调 Foo.__new__（返回缓存），然后仍然调 Foo.__init__(缓存对象)。__init__ 被反复执行，如果有副作用（重置属性、打开文件），会出问题。

元类版：

python
class Singleton2(type):
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance

class Foo2(metaclass=Singleton2):
    def __init__(self):
        print("Foo2.__init__ 被调用")

Foo2()
Foo2()
输出：

text
Foo2.__init__ 被调用
只打印一次。因为第二次 Foo2() 时，Singleton2.__call__ 直接 return cls._instance，根本没走到 type.__call__，所以 __init__ 不会被调用。这是元类版更“干净”的地方：单例对象只初始化一次。
"""

class Singleton2(type):
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(Singleton2, cls).__call__(*args, **kwargs)
        return cls._instance


class Foo2(metaclass = Singleton2):
    pass
foo1 = Foo2()
foo2 = Foo2()

print(foo1 is foo2)  # True
