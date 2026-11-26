import re

m = re.match(r"^(\d{3})-(\d{3,8})", "010-12345dfgdfg")
print(m)
print(m.group(0))
print(m.group(1))
print(m.group(2))
print(m.groups())


pattern = re.compile(r"hello")
result1 = re.match(pattern, "hello")
result2 = re.match(pattern, "helloo, aaa")
result3 = re.match(pattern, "helo AAB")
result4 = re.match(pattern, "helloww")

if result1:
    print(result1)
else:
    print("failed!!!")

if result2:
    print(result2.group())
else:
    print("failed!!!")

if result3:
    print(result3.group())
else:
    print("failed!!!")

if result4:
    print(result4.group())
else:
    print("failed!!!")


m = re.match(r"(\w+) (\w+)(?P<sign>.*)", "hello world!34534534543")
print("m.string is %s" % (m.string))
print("m.re: %s" % (m.re))
print("m.pos: %d" % (m.pos))
print("m.endpos: %d" % (m.endpos))
print("m.lastindex: %d" % (m.lastindex))
print("m.lastgroup: %s" % (m.lastgroup))
print("m.groups: ", m.groups())
print("m.group: ", m.group())
print("m.group(1,2): ", m.group(1, 2))
print("m.groupdict():", m.groupdict())
print("m.start(2):", m.start(2))
print("m.end(2):", m.end(2))
print("m.span(2):", m.span(2))
print("m.expand(r'\g \g\g'):", m.expand(r"\2 \1\3"))
