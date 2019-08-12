#!/usr/bin/env python
# coding: utf-8

# 我们的示例数据集如下图所示:
# 
# ![img/19_1.png](img/19_1.png)
# 
# 这是一个 Json 文件. 注意 conference, events, speakers 和 venues 的 值是列表, 列表的每一个元素是字典

# In[6]:


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


# In[12]:


# 检查下载的Json文件
raw_feed = load()
print(sorted(raw_feed['Schedule'].keys()))

for key, value in sorted(raw_feed['Schedule'].items()):
    print('{:3} {}'.format(len(value), key))


# ###### Exploring JSON-Like Data with Dynamic Attributes

# In[11]:


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

# In[19]:


feed = FrozenJSON(raw_feed)
len(feed.Schedule.speakers)


# In[20]:


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

# In[24]:


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


# In[27]:


feed = FrozenJSON(raw_feed)

# feed.Schedule.speakers


# ###### 用 shelve 模块来重新构建数据

# In[30]:


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
        for record in rec_lsit:
            key = '{}.{}'.format(record_type, record['serial']) #4
            print(record['serial'])
            record['serial'] = key #5
            db[key] = Record(**record) #6


# <center>总结</center>
# 
# 1. 通过更新 \_\_dict\_\_ 来批量初始化实例变量 (Note: depending on the application context, the Record class may need to deal with keys that are not valid attribute names.)
# 2. Iterate over collections under 'Schedule'(Schedule 是最上层的键)
# 3. record_type is set to the collection name without the trailing 's' (i.e., 'events' becomes 'event')
# 4. build key and 'serial' field
# 5. Update the 'serial' field with the full key
# 6. Build Record instance and save it to the database under the key

# 下面扩展 Record class

# In[31]:


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
        db = cls.get_db()
        try:
            return db[ident]
        except TypeError:
            if db is None:
                msg = "database not set; call '{}.set_db(my_db)'"
                raise MissingDatabaseError(msg.format(cls.__name))
            else:
                raise
    def __repr__(self):
        if hasattr(self, 'serial'):
            cls_name = self.__class__.__name__
            return '<{} serial={!r}>'.format(cls_name, self.serial)
        else:
            return super().__repr__()


# In[32]:


class Event(DbRecord):
    
    @property
    def venue(self):
        key = 'venue.{}'.format(self.venue_serial)
        return self.__class__.fetch(key)
    @property
    def speakers(self):
        if not hasattr(self, '_speaker_objs'):
            spkr_serials = self.__dict__['speakers']
            fetch = self.__class__.fetch
            self._speaker_objs = [fetch('speaker.{}'.format(key))                                  for key in spkr_serials]
        return self._speaker_objs
    
    def __repr__(self):
        if hasattr(self, 'name'):
            cls_name = self.__class__.__name__
            return '<{} {!r}>'.format(cls_name, self.name)
        else:
            return super().__repr__()


# In[ ]:


import inspect
def load_db_v2(db):
    raw_data = load()
    warnings.warn('loading ' + DB_NAME)
    for collections, rec_list in raw_data['Schedule'].items():
        record_type = collections[:-1]
        cls_name = record_type.capitalize()
        cls = globals().get(cls_name, DbRecord)
        if inspect.isclass(cls) and issubclass(cls, DbRecord):
            factory = cls
        else:
            factory = DbRecord
        for record in rec_list:
            key = '{}.{}'.format(record_type, record['serial'])
            record['serial'] = key
            db[key] = factory(**record)  # <8>
        

