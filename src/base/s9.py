from datetime import datetime, timedelta, timezone

now = datetime.now()
print(now)
print(type(now))
print(now.timestamp())
print(datetime.fromtimestamp(now.timestamp()))

t = 1429417200.0
print(datetime.utcfromtimestamp(t))


# 字符串转成时间
cday = datetime.strptime("2017-6-1 18:22:22", "%Y-%m-%d %H:%M:%S")
print(cday)


now = datetime.now()
print(now)
print(now + timedelta(hours=10))
print(now + timedelta(days=1))
print(now + timedelta(days=2, hours=12))

# UTC + 8:00
timezone_8 = timezone(timedelta(hours=8))
now = datetime.now()
print(now)
dt = now.replace(tzinfo=timezone_8)
print(dt)


utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
print(utc_dt)
bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
print(bj_dt)

tokyo_dt = utc_dt.astimezone(timezone(timedelta(hours=9)))
print(tokyo_dt)

tokyo_dt2 = bj_dt.astimezone(timezone(timedelta(hours=9)))
print(tokyo_dt2)


from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])
p = Point(1, 2)
print(p.x)
print(p.y)


from collections import OrderedDict

d = dict([["a", 1], ["b", 2], ["c", 3]])
print(d)
od = OrderedDict([("a", 1), ("b", 2), ("c", 3)])
print(od)

od2 = OrderedDict([["Bob", 90], ["Jim", 20], ["Seve", 22]])
print(od2)

from collections import Counter
c = Counter()

for ch in "programing":
    c[ch] = c.setdefault(ch,0) + 1

print(c)

import itertools
natuals = itertools.count(1)
# for n in natuals:
# print(n)
natuals = itertools.count(1)
ns = itertools.takewhile(lambda x: x <= 10, natuals)
print(ns)
print(list(ns))

for c in itertools.chain("ABC", "XYZ"):
    print(c)

print(list(itertools.chain("ABC", "XYZ")))

for key, group in itertools.groupby("AAABBBCCAAA"):
    print(key, list(group))
    print(key, group)

for key, group in itertools.groupby("AaaBBbcCAAa", lambda c: c.upper()):
    print(key, list(group))


class Query(object):
    def __init__(self,name):
        self.name = name

    def __enter__(self):
        print("enter")
        return self
    def __exit__(self,exc_type,exc_value,traceback):
        if exc_type:
            print("Error")
        else:
            print("end")
    def query(self):
        print("Query info about %s..." % self.name)


with Query("BBBB") as q:
    if q:
        q.query()

from contextlib import contextmanager

@contextmanager
def my_resource():
    print("enter")
    yield "资源"
    print("exit")
with my_resource() as r:
    print(r)

from contextlib import closing
# from urllib.request import urlopen

# with closing(urlopen("https://www.python.org")) as page:
#     for line in page:
#         print(line)


from urllib import request

# with request.urlopen("https://www.baidu.com") as f:
#     data = f.read()
#     print(data)
#     print(f.status,f.reason,f.url)


req = request.Request("https://www.baidu.com")
req.add_header("User-Agent","Mozilla/6.0")

with request.urlopen(req) as f:
    print(f.status,f.reason)
    for k,v in f.getheaders():
        print("%s: %s" % (k,v))