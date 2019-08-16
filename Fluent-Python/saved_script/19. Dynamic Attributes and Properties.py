#!/usr/bin/env python
# coding: utf-8

# ##### Data Wrangling with Dynamic Attributes

# 我们的示例数据集如下图所示:
# 
# ![img/19_1.png](img/19_1.png)
# 
# 这是一个 Json 文件. 注意 conference, events, speakers 和 venues 的 值是列表, 列表的每一个元素是字典

# In[5]:


# 下载示例数据集

from urllib.request import urlopen
import warnings
import os
import json

URL = 'http://www.oreilly.com/pub/sc/osconfeed' 
JSON = 'data/osconfeed.json'

def load():
    if not os.path.exists(JSON):
        msg = 'downloading {} to {}'.format(URL, JSON)
        warnings.warn(msg)
        with urlopen(URL) as remote,             open(JSON, 'wb') as local:
            local.write(remote.read())
    with open(JSON) as fp:
        return json.load(fp)


# In[6]:


# 检查下载的Json文件
raw_feed = load()
print(sorted(raw_feed['Schedule'].keys()))

for key, value in sorted(raw_feed['Schedule'].items()):
    print('{:3} {}'.format(len(value), key))


# ###### Exploring JSON-Like Data with Dynamic Attributes

# In[7]:


from collections import abc


class FrozenJSON(object):
    """用于读取 Json 格式的类,
    只提供读取方法.
    """

    def __init__(self, mapping):
        self.__data = dict(mapping) #1

    def __getattr__(self, name): #2
        if hasattr(self.__data, name):
            return getattr(self.__data, name) #3
        else:
            return FrozenJSON.build(self.__data[name]) #4

    @classmethod
    def build(cls, obj): #5
        if isinstance(obj, abc.Mapping): #6
            return cls(obj)
        elif isinstance(obj, abc.MutableSequence): #7
            return [cls.build(item) for item in obj]
        else: #8
            return obj


# <center>总结</center>
# 
# 1. 获得 mapping 的 copy 并且获得一个 dict 对象.
# 2. **只有实例而找不到 `name` 属性, 并且实例的类及其父类中也找不到时, 才会调用 \_\_getattr\_\_ 方法.**
# 3. 如果 \_\_data 有名为 `name` 的属性, 就直接返回.
# 4. 否则, 首先获取 \_\_data 中的名为 `name` 的 key, 然后调用 FrozenJSON.build() 函数.
# 5. 用 classmethod 实现的工厂函数
# 6. 如果 obj 是一个 mapping 对象, 用它构造一个 FrozenJSON 对象.
# 7. 如果 obj 是一个 MutableSequence 对象, 他一定是一个 list. **这是因为 Json 格式中只能有 list 和 dict.** 那么返回一个列表生成式.
# 8. 如果既不是 list 也不是 dict, 就返回他自身.

# In[8]:


feed = FrozenJSON(raw_feed)
len(feed.Schedule.speakers)


# In[9]:


# 当原始数据中的 key 不是合法的属性名时, 比如 key 是 Python中的关键字
# 需要在初始化时改变一下名字: 用 keyword 模块中的 iskeyWord 检测是否为关键字

from keyword import iskeyword


def __init__(self, mapping):
    self.__data = {}
    for key, value in mapping.items():
        if iskeyword(key):
            key += '_'
        self.__data[key] = value


# ###### 用 \_\_new\_\_ 方法完成实例化
# 
# \_\_new\_\_ 创建了实例, 并且调用 \_\_init\_\_ 函数, 将实例作为第一个参数传递给 \_\_init\_\_ 函数.

# In[10]:


from keyword import iskeyword


class FrozenJSON(object):
    def __new__(cls, args):
        print('Calling new.')
        if isinstance(args, abc.Mapping):
            return super().__new__(cls)
        elif isinstance(args, abc.MutableSequence):
            return [cls(item) for item in args]
        else:
            return args

    def __init__(self, mapping):
        print('Calling init.')
        self.__data = {}
        for key, value in mapping.items():
            if iskeyword(key):
                key += '_'
            self.__data[key] = value

    def __getattr__(self, name):
        if hasattr(self.__data, name):
            return getattr(self.__data, name)
        else:
            return FrozenJSON(self.__data[name])


# In[11]:


feed = FrozenJSON(raw_feed)

# feed.Schedule.speakers


# ###### 用 shelve 模块来重新构建数据

# In[21]:


import warnings

DB_NAME = 'data/schedule1_db'
CONFERENCE = 'conference.115'

class Record(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs) #1
    
    def __eq__(self, other):
        if isinstance(other, Record):
            return self.__dict__ == other.__dict__
        else:
            return NotImplemented

def load_db(db):
    raw_data = load()
    warnings.warn('loading ' + DB_NAME)
    for collection, rec_list in raw_data['Schedule'].items(): #2
        record_type = collection[:-1] #3
        for record in rec_list:
            key = '{}.{}'.format(record_type, record['serial']) #4
#             print(key)
            record['serial'] = key #5
            db[key] = Record(**record) #6


# <center>总结</center>
# 
# 1. 通过更新 \_\_dict\_\_ 来批量初始化实例变量 (Note: depending on the application context, the Record class may need to deal with keys that are not valid attribute names.)
# 2. Iterate over collections under 'Schedule'(Schedule 是最上层的键)
# 3. record_type is set to the collection name without the trailing 's' (i.e., 'events' becomes 'event')
# 4. build key and 'serial' field
# 5. Update the 'serial' field with the full key
# 6. Build Record instance and save it to the database under the key.
# json 文件里面的一个字典就是 load_db 里面的一个 Record 对象.

# In[22]:


# Let's test the aboveing code
# Fisrt open `DB_NAME` and save json data in it.
import shelve

db = shelve.open(DB_NAME)
if CONFERENCE not in db:
    load_db(db)


# In[37]:


# Test db
def test_record_class():
    rec = Record(spam=99, eggs=12)
    assert rec.spam == 99
    assert rec.eggs == 12


def test_conference_record(db):
    assert CONFERENCE in db


def test_speaker_record(db):
    speaker = db['speaker.3471']
    assert speaker.name == 'Anna Ravenscroft'


def test_event_record(db):
    event = db['event.33950']
    assert event.name == 'There *Will* Be Bugs'


def test_event_venue(db):
    event = db['event.33950']
    assert event.venue_serial == 1449

test_record_class()
test_conference_record(db)
test_speaker_record(db)
test_event_record(db)
test_event_venue(db)
db.close()


# 下面扩展 Record class
# 
# New service: Automatically retrieving venue and speaker records referenced in an event record.
# 
# ![img/19_2.png](img/19_2.png)

# In[53]:


class MissingDatabaseError(RuntimeError):
    """Raised when a database is required but was not set.
    """


class DbRecord(Record):

    __db = None

    @staticmethod
    def set_db(db):
        DbRecord.__db = db

    @staticmethod
    def get_db():
        return DbRecord.__db

    @classmethod
    def fetch(cls, ident):
        """Retrive records from the database
        """
        db = cls.get_db()
        try:
            return db[ident]
        except TypeError:
            if db is None:
                msg = "database not set; call '{}.set_db(my_db)'"
                raise MissingDatabaseError(msg.format(cls.__name__))
            else:
                raise

    def __repr__(self):
        if hasattr(self, 'serial'):
            cls_name = self.__class__.__name__
            return '<{} serial={!r}>'.format(cls_name, self.serial)
        else:
            return super().__repr__()


class Event(DbRecord):
    """Subclass of DbRecord adding `venue` and `speakers` prperties
    to retrive linked records, and a specialized __repr__ method.
    """

    @property
    def venue(self):
        key = 'venue.{}'.format(self.venue_serial)
        return self.__class__.fetch(key)

    @property
    def speakers(self):
        if not hasattr(self, '_speaker_objs'):
            spkr_serials = self.__dict__['speakers']
            # 用 self.__class__来获取 classmethod
            fetch = self.__class__.fetch
            self._speaker_objs = [fetch('speaker.{}'.format(key))
                                  for key in spkr_serials]
        return self._speaker_objs

    def __repr__(self):
        if hasattr(self, 'name'):
            cls_name = self.__class__.__name__
            return '<{} {!r}>'.format(cls_name, self.name)
        else:
            return super().__repr__()


# In[54]:


import inspect
def load_db_v2(db):
    raw_data = load()
    warnings.warn('loading ' + DB_NAME)
    for collections, rec_list in raw_data['Schedule'].items():
        record_type = collections[:-1] #1
        cls_name = record_type.capitalize() #2
        cls = globals().get(cls_name, DbRecord) #3
        if inspect.isclass(cls) and issubclass(cls, DbRecord): #4
            factory = cls #5
        else:
            factory = DbRecord #6
        for record in rec_list: #7
            key = '{}.{}'.format(record_type, record['serial'])
            record['serial'] = key
            db[key] = factory(**record)  # 8
        


# <center>总结</center>
# 
# 1. 去掉 `s`, 没错就是这么完美~~
# 2. 把原始的 key 搞成大写
# 3. **Get an object by that name from the module global scope; get DbRecord if there’s no such object.**
# 4. 如果3中 get 到的是 一个 class 并且是 DbRecord 的子类
# 5. 那么工厂方法就是它
# 6. 否则工厂方法就是基类 
# 7. for 循环遍历 每一个字典
# 8. 用先前得到的工厂函数构造实例, 并且写入 db 中.

# In[55]:


# Let's test the aboveing code
# Fisrt open `DB_NAME` and save json data in it.
import shelve

db = shelve.open(DB_NAME)
if CONFERENCE not in db:
    load_db_v2(db)


# In[56]:


import pytest
def test_record_attr_access():
    rec = Record(spam=99, eggs=12)
    assert rec.spam == 99
    assert rec.eggs == 12


def test_record_repr():
    rec = DbRecord(spam=99, eggs=12)
    assert 'DbRecord object at 0x' in repr(rec)
    rec2 = DbRecord(serial=13)
    assert repr(rec2) == "<DbRecord serial=13>"


def test_conference_record(db):
    assert CONFERENCE in db


def test_speaker_record(db):
    speaker = db['speaker.3471']
    assert speaker.name == 'Anna Ravenscroft'


def test_missing_db_exception():
    with pytest.raises(MissingDatabaseError):
        DbRecord.fetch('venue.1585')


def test_dbrecord(db):
    # db 储存了 DbRecord 的实例,
    # 通过 set_db 方法设置了 DbRecord 的类属性
    # 然后就可以 fetch了~~
    DbRecord.set_db(db)
    venue = DbRecord.fetch('venue.1585')
    assert venue.name == 'Exhibit Hall B'


def test_event_record(db):
    event = db['event.33950']
    assert repr(event) == "<Event 'There *Will* Be Bugs'>"


def test_event_venue(db):
    Event.set_db(db)
    event = db['event.33950']
    assert event.venue_serial == 1449
    assert event.venue == db['venue.1449']
    assert event.venue.name == 'Portland 251'


def test_event_speakers(db):
    Event.set_db(db)
    event = db['event.33950']
    assert len(event.speakers) == 2
    anna_and_alex = [db['speaker.3471'], db['speaker.5199']]
    assert event.speakers == anna_and_alex


def test_event_no_speakers(db):
    Event.set_db(db)
    event = db['event.36848']
    assert len(event.speakers) == 0


# In[62]:


test_record_attr_access()
test_record_repr()
test_conference_record(db)
test_speaker_record(db)
# test_missing_db_exception()
test_dbrecord(db)
test_event_venue(db)
test_event_speakers(db)
test_event_no_speakers(db)


# ##### Using a Property for Attribute Validation

# In[66]:


class LineItem(object):
    """订单类, 实例属性包含: 
    商品的描述
    商品的数目/重量
    商品的单价
    """
    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price
    
    def subtotal(self):
        return self.weight * self.price


# In[69]:


class LineItem(object):
    """改进的订单类
    """
    def __init__(self, description, weight, price):
        self.description = description
        # 在初始化的时候会调用 weight.setter
        self.weight = weight
        self.price = price
    
    def subtotal(self):
        return self.weight * self.price
    
    @property
    def weight(self):
        return self.__weight
    
    @weight.setter
    def weight(self, value):
        if value > 0:
            self.__weight = value
        else:
            raise ValueError('value must be > 0')


# <center>总结</center>
# 
# property 的完整签名:
# 
# ```python
# property(fget=None, fset=None, fdel=None, doc=None)
# ```
# 
# 1. 由此看见, property 是**类属性**. 但是, 它控制了实例的属性访问
# 2. 一般的, 在使用点表达式时, **同名的实例属性会覆盖掉类属性**
# 3. 但是如果**类属性是 property, 那么在实例上用点表达式会覆盖掉实例属性**
# 4. 在类上用点表达式会 **destroy property** 

# ###### coding a property factory

# In[79]:


def quantity(storage_name):
    """property factory function
    """
    storage_name_ = '__' + storage_name
    def getter(instance):
        print('Calling getter.')
        return instance.__dict__[storage_name_]
    def setter(instance, value):
        print('Calling setter.')
        if value > 0:
            instance.__dict__[storage_name_] = value
        else:
            raise ValueError('value must be > 0')
    return property(fget=getter, fset=setter)


# In[80]:


class LineItem(object):
    # 创建两个 property
    weight = quantity('weight')
    price = quantity('price')

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight # The property is already active.
        self.price = price

    def subtotal(self):
        return self.weight * self.price


# In[81]:


test = LineItem('zzj', 90, 450)


# In[86]:


# 通过实例的字典看到真正的实例属性
test.__dict__


# ##### Essential Attributes and Functions for Attribute Handling

# 类及其实例的特殊属性:
# 
# 1. \_\_class\_\_: obj.\_\_class\_\_ 等价于 type(obj)
# 2. \_\_dict\_\_: 存放了类或者类的实例的所有**可写属性的字典**
# 3. \_\_slots\_\_: An attribute that may be defined in a class to limit the attributes its instances can have. __slots__ is a tuple of strings naming the allowed attributes. If the '__dict__' name is not in __slots__, then the instances of that class will not have a __dict__ of their own, and only the named attributes will be allowed in them
# 
# Built-in Functions for Attribute Handling:
# 
# 1. dir(\[object\]): 列出了类或类的实例的最多属性, 返回的是列表.
# 2. **getattr(object, name\[, default\])**: Gets the attribute identified by the name string from the object. This may fetch an attribute from the object’s class or from a superclass. If no such attribute exists, getattr raises AttributeError or returns the default value, if given.
# 3. hasattr
# 4. setattr(object, name, value): Assigns the value to the named attribute of object, if the object allows it. This may create a new attribute or overwrite an existing one.
# 5. Returns the __dict__ of object; vars can’t deal with instances of classes that define __slots__ and don’t have a __dict__ (contrast with dir, which handles such in‐stances). Without an argument, vars() does the same as locals(): returns a dict representing the local scope.

# *Special Methods for Attribute Handling*:
# 
# 注意: 
# * 下面的 methods 是作用在 class 上的, 即使点运算符左边的对象是实例.
# * 如果你直接访问了 \_\_dict\_\_ 那么不会出发这些 methods.
# * 这些 methods 不会被实例中同名的属性覆盖掉.
# 
# 
# 1. cls.\_\_delattr(self, name)
# 2. cls.\_\_dir\_\_(self)
# 3. \_\_getattribute\_\_: Always called when there is an attempt to retrieve the named attribute, except when the attribute sought is a special attribute or method. Dot notation and the get attr and hasattr built-ins trigger this method. *__getattr__ is only invoked after __getattribute__, and only when __getattribute__ raises AttributeError*. To retrieve attributes of the instance obj without triggering an infinite recursion, im‐plementations of __getattribute__ should use super().__getattri bute__(obj, name).
# 4. cls.\_\_setattr\_\_(self, name, value)

# In[ ]:




