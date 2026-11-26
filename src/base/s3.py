g = (x*2 for x in range(1,11))

print(g)

print(next(g))

'''
    Iterator是生成器，可以被next
    Iterable是迭代器，可以被for i in ...
    
    Iterator ∈ Iterable
    Generator 是生成器，所以也是迭代器，可以被迭代取出。
'''

def triangles():
    yield [1]
    yield [1, 1]
    lists = [1, 1]
    while True:
        i = 1
        n = len(lists)
        newlists = [1]
        while i < n:
            newlists.append(lists[i - 1] + lists[i])
            i = i + 1
        newlists.append(1)
        lists = newlists
        yield newlists


from collections.abc import Iterable
from collections.abc import Iterator

b1 = isinstance([], Iterable)
b2 = isinstance([], Iterator)
print("[] is Iteralbe", b1)
print("[] is Iterator", b2)

b1 = isinstance({}, Iterable)
b2 = isinstance({}, Iterator)

print("[] is Iteralbe", b1)
print("[] is Iterator", b2)

b1 = isinstance((x * x for x in range(10)), Iterable)
b2 = isinstance((x * x for x in range(10)), Iterator)
print("x*x for x in range(10) isIterable", b1)
print("x*x for x in range(10) isIterator", b2)

# 可以被next()函数调用并不断返回下一个值的对象称为迭代器：Iterator

b1 = isinstance(triangles(), Iterable)
b2 = isinstance(triangles(), Iterator)
print("triangles()", b1)
print("triangles()", b2)


# for i in triangles():
#     print(i)