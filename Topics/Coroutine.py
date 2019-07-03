#!/usr/bin/env python
# coding: utf-8

# ### 生成器函数

# In[1]:


def f():
    print('---start---')
    yield 1
    print('---middle---')
    yield 2
    print('---finished---')


# In[3]:


#和一般的函数不同, 调用生成器函数不会立刻运行
gen = f()


# In[4]:


gen.__next__()


# In[5]:


gen.__next__()


# In[6]:


gen.__next__()


# ### 生成器函数的实现原理

# ### 双边交流
# 
# 1. send(value) (注意 next(g) 等价于 g.send(None))
# 2. throw(type, value=None, traceback=None), 等价于 raise type, value, traceback
# 3. close()

# In[13]:


import itertools
def g():
    print('---start---')
    for i in itertools.count():
        print('---yielding %i---' % i)
        try:
            ans = yield i
        except GeneratorExit:
            print('---closing---')
            raise
        except Exception as e:
            print('---yield raised %r---' % e)
        else:
            print('---yield returned %s' % ans)


# In[14]:


it = g()


# In[15]:


it.__next__()


# In[16]:


it.__next__()


# In[17]:


#传入 121 给 ans
it.send(121)


# In[18]:


#send(None) 相当于 i__next__()
#会生成 i，但是不传进任何的值
it.send(None)


# In[19]:


#抛入的异常会被 except捕捉到
it.throw(IndexError)


# In[20]:


it.close()


# ### 协程--一种针对有序数据的处理方式

# In[1]:


#与子进程不同, 协程都是平等的，它们 协作组成流水线，不带有任何上级函数来负责以特定顺序调用它们。


# In[2]:


#Python 的生成器函数可以使用 yield 语句接受一个值.
#生成器对象上有两个额外的方法, send()和close(),
#定义了这些对象的生成器叫做 协程


# In[5]:


#协程可以通过(yield)语句来消耗值,像下面这样:
"""
value = (yield)
"""
#使用上面的语法, 在使用send方法传递参数之前, 执行流会停在上面那句话上
"""
coroutine.send(data)
"""
#使用了send方法后, 执行会恢复, value会被赋予data的值。
#通过close()方法来关闭协程,这会在协程内部产生 GeneratorExit异常。


# In[8]:


def match(pattern):
    print("Looking for " + pattern)
    while True:
        try:
            s = (yield)
        except GeneratorExit:
            print("===Done===")
            break
        else:
            if pattern in s:
                print(s)


# In[10]:


#我们可以使用一个字符串来初始化 match函数
m = match("Jabberwock")


# In[11]:


#然后调用__next__方法开始执行
#语句会一直执行到 s = (yield) 处，然后暂停,等待一个发送给 m的值
m.__next__()


# In[12]:


m.send("the Jabberwock with eyes of flame")


# In[13]:


m.send("came whiffling through the tulgey wood")


# In[14]:


m.close()


# In[2]:


#我们通过 yield 和 send函数 可以实现一些列复杂的行为
def read(text, next_coroutine):
    for line in text.split():
        next_coroutine.send(line)
    next_coroutine.close()


# In[16]:


#将read函数和match协程链到一起, 就可以创建出一个程序
#只打印出匹配特定单词的单词
text = 'Commending spending is offending to people pending lending!'
matcher = match('ending')


# In[18]:


matcher.__next__()


# In[19]:


#matcher协程中, s = (yield)一行等待每个read函数发送进来的单词,匹配结束后将控制流归还给read
read(text, matcher)


# ### 基于协程的生产-过滤-消耗 模型

# In[20]:


#生产者创建序列中的物品, 使用send()传递给过滤者
#过滤者通过(yield)来消耗物品并通过send()发送给消费者
#消费者使用(yield)来消耗物品但是不发送


# In[30]:


#我们可以将 match拆分为过滤者和消费者
def match_filter(pattern, next_coroutine):
    print('Looking for ' + pattern)
    while True:
        try:
            s = (yield)
        except GeneratorExit:
            next_coroutine.close()
            break
        else:
            if pattern in s:
                next_coroutine.send(s)
def print_consumer():
    print('Preparing to print')
    while True:
        try:
            line = (yield)
        except GeneratorExit:
            print('===Done===')
            break
        else:
            print(line)


# In[31]:


#当过滤者和消费者被构建时, 必须调用__next__方法开始执行
printer = print_consumer()
printer.__next__()


# In[32]:


matcher = match_filter('pend', printer)
matcher.__next__()


# In[33]:


read(text, matcher)


# In[4]:


#过滤者filter不但可以移除元素, 也可以转换元素
def counter_letters(next_coroutine):
    while True:
        try:
            s = (yield)
        except GeneratorExit as e:
            next_coroutine.close()
            break
        else:
            #统计文本中单词的频率
            counts = {letter : s.count(letter) for letter in set(s)}
            next_coroutine.send(counts)
    return

#下面再定义消费者
def sum_dictionaries():
    total = {}
    while True:
        try:
            counts = (yield)
        except GeneratorExit:
            #找出频率最高的单词
            max_letter = max(total.items(), key = lambda t : t[1])[0]
            print("Most frequent letter: " + max_letter)
            break
        else:
            #下面的循环统计单词的总出现次数
            for letter, count in counts.items():
                total[letter] = count + total.get(letter, 0)


# In[5]:


text = 'Commending spending is offending to people pending lending!'
s = sum_dictionaries()
s.__next__()
c = counter_letters(s)
c.__next__()
read(text, c)


# In[6]:


#协程与多任务
#生产者与过滤者可以向多个协程send数据


# In[7]:


def read2many(text, coroutines):
    for word in text.split():
        for coroutine in coroutines:
            coroutine.send(word)
    for coroutine in coroutines:
        coroutine.close()


# In[9]:


#我们可以用 read2many 检测多个单词中的相同文本
m = match('mend')
p = match('pe')
m.__next__()
p.__next__()


# In[10]:


read2many(text, [m, p])


# <center>总结</center>
# 
# 1. 实现了函数级别的并发, 让我们用同步的方式编写异步的代码
# 2. 在适当的时候暂停函数并且在适当的时候重启动函数
# 3. 协程是单线程的, 因此遇到费IO操作务必yield出去

# ### async await

# In[ ]:




