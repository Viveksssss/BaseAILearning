""" "
format,map,reduce,filter,sorted
"""

from functools import reduce
import functools
import time

f = abs
print(f(-10))

# f = "abs"
# print(f)


def add(a, b, f):
    return f(a) + f(b)


print(add(-1, 2, f))


def squart(n):
    return n * n


print(map(squart, range(1, 11)))
print(list(map(squart, range(1, 11))))


def func(a, b):
    return a + b


print(reduce(func, range(1, 11)))


def str2int(str):
    def char2int(c):
        return int(c)

    def convertnum(a, b):
        return a * 10 + b

    return reduce(convertnum, map(char2int, str))


print(str2int("325235235235"))


def odd_generator():
    n = 1
    while True:
        n += 2
        yield n


def primer_generator():
    yield 2
    it = odd_generator()
    while True:
        n = next(it)
        yield n
        it = filter(lambda x, p=n: x % p > 0, it)


for i in primer_generator():
    if i < 100:
        print(i)
    else:
        break
print(sorted(["Abert", "Sort", "kill", "Port"], key=str.lower, reverse=True))


"""
    函数延迟调用
"""


def lazy_sum(*arg):
    def sum():
        x = 0
        for i in arg:
            x = i + x
        return x

    return sum


f = lazy_sum(2, 3, 4, 6, 78, 8, 21)
print(f())


def decoratorfunc(param):
    def decoratorfunc2(func):
        @functools.wraps(func)
        def wrappedfunc(*arg, **kw):
            time1 = time.time()
            func(*arg)
            time2 = time.time()
            print("use time %d" % (time2 - time1))

        return wrappedfunc

    return decoratorfunc2


@decoratorfunc("execute")
def helloworld(str):
    print(str)


p = helloworld("helloworld")
print(helloworld.__name__)


intnew = functools.partial(int,base=16)
print(intnew('12'))