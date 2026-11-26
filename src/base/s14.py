f = open(r"E:\Code\python\base\src\base\s10.py", "rb")
print(f.read())
f.close()


from io import StringIO

f = StringIO()
f.write("hello")
f.write(" ")
f.write("world !")
print(f.getvalue())


from io import StringIO

f = StringIO("Hello\nWorld\nGoodBye!!")
while True:
    s = f.readline()
    if s == "":
        break
    print(s.strip())


from io import BytesIO

f = BytesIO()
f.write("中文".encode("utf-8"))
print(f.getvalue())

from io import BytesIO

f = BytesIO(b"\xe4\xb8\xad\xe6\x96\x87")
c = str(f.read(),encoding="utf-8")
print(c)


import pickle

d = dict(name="Bob", age=20, score=88)
print(pickle.dumps(d))

d = pickle.loads(pickle.dumps(d))
print(d)


import json


class Student(object):
    """asdasd"""
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score


def convertFunc(std):
    return {"name": std.name, "age": std.age, "score": std.score}


s = Student("Bob", 20, 88)
print(json.dumps(s, default=convertFunc))
print(json.dumps(s, default=lambda obj: obj.__dict__))
print(Student("asd",23,23).__dict__)

print(Student.__bases__)


def revert(std):
    return Student(std["name"], std["age"], std["score"])


json_str = '{"age": 20, "score": 88, "name": "Bob"}'
print(json.loads(json_str, object_hook=revert))
