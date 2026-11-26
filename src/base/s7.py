class Student(object):
    def __init__(self, name):
        self.name = name

    def __str__(self) -> str:
        return "Student"


class Iter(object):
    def __init__(self):
        self.a = 0
        self.b = 1

    def __iter__(self):
        return self

    def __next__(self):
        self.a, self.b = self.b, self.a + self.b
        if self.a > 30:
            raise StopIteration()
        return self.a


for i in Iter():
    print(i)


class OddNum(object):
    def __init__(self):
        self.num = 1

    def __iter__(self):
        return self

    def __next__(self):
        self.num = self.num + 2
        if self.num > 10:
            raise StopIteration()
        return self.num

    def __getitem__(self, n):
        if isinstance(n, int):
            temp = 1
            for i in range(n):
                temp += 2
            return temp

        if isinstance(n, slice):
            start = n.start
            end = n.stop
            if start is None:
                start = 0
            tempList = []
            temp = 1
            for i in range(end):
                if i >= start:
                    temp += 2
                    tempList.append(temp)

            return tempList


    def __getattr__(self,attr):
        if attr == 'name':
            return 'OddNum'
        if attr == 'data':
            return lambda:self.num
        raise AttributeError('\'OddNum\' object has no attribute \'%s\'' %attr)
    def __call__(self):
        return "My name is OddNum!!"
    
    def __repr__(self):
        return "ODDNUM"
for i in OddNum():
    print(i)
print(OddNum()())
print(OddNum()[:5])
print(OddNum())


from enum import Enum, unique

Month = Enum(
    "Month",
    (
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ),
)

for name,member in Month.__members__.items():
    print(name,"=>",member,",",member.value)

@unique
class WeekDay(Enum):
    Sun = 0
    Mon = 1
    Tue = 2
    Wed = 3
    Thu = 4
    Fri = 5
    Sat = 6

for name,member in WeekDay.__members__.items():
    print(name,"=>",member,",",member.value)