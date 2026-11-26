class TypeClass(object):
    def typeprint(self, name="typeclass"):
        print("class name is %s" % (name))


typeclasses = TypeClass()
print(type(TypeClass))
print(type(typeclasses))


def printHW(self):
    print("Hello world!!!")


TypeClass2 = type("TypeClass2", (object,), dict(typeprinthw=printHW))


typeclass2 = TypeClass2()
typeclass2.typeprinthw()


cls = globals()["TypeClass"]
cls().typeprint()


class Field:
    def __init__(self, name, column_type):
        self.name = name
        self.column_type = column_type

    def __str__(self):
        return "<%s%s>" % (self.__class__.__name__, self.name)


class IntegerField(Field):
    def __init__(self, name):
        super().__init__(name, "bigint")


class StringField(Field):
    def __init__(self, name):
        super().__init__(name, "vector(100)")


print(StringField("1234"))


"""
    class User(Model):
    id = IntegerField('id')
    name = StringField('username')
    email = StringField("email")
    password = StringField("password")
    u = User(id=12345, name="Michael", email="test@orm.org", password="my-pwd")
    
    这时候u.id 走的是实例化的数据 12345
    如果创建User的时候没有指定id,此时u.id 实际上是类的属性id # <IntegerField: id>   ← 返回字段对象，不是报错
    
    显然这样是不对的，实例化后的属性和类属性应该分开，类属性只作为结构描述。
    
    所以引入metaclass元类
    元类用来造类
    class User(Model, metaclass=ModelMetaclass)，意思是：“造 User 这个类的时候，别用默认的 type，用 ModelMetaclass 来造。”
    一个类创造的时候先走的__new__，
    
    class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == "Model":                 # Model 本身不处理
            return type.__new__(cls, name, bases, attrs)

        fields = {}
        for k, v in list(attrs.items()):
            if isinstance(v, Field):        # 发现字段声明
                fields[k] = v
                attrs.pop(k)                # 从类属性里删掉
        attrs['__fields__'] = fields        # 收进一个专门的属性
        return type.__new__(cls, name, bases, attrs)
        
    这样造 User 时：

    attrs 里的 id、name 被识别为 Field；

    从 attrs 里删掉，所以 User.id 不再是 IntegerField 对象；

    收进 User.__fields__ = {"id": IntegerField('id'), ...}。

    这就是元类在这个 ORM 里唯一不可替代的作用：在类创建时，把“字段声明”从类属性里挑出来、整理好。手写类做不到这一点，因为类体写完后 Python 就直接造类了，你没有插手的机会。
    
    如此一来：
    
    因为示例化的数据存入了字典，但是对应的类属性却被我们摘出去了，这样数据不存在时报错。
    u = User()
    print(u.id)         # AttributeError: 'Model' object has no attribute 'id'
"""
class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)
        fields = {}
        for k, v in list(attrs.items()):
            if isinstance(v, Field):  # 发现字段声明
                fields[k] = v
                attrs.pop(k)  # 从类属性里删掉
        attrs["__fields__"] = fields  # 收进一个专门的属性
        return type.__new__(cls, name, bases, attrs)

class Model(dict, metaclass=ModelMetaclass):
    def __init__(self,**kw):
        super().__init__(**kw)

    def __getattr__(self,key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


class User(Model):
    id = IntegerField('id')
    name = StringField('username')
    email = StringField("email")
    password = StringField("password")

u = User(id=12345, name="Michael", email="test@orm.org", password="my-pwd")

print(dir(User))
