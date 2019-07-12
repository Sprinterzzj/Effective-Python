#!/usr/bin/env python
# coding: utf-8

# ### Python 迭代器
# 迭代器实现了两个协议:
# * 1. \_\_next\_\_ 返回当前元素并计算下一个元素以及判断迭代终止
# * 2. \_\_iter\_\_ 简单返回迭代器
# 
# 迭代器用来实现有序数据序列的顺序访问, 注意不是随机访问！！

# In[8]:


#下面的 Letters class 迭代了从 'a' 到 'd' 的字母序列
# Letters 的任何实例只可以迭代一次. 一旦抛出 StopIteration
# 异常, 它的状态就一直这样了，除非创建新的实例
class Letters(object):
    def __init__(self):
        self.current = 'a'
    def __next__(self):
        # if 语句判断迭代是否终止
        if self.current > 'd':
            raise StopIteration
        result = self.current
        self.current = chr(ord(result) + 1)
        return result
    def __iter__(self):
        return self


# In[16]:


letters = Letters()

print(id(letters) == id(letters.__iter__()))

print(next(letters))
print(next(letters))
print(next(letters))
print(next(letters))
print(next(letters))


# In[17]:


letters = Letters()
for l in letters:
    print(l)


# In[10]:


#下面的 Positives class 实现了无限序列
class Positive(object):
    def __init__(self):
        self.current = 0
    def __next__(self):
        result = self.current
        self.current += 1
        return result
    def __iter__(self):
        return self


# In[12]:


pos = Positive()
for i in range(10):
    print(next(pos))


# #### 使用 for 语句配合迭代器

# In[2]:


#1. counters list 通过 __iter__方法返回迭代器
#2. for 语句 反复调用迭代器的 __next__方法，每次都将当前值赋值给 item
#   直到遇到 StopIteration 异常, for循环终止
counts = [1, 2, 3, 4, 5]
for item in counts:
    print(item)


# In[3]:


#由此, 我们可以这样模拟for语句的求值规则:
#1. 首先调用 __iter__方法返回一个迭代器
#2. 然后反复调用迭代器的__next__方法直到StopIteration 异常
i = counts.__iter__()
while True:
    try:
        item = i.__next__()
    except StopIteration:
        break
    else:
        print(item)


# ### 生成器

# In[4]:


#上面的Letters class 中，我们引入self.current属性来跟踪序列当前的状态。
#对于复杂的序列，这么做可能会使得__next__()方法消耗过多内存
#解决方法: 生成器


# In[5]:


#生成器是一种特殊的函数, 使用 yield 关键字返回序列中的元素
#每次调用 __next__方法时, 执行到下一个 yield 语句
def letters_generator():
    current = 'a'
    while current <= 'd':
        #生成当前的 current
        yield current
        #计算下一个位置的 current
        current = chr(ord(current) + 1)


# In[7]:


#即便没有显示定义 __next__和__iter__ 方法,
#Python 会理解我们使用 yield 关键字时, 我们打算定义生成器.

#在调用时, 生成器不反回特定产出值, 而是返回一个生成器(一种迭代器), 其自身可以返回产出的值
#生成器对象有 __iter__和__next__方法, 
###每个对next的调用都会从上次停留的地方继续执行生成器函数直到另一个yield语句执行的地方
for letter in letters_generator():
    print(letter)


# In[13]:


#__next__第一次调用: 程序从函数体一直执行到进入 yield 语句。
#之后, 程序暂停并且返回 current 的值。
#yield语句并不破坏新创建的环境, 而是为之后的使用保留了它。

#下面手动调用__next__来遍历生成器
letters = letters_generator()
type(letters)


# In[14]:


print(letters.__next__())
print(letters.__next__())
print(letters.__next__())
print(letters.__next__())
print(letters.__next__())


# ####  生成器在UserList中的应用

# In[2]:


#如果你要实现自己list class, 你应该继承UserList.
from collections import UserList


# #### 生成器读取大文件

# In[4]:


def readlines(f, newline):
    """
    Parameters
    ----------
    f : 文件的句柄, 注意这里的文件只有一行, 大小可能有500G
    newline : 你自己定义的分隔符
    """
    #buf缓存
    buf = ''
    while True:
        #内循环不断的在buf中找分隔符(newline)
        while newline in buf:
            #找到newline的位置
            pos = buf.index(newline)
            # yield newline之前的内容
            yield buf[: pos]
            # 更新buf
            buf = buf[pos + len(newline) : ]
        #如果buf里面没有newline了, 就继续读一块chunk
        chunk = f.read(4096 * 10)
        #判断 chunk是否读取, 如果没有读取那么说明文件已被读完, yiled剩下的buf后
        #循环终止
        if not chunk:
            yield buf
            break
        #我们把读到的chunk加到缓存中
        buf += chunk
            


# In[ ]:


#应用
# with open('big_txt.txt') as f:
#     for line in readlines(f, '{|}'):
#         print(line)


# ### Python 中的可迭代对象
# 可迭代对象与迭代器不一样, 可迭代对象只需要实现 \_\_iter\_\_方法

# In[21]:


#在 Python 中, 迭代只能遍历一次元素
#但我们有时需要多次迭代,例如:
def all_pairs(s):
    return ((s1, s2) for s1 in s for s2 in s)


# In[22]:


type(all_pairs([1, 2, 3, 4]))


# In[23]:


list(all_pairs([1,2,3,4]))


# In[18]:


#注意, 序列本身不是迭代器, 但它是可迭代对象。
#Pyhton的可迭代对象只包含一个接口, __iter__, 返回一个迭代器。
#Pyhton的 built-in 序列类型在 __iter__ 方法调用时, 返回迭代器的新的实例。
#因此, 因此他们可以被多次迭代!!!
#注意上面的 Letters class, 它的__iter__返回自身, 而不是新的实例


# In[19]:


class LetterIterable(object):
    def __iter__(self):
        #等价于 return (x for x in list('abcd'))
        current = 'a'
        while current <= 'd':
            yield current
            current = chr(ord(current) + 1)


# In[24]:


#__iter__ 方法定义为生成器函数, 他返回一个生成器对象产出 从 'a'到 'd'的字母
#Letters class 的一个实例只可以迭代一次，LetterIterable可以迭代多次
letters = LetterIterable()
list(all_pairs(letters))


# In[26]:


#你可以反复调用LetterIterable的同一个实例
list(all_pairs(letters))


# #### 如何设计一个可迭代对象?
# 1. 我们需要定义 \_\_iter\_\_方法
# 2. 但是在\_\_iter\_\_中, 将返回的迭代器**委托**给其他类的实例！！！

# In[3]:


from collections import Iterator
class MyIterator(Iterator):
    def __init__(self, employee_list):
        self.iter_list = employee_list
        self.index = 0
    def __next__(self):
        try:
            word = self.iter_list[self.index]
        except IndexError:
            #注意迭代器需要抛出 StopIteration
            raise StopIteration
        else:
            self.index += 1
            return word         


# In[4]:


class Company(object):
    def __init__(self, employee_list):
        self.employee = employee_list
    # __Iter__方法返回一个迭代器的新的实例
    def __iter__(self):
        return MyIterator(self.employee)


# ### Python 流

# In[48]:


#Stream 是惰性计算的递归列表
#Stream 的剩余部分是惰性计算的, 它提供了计算剩余部分的方法。

class Stream(object):
    """
    一个惰性计算的递归列表
    """
    def __init__(self, first, compute_rest, empty = False):
        self.first = first
        self._compute_rest = compute_rest
        self.empty = empty
        self._rest = None
        self._computed = False
    @property
    def rest(self):
        """
        返回流的剩余部分, 在必要时计算它们
        """
        assert not self.empty #空 stream没有剩余部分
        if not self._computed:
            #计算剩余部分
            self._rest = self._compute_rest()
            self._computed = True
        return self._rest
    def __repr__(self):
        if self.empty:
            return '<empty stream>'
        return 'Stream({0}, <compute_rest>)'.format(repr(self.first))


# In[42]:


#我们可以创建一个 Stream 来表示 1 和 5 的序列。 
#Stream 在请求剩余部分之前，并不 会实际计算下一个元素 5 。


# In[43]:


#通过 Lambda 运算 使得 class callable
#
s = Stream(first = 1, compute_rest =  lambda : Stream(first = 2 + 3,  compute_rest = lambda : Stream.empty))


# In[44]:


s.first


# In[45]:


s.rest.first


# In[46]:


#当 构建 Stream的实例 s 时, s._computed is False。这代表s._rest 没有被计算。
#当调用s.rest时, s._rest = s._compute_rest() 计算出Stream的剩余部分, 然后令 s._computed = True
## Stream数据结构的核心是 _compute_rest 方法, 这一方法没有任何输入参数,并且返回 Stream实例。


# In[49]:


#惰性计算可以让我们表示无限长的序列。
#无论如何请求 make_integer_stream()的rest, 都会自增地调用其本身。
def make_integer_stream(first = 1):
    def compute_rest():
        return make_integer_stream(first + 1)
    return Stream(first, compute_rest)


# In[50]:


ints = make_integer_stream()


# In[51]:


ints.first


# In[52]:


ints.rest


# In[53]:


ints.rest.first


# In[54]:


ints.rest.rest


# In[55]:


#map_stream 和 filter_stream 展示了流式处理的常见模式：无论流的剩余部分何时被计算，
#局部定义的 compute_rest 函数都会对流的剩余部分递归调用某个处理函数。


# In[80]:


#map_stream, Stream上的映射函数.
#局部定义的compute_rest()确保了计算rest时,会在Stream的剩余部分上映射
def map_stream(fn, s):
    if s.empty:
        return s
    def compute_rest():
        return map_stream(fn, s.rest)
    return Stream(fn(s.first), compute_rest)
#filter_stream, Stream上的过滤函数。
#compute_rest在 Stream 的剩余部分上调用filter函数，
##如果 filter函数拒绝了 Stream的第一部分,那么剩余部分会被立刻计算出来
def filter_stream(fn, s):
    if s.empty:
        return s
    def compute_rest():
        return filter_stream(fn, s.rest)
    if fn(s.first):
        return Stream(s.first, compute_rest)
    print('{0} is removed!'.format(s.first))
    return compute_rest()


# In[81]:


#为了观察Stream的内容将其截断并且转化为List

#截断Strteam的函数
def truncate_stream(s, k):
    if s.empty or k == 0 :
        return Stream.empty
    def compute_rest():
        return truncate_stream(s.rest, k - 1)
    return Stream(s.first, compute_rest)
#将Stream的内容保存到List里
def stream_to_list(s):
    r = []
    while not s.empty:
        r.append(s.first)
        s = s.rest
    return r


# In[67]:


#下面我们验证 map_stream的实现
Stream.empty = Stream(None, None, True)
s = make_integer_stream(3)


# In[68]:


s


# In[69]:


m = map_stream(lambda x: x**2, s)


# In[70]:


m


# In[71]:


stream_to_list(truncate_stream(m, 5))


# In[88]:


##“递归地”理解下面的函数
##Stream通过 高阶函数 实现了惰性求值


# In[82]:


#我们可以用 filter_stream函数来定义素数流,
#这一流实现了埃拉托斯特尼筛法: 对整数流过滤, 移除first倍数的所有元素
def primes(pos_stream):
    def not_divible(x):
        return x % pos_stream.first != 0
    def compute_rest():
        return primes(filter_stream(not_divible, pos_stream.rest))
    return Stream(pos_stream.first, compute_rest)


# In[83]:


p1 = primes(make_integer_stream(2))


# In[84]:


p1


# In[85]:


p1.rest


# In[86]:


p1.rest.rest


# In[87]:


p1.rest.rest.rest


# In[ ]:




