#!/usr/bin/env python
# coding: utf-8

# ## 动态属性

# <center>users.age</center>
# 查找过程按照如下顺序:<br>
# 如果user是类的实例化, 那么users.age或者等价的getattr(user, 'age'), 首先会调用__getattribute__函数. 如果类定义了 __getattr__则会在__getattribute__抛出 **AttributeError**的时候调用.<br>
# 对于描述符(__get__)的调用, 也是发生在 __getattribute__内部的.
# 
# 1. 如果 age 是出现在 User或其基类的__dict__中并且 age是数据描述符(这时候age是类属性), 那么会调用数据描述符中的 __get__
# 2. 如果 age 是出现在 user(也就是User的实例)的__dict__中, 那么直接返回object.__dict__['age'], 否则:
# 3. 如果 age 是出现在User或其基类的 __dict__中:<br>
# 3.1. 如果 age 是非数据描述符, 那么直接调用其__get__方法, 否则:<br>
# 3.2. 返回 __dict__['age']
# 4. 如果User定义了__getattr__方法, 调用__getattr__方法, 否则:
# 5. 抛出AttributeError.
# 
# 注意user.age 和user.__dict__['age']调用的逻辑不同

# ### 用 property实现动态属性

# In[1]:


# 在Python里 无需显式地调用setter和getter方法
# 在大多数情况下，你应该用简单公共属性。
# 公共属性 用 X.y的方式就可以访问。
class Resistor(object):
    def __init__(self, ohms):
        self.ohms = ohms
        self.voltage = 0
        self.current = 0

r1 = Resistor(500)
r1.ohms += 1000
r1.ohms


# In[5]:


# 如果你要实现自己的setter方法，你可以用@property装饰器
# 和setter方法
class VoltageResistance(Resistor):
    def __init__(self, ohms): super().__init__(ohms)
        #设置私有属性voltage
        self._voltage = 0
    #getter方法
    @property
    def voltage(self):
        return self._voltage
    #setter方法
    @voltage.setter
    def voltage(self, voltage):
        self._voltage = voltage
        self.current = self._voltage / self.ohms

r2 = VoltageResistance(1000)
r2.current

r2.voltage = 10
r2.current


# In[9]:


#你也可以在setter方法里面加入其他功能, 例如类型检查
class BoundResistance(Resistor):
    def __init__(self, ohms):
        super().__init__(ohms)
    @property
    def ohms(self):
        return self._ohms
    @ohms.setter
    def ohms(self, ohms):
        if ohms <= 0:
            raise ValueError('%f ohms must be > 0' % ohms)
        self._ohms = ohms  

r3 = BoundResistance(1000)
r3.ohms = 0

#初始化类的时候会调用__init__函数，而self.ohms = -5会调用 setter方法进行类型检查和值检查
r4 = BoundResistance(-5)


# In[12]:


#你甚至可以用setter方法保证属性的值不被重置
#注意这个用法
class FixedResistance(Resistor):
    @property
    def ohms(self):
        return self._ohms
    @ohms.setter
    def ohms(self, ohms):
        #如此一来，ohms属性只能在初始化时被赋值
        if hasattr(self, '_ohms'):
            raise AttributeError('Can not set attribute')
        self._ohms = ohms


# In[1]:


#我们的需求: 需要知道user的年龄
from datetime import date, datetime
class User(object):
    def __init__(self, name, birthday):
        self.name = name
        self.birthday = birthday
        self._age = 0
    
    #计算属性
    @property
    def age(self):
        return datetime.now().year - self.birthday.year
    @age.setter
    def age(self, value):
        self._age = value


# In[1]:


#@property的注意点
##1.@property指定的属性 只能在类和子类之间共享。
##2.@property指定的方法无法被其他属性复用
##3.不要在@property指定的属性的方法中修改其他属性的值
##4.确保你的@property的方法 simple and fast


# In[15]:


#一个 @property的高级用法
from datetime import datetime
class Bucket(object):
    def __init__(self, period):
        self.period_delta = timedelta(seconds = period)
        self.reset_time = datetime.now()
        self.max_quota = 0
        self.quota_consumed = 0
    def __repr__(self):
        return ('Bucket(max_quota = %d, quota_consumed = %d)' %                (self.max_quota, self.quota_consumed))
    # 用@property的方法 maintain那些经常改变(例如数值变化)的属性(例如上面的计算年龄)
    # 这样写的好处是，Bucket.quota 属性不需要知道class的变化，他只需要枚举
    #所有可能的状态在做相应的改变就可以了。
    @property
    def quota(self):
        return self.max_quota - self.quota_consumed
    @quota.setter
    def quota(self, amount):
        delta = self.max_quota - amount      
        if amount == 0:
            #Quota being reset for a new period
            self.quota_consumed = 0
            self.max_quota = 0
        elif delta < 0:
            #Quota being filled for the new period
            assert self.quota_consumed == 0
            self.max_quota = amnount
        else:
            #Quota being consumed during the period
            assert self.max_quota >= self.quota_consumed
            self.quota_consumed += delta

def fill(bucket, amount):
    now = datetime.now()
    if now - bucket.reset_time > bucket.period_delta:
        #此时bucket需要被重置
        bucket.quota = 0
        bucket.reset_time = now
    bucket.quota += amount
def deduct(bucket, amount):
    now = datetime.now()
    if now - bucket.reset_time > bucket.period_delta:
        return False
    if bucket.quota - amount < 0:
        return False
    bucket.quota - amount
    return True
        


# ### 用描述符实现getter和setter
# 1. 将类变成属性描述符, 需要实现\_\_get\_\_或者\_\_set\_\_或者\_\_delete\_\_
# 2. 实现了 \_\_get\_\_和\_\_set\_\_方法的叫数据描述符, 这里的\_\_set\_\_方法可以用来控制一类属性的赋值行为
# 3. 实现了\_\_get\_\_的叫非数据描述符

# In[6]:


import numbers
#IntField属性描述符
class IntField(object):
    def __get__(self, instance, owner):
        #Owner是类本身, 不是实例化
        print(instance, owner)
        return self.value
    def __set__(self, instance, value):
        #instance 是类的实例化
        if not isinstance(value, numbers.Integral):
            raise ValueError('Need int input!')
        else:
            self.value = value
        print(instance, value)
                 
    def __delete__(self, instance):
        pass
#NondataField非属性描述符
class NondataField(object):
    def __get__(self, instance, owner):
        pass


# In[23]:


#数据描述符
class Grade(object):
    def __init__(self):
        self._value = 0
    def __get__(self, instance, instance_type):
        return self._value
    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._value = value
class Exam(object):
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()


# In[28]:


#上面的Exam类是有bug的：
##因为三个Grade的实例是类属性, 只会在Exam类第一次实例化时初始化，此后不会在初始化！！！
first_exam = Exam() 
first_exam.writing_grade = 82 
first_exam.science_grade = 99 
print('Writing', first_exam.writing_grade) 
print('Science', first_exam.science_grade)
second_exam = Exam() 
second_exam.writing_grade = 75 
print('Second', second_exam.writing_grade, 'is right') 
print('First ', first_exam.writing_grade, 'is wrong')


# In[13]:


#解决方案：在基类中维护一个储存实例的字典
class Grade_v2(object):
    def __init__(self):
        #这一方法的缺点就是消耗内存
        self._values = {}
    def __get__(self, instance, instance_type):
        if instance is None: return self
        print(instance)
        return self._values.get(instance, 0) #第二个参数是没有找到instance时默认创建的
    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError('Grade must be between 0 and 100')
        self._values[instance] = value
class Exam_v2(object):
    math_grade = Grade_v2()
    writing_grade = Grade_v2()
    science_grade = Grade_v2()


# In[14]:


a = Exam_v2()
b = Exam_v2()
a.math_grade = 30
b.math_grade = 70


# In[1]:


#解决方安: 用weakref内置模块,这样会触发Python的自动垃圾回收机制
from weakref import WeakKeyDictionary


# In[2]:


class Grade_v3(object):
    def __init__(self):
        self.__values = WeakKeyDictionary()
    pass #下同Grade_v2


# ### 动态方法 __getattr__, __setattr__
# 1. \_\_getattr\_\_在查找不到属性的时候调用
# 2. 只要你定义了getattribute, 那么 cls.attr 就会调用getattribute

# In[2]:


from datetime import date, datetime
class User(object):
    def __init__(self, name, birthday):
        self.name = name
        self.birthday = birthday
    def __getattr__(self, item):
        if item == 'Name':
            return self.name
        else:
            return ('%s not found' % item)


# In[3]:


#在cls.__dict__中查找不到age的时候, 就会调用 __get_attr__
user = User('bobby', date(year=1991, month=7, day=19))
print(user.age)
print(user.Name)


# In[10]:


#设想你需要设计一个数据库的class
#这个class的每个属性属性代表了数据库的 一个row
#但你的数据库的row是不确定的, 这时候可以考虑动态方法
class LazyDB(object):
    #LayDB的属性是你数据库的row
    #但是你数据库的row是未确定的
    #这时候可以用__getattr__和__setattr__，
    #当你访问的attribute不存在时， python会调用这俩方法
    def __init__(self):
        self.exists = 5
    def __getattr__(self, name):
        value = 'value for %s' % name
        #setattr方法将属性放入实例的字典
        setattr(self, name, value)
        return value


# In[11]:


data = LazyDB()
print('Before:', data.__dict__)
print('foo:', data.foo)
print('After:', data.__dict__)


# In[12]:


hasattr(data, 'foo')


# In[13]:


#在子类中使用 getattr 需要注意:
class LoggingLayDB(LazyDB):
    def __getattr__(self, name):
        print('called __getattr__(%s)' % name)
        #在子类中，用super().__getattr__()方法来避免死循环
        return super().__getattr__(name)


# In[14]:


data = LoggingLayDB()
#exists 是父类的属性因而不会调用__getattr__
print('exists:', data.exists)
print('foo:', data.foo)
print('foo:', data.foo)


# ### \_\_getattribute\_\_, \_\_setattribute\_\_, \_\_setattr\_\_

# In[4]:


from datetime import date, datetime
class User(object):
    def __init__(self, name, birthday):
        self.name = name
        self.birthday = birthday
    def __getattr__(self, item):
        if item == 'Name':
            return self.name
        else:
            return ('%s not found' % item)
    def __getattribute__(self, item):
        return "这是所有属性访问的入口"


# In[5]:


#在__getattribute__时所有属性访问的入口
#尽量不要重写这个函数
user = User('bobby', date(year=1991, month=7, day=19))
print(user.age)
print(user.Name)


# In[16]:


#假设用户访问一个属性时，他想知道该属性在数据库中的row是否还存在。
#用__getattr__无法满足上述需求，？？？？？？
#此时可以用__getattribute__方法， 
class ValidatingDB(object):
    def __init__(self):
        self.exists = 5
    def __getattribute__(self, name):
        print('called __getattribute__(%s)' % name)
        try:
            return super().__getattribute__(name)
        except AttributeError:
            value = 'Value for %s' % name
            setattr(self, name, value)
            return value


# In[17]:


data = ValidatingDB()
print('exists:', data.exists)
print('foo:', data.foo)
print('foo:', data.foo)


# In[4]:


#__setattr__每次在对象设置属性的时候都会调用
#setattr也要会调用__setattr__
class SavingDB(object):
    def __setattr__(self, name, value):
        super().__setattr__(name, value)
class LoggingSavingDB(SavingDB):
    def __setattr__(self, name, value):
        print('Called __setattr__(%s, %r)' % (name, value))
        super().__setattr__(name, value)


# In[5]:


data = LoggingSavingDB()
print('Before:', data.__dict__)
#注意这个之前的访问不同，这里是对未必存在的属性赋值!!!!!
data.foo = 5
print('After:', data.__dict__)
data.foo = 7
print('Finally', data.__dict__)


# In[6]:


#__getattribute__和__setarrt__在每次访问以及赋值的时候都会被调用,无论属性是否存在，这其实也是他们的缺点!!!
class BrokenDictionaryDB(object):
    def __init__(self,data):
        self._data = data
    def __getattribute__(self, name):
        print('Called __getattribute__()%s' % name)
        #你在__getattrbute__里访问slef._data这也会导致
        #__getattribute__被调用，最终导致死循环
        return self._data[name]
#解决方案，在__getattribute__里调用父类的__getattribute__
class DictionaryDB(object):
    def __init__(self, data):
        self._data = data
    def __getattribute__(self, name):
        data_dict = super().__getattribute__('data')
        return data_dict[name]


# ## Meta Class

# <center>Python 中实例化的过程</center>
# 
# 1. 如果子类和基类都没有metaclass, type去创建唯一的class object, 注意不是实例.
# 2. 如果指定了metaclass, 那么在实例化 类对象之前会调用metaclass, 通过metaclass去创建类对象.
# 3. 如果没有指定metaclass但是基类指定了metaclass, 那么会调用基类的metaclass
# **因此, 创建类对象的过程可以委托给元类, 而无需再类里面定义new方法**

# ###### \_\_new\_\_ 和 \_\_init\_\_ 的区别
# 1. 如果new方法不反回对象就不会调用init函数， new方法返回类的实例
# 2. init是类实例化之后调用

# In[7]:


class User(object):
    #new魔法函数, 在类的实例化之前调用
    def __new__(cls, *args, **kwargs):
        print('In new.')
    #init是类实例化之后调用
    def __init__(self):
        print('In init.')


# In[8]:


user = User()


# In[11]:


class User_(object):
    #new魔法函数, 在类的实例化之前调用
    def __new__(cls, *args, **kwargs):
        print('In new.')
        #必须有这句话否则不会调用初始化函数
        return super().__new__(cls)
    #init是类实例化之后调用
    def __init__(self):
        print('In init.')


# In[12]:


user = User_()


# ###### 自定义元类
# 类也是对象, type是用来创建类的类

# In[13]:


#根据名字动态创建类
def create_class(name):
    if name == 'user':
        class User(object):
            pass
        return User
    elif name == 'company':
        class Company(object):
            pass
        return Company
    else:
        return None


# ###### 自定义元类 用type
# 1. 第一个参数是一个字符串, 代表类的名字
# 2. 第一个参数是tuple, 是你的元类的基类: (base1, bas2, ..., object,)
# 3. 第三个参数是字典, 里面储存了类属性和类方法

# In[14]:


#用更灵活的方法, 用type
#注意！name是类属性
class BaseClass(object):
    def ans(self):
        return 'I am base class.'
def say(self):
    return self.name
#User是type生成的元类
User = type('User', (BaseClass,object,), {'name':'user', 'say':say})
user = User()
print(user.name)
print(User.__dict__)
print(user.__dict__)
print(user.ans())


# ##### 元类是创建类的类
# type->class(cls在python中也是对象)->对象

# In[ ]:


#一般的元类需要继承type,
#MetaClass控制类实例化的过程
class MetaClass(type):
    def __new__(cls, name, bases, class_dict):
        print('In meta class.')
        #用父类, 也就是type来生成cls
        #等价于 super().__new__(cls, name, bases, class_dict)
        return type.__new__(cls, name, bases, class_dict)
class User(metaclass=MetaClass):
    def __init__(self):
        pass


# ##### 元类的若干用途

# In[16]:


#1. 用metaclass确认一个class是否正确定义, 尤其当你的class层次复杂时
#metaclass的定义方式
class Meta(type):
    #我们可以在__new__方法里增加验证参数的代码
    def __new__(meta, name, bases, class_dict):
        print(meta, name, bases, class_dict)
        return type.__new__(meta, name, bases, class_dict)


#The __new__ method of metaclasses is run 
#after the class statement’s entire body has been processed.
class MyClass(object, metaclass = Meta):
    stuff = 123
    def foo(self):
        pass


# In[4]:


#演示一下 复杂继承的情况。
#meta class
class ValidatePolygon(type):
    def __new__(meta, name, bases, class_dict):
        if bases != (object, ): #如果不是基类
            #特别注意，不要在基类重新验证了
            if class_dict['sides'] < 3:
                raise ValueError('Polygons need 3+ sides')
        return type.__new__(meta, name, bases, class_dict)
#基类, base = object
class Polygon(object, metaclass = ValidatePolygon):
    sides = None 
    @classmethod
    def interior_angles(cls):
        return (cls.sides - 2) * 180
class Triangle(Polygon):
    sides = 3


# In[7]:


print('Before class') 

class Line(Polygon):
    print('Before sides')
    sides = 1
    print('After sides') 
    
print('After class')


# In[12]:


#2. meta class的另一个作用是， 自动类型注册

#基类:把参数序列化
import json
class Serializable(object):
    def __init__(self, *args):
        self.args = args
    def serialize(self):
        return json.dumps({'args': self.args})


# In[13]:


class Point2D(Serializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self. y = y
    def __repr__(self):
        return 'Point2D(%d, %d)' % (self.x, self.y)


# In[14]:


point = Point2D(5, 3)
print('Object:', point) 
print('Serialized:', point.serialize())


# In[15]:


#下面我们要对参数解序列化， 来获得类的实例
class Deserializeable(Serializable):
    @classmethod
    def deserialize(cls, json_data):
        params = json.loads(json_data)
        return cls(*params['args'])

class BetterPoint2D(Deserializeable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self. y = y
    def __repr__(self):
        return 'BetterPoint2D(%d, %d)' % (self.x, self.y)


# In[17]:


point = BetterPoint2D(5, 3) 
print('Before:', point) 
data = point.serialize() 
print('Serialized:', data) 
after = BetterPoint2D.deserialize(data) 
print('After:', after)


# In[24]:


#上面一套持久化的办法的一个问题是， 你需要提前决定Point2D和BetterPoint2D的结构
#解决方案, 将类名一并序列化,并且维护一个类的字典
class BetterSerializable(object):
    def __init__(self, *args):
        self.args = args
    def serialize(self):
        return json.dumps(
            {
                'class' : self.__class__.__name__, 
                'args' : self.args
            }
        )

#registry字典: 类名字 : 类
registry = {}
def register_class(target_class):
    """
    Parameters
    ----------
    target_class : class, not a instance of class!
    """
    registry[target_class.__name__] = target_class

def deserialize(data):
    params = json.loads(data)
    name = params['class']
    #从字典中取得需要解序列化的class
    target_class = registry[name]
    #返回一个实例
    return target_class(*params['args'])


# In[25]:


class EvenBetterPoint2D(BetterSerializable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self. y = y
register_class(EvenBetterPoint2D)


# In[26]:


point = EvenBetterPoint2D(5, 3)
print('Before: ', point)
data = point.serialize()
print('Serialized: ', data)
after = deserialize(data)
print('After: ', after)


# In[ ]:


#上面的方法的问题是， 你可能忘记register_class！！
class Point3D(BetterSerializable):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.x = x
        self.y = y
        self.z = z


# In[27]:


#解决方案,用meta class完成类的注册操作
class Meta(type):
    def __new__(meta, name, bases, class_dict):
        #首先生成class
        cls = type.__new__(meta, name, bases, class_dict)
        #通过调用父类的__new__方法，来完成 class的注册
        register_class(cls)
        return cls
class RegisterSerializable(BetterSerializable, metaclass = Meta):
    pass
class Vector3D(RegisterSerializable):
    def __init__(self, x, y, z):
        super().__init__(x, y, z)
        self.x, self.y, self.z = x, y, z


# In[32]:


v3 = Vector3D(10, -7, 3)
print('Before: ', v3)
data = v3.serialize()
print('Serialized: ', data)
print('After: ', deserialize(data))


# In[2]:


#3. 用meta class为类增加属性和方法


# In[1]:


#下面的customer class的每一个属性代表了数据库的一列
#通过下面的 数据描述符, 可以为Customer class 增加一个受保护的属性
#这一受保护的属性的名字为 _interval_name, 由用户定义！！！
class Field(object):
    def __init__(self, name):
        self.name = name
        self.internal_name = '_' + self.name
    
    #get方法调用实例的`internel_name`属性
    def __get__(self, instance, isntance_type):
        if instance is None:
            return self
        print(instance.__class__.__name__, self.internal_name)
        return getattr(instance, self.internal_name, '')
    
    #set方法设置internal_name属性的值
    def __set__(self, instance, value):
        setattr(instance, self.internal_name, value)

class Customer(object):
    #属性描述符
    first_name = Field('first_name')
    last_name = Field('last_name')
    prefix = Field('prefix')
    suffix = Field('suffix')


# In[2]:


#注意 调用 __get__和__set__的实例是 foo， 因此instance 是 foo
foo = Customer()
print('Before:', repr(foo.first_name), foo.__dict__)
foo.first_name = 'zzj'
print('After:', repr(foo.first_name), foo.__dict__)


# In[3]:


#上面的方法是冗余的，因为在Customer声明中我已经set了属性的名字 first_name
#那么接着把 字符串 'first_name'传递到Field的构造函数里显得多余了:
"""
    first_name = Field('first_name')
"""
#解决方案, 用meta class + descriptors


# In[82]:


class Meta(type):
    def __new__(meta, name, bases, class_dict):
       #class_dict : 类属性的名字为键, 类属性为值
        for key, value in class_dict.items():
            #如果属性是Field类型,为其属性赋值
            if isinstance(value, Field):
                value.name = key
                value.internal_name = '_' + key
        cls = type.__new__(meta, name, bases, class_dict)
        return cls
class DatabaseRow(object, metaclass = Meta):
    pass
#注意Field不用metaclass
class Field(object):
    def __init__(self):
        #这属性在 meta class 中初始化
        self.name = None
        self.internal_name = None


# In[84]:


class BetterCustomer(DatabaseRow):
    first_name = Field()
    last_name = Field()
    prefix = Field()
    suffix = Field()


# In[85]:


foo = BetterCustomer()
print('Before: ', repr(foo.first_name), foo.__dict__)
foo.first_name = 'Euler'
print('After: ', repr(foo.first_name), foo.__dict__)


# ## 通过元类实现ORM

# In[3]:


#orm 将我们的类映射到数据库中的一张表.


# In[6]:


class Field(object):
    pass


# In[7]:


class IntField(Field):
    def __init__(self, db_column, min_value=None, max_value=None):
        self.db_column = db_column
        self._value = None
        #我们略去类型和值检查
        self.min_value = min_value
        self.max_value = max_value
    def __get__(self, instance, instance_type):
        return self._value
    def __set__(self, instance, value):
        #我们略去类型和值检查
        self._value = value


# In[8]:


class CharField(Field):
    def __init__(self, db_column, max_length=None):
        self.db_column = db_column
        self.max_length = max_length
        self._value = None
    def __get__(self, instance, instance_type):
        return self._value
    def __set__(self, instance, value):
        self._value = value


# In[17]:


class Meta(type):
    def __new__(meta, name, bases, class_dict):
        if name == 'Base':
            return super().__new__(meta, name, bases, class_dict)
        
        #下面的逻辑是对User子类的
        #new方法整理cls的类属性并且为它加入新的类属性
        
        #从 cls的类属性字典中, 取出类型为Field的属性
        fields = {}
        for key, value in class_dict.items():
            if isinstance(value, Field):
                fields[key] = value
        #将 fields字典加入cls的属性字典中
        class_dict['fields'] = fields
        # 从cls中取出它内部定义的 Meta class
        # 从Meta class 中取出 它的 db_table属性
        attrs_meta = class_dict.get('Meta', None)
        db_table = name.lower()
        if attrs_meta is not None:
            table = getattr(attrs_meta, 'db_table', None)
            if table is not None:
                db_table = table   
        #将_meta加入到属性字典中
        _meta = {}
        _meta['tb_table'] = db_table
        class_dict['_meta'] = _meta
        del class_dict['Meta']
        return super().__new__(meta, name, bases, class_dict)


# In[35]:


class Base(object, metaclass=Meta):
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return
    def save(self):
        pass
        
class User(Base):
    name = CharField(db_column='a', max_length=10)
    age = IntField(db_column='b', min_value=1, max_value=100)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta(object):
        db_table = 'user'


# In[21]:


for key, value in User.__dict__.items():
    print('{0} : {1}'.format(key, value))


# ###### 注意 魔法方法访问顺序

# In[71]:


class Int(object):
    def __init__(self, i):
        self.i = i
    def __get__(self, instance, instance_type):
        return self.i
    def __set__(self, instance, value):
        print('Calling __set__.')
        self.i = value


# In[72]:


class A(object):
    a = 1
    b = Int(1)
    def __init__(self, c):
        self.c = c


# In[73]:


instance = A(1)
print(getattr(instance, 'a'))
#给instance增加同名的实例属性
instance.a = 3
#此时调用 getattr会去取实例属性
print(getattr(instance, 'a'))


# In[74]:


instance = A(1)
print(getattr(instance, 'b'))
#!!!!注意此时会调用数据描述符的set方法而不是产生新的属性！！！
instance.b = 3
#此时调用 getattr不会新加实例属性
print(getattr(instance, 'b'))
print(instance.__dict__)
#如果非要新加一个同名的实例属性b, 可以直接调用实例的__dict__方法


# In[ ]:




