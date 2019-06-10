#!/usr/bin/env python
# coding: utf-8

# ### subprocess 模块

# In[3]:


#用 subprocess 模块管理子进程
import subprocess


# In[4]:


#Popen 开始进程
proc = subprocess.Popen(
    ['echo', 'Hello from the child!'],
    stdout = subprocess.PIPE
)
out, err = proc.communicate()
print(out.decode('utf-8'))


# In[5]:


#子进程的状态可以每隔一段时间被检测到, 通过poll函数
proc = subprocess.Popen(['sleep', '0.3'])
# while proc.poll() is None:
#     print('Working ...')
#     # Some time-consuming work here
# print('Exist status', proc.poll())


# In[6]:


from time import time
#父进程可以平行的运行多个子进程
def run_sleep(period):
    proc = subprocess.Popen(['sleep', str(period)])
    return proc
start = time()
procs = []
for _ in range(10):
    proc = run_sleep(.1)
    procs.append(proc)

#通过 communicate方法终止这些进程
for proc in procs:
    proc.communicate()
end = time()


# In[7]:


#如果这些进程是顺序执行的， 那么总运行时间大约是1s
print('Finished in %.3f seconds' % (end - start))


# In[8]:


#你也可以接收子进程的返回值
#假设你需要用 openssl 命令行工具 加密某些文件
def run_openssl(data):
    env = os.environ.copy()
    env['password'] = b'\xe24U\n\xd0Ql3S\x11'
    proc = subprocess.Popen(
        ['openssl', 'enc', '-des3', '-pass', 'env:password'],
        env = env,
        stdin = subprocess.PIPE,
        stdout = subprocess.PIPE
    )
    #这两行保证了子进程得到输入
    proc.stdin.write(data)
    proc.stdin.flush()
    return proc


# In[9]:


import os
procs = []
for _ in range(3):
    data = os.urandom(10)
    proc = run_openssl(data)
    procs.append(proc)


# In[10]:


for proc in procs:
    out, err = proc.communicate()
    print(out[-10 :])


# In[12]:


#from hashlib import md5
#你也可以将两个子进程串联起来
def run_md5(input_stdin):
    proc = subprocess.Popen(
        ['md5sum'],
        stdin = input_stdin, #注意这里的标准输入来自于另一个子进程的输出
        stdout = subprocess.PIPE
    )
    return proc
input_procs = []
hash_procs = []
for _ in range(3):
    data = os.urandom(10)
    
    proc = run_openssl(data)
    input_procs.append(proc)
    #用proc的标准化输出来作为has_proc的输入
    hash_proc = run_md5(proc.stdout)
    hash_procs.append(hash_proc)


# In[25]:


for proc in input_procs:
    proc.communicate()
for proc in hash_procs:
    out, err = proc.communicate()
    print(out.strip())


# In[26]:


#如果你担心子进程可能不会终止, 那么给communicate()方法传递 timeout参数
proc = run_sleep(.5)
try:
    proc.communicate(timeout = .1)
except subprocess.TimeoutExpired:
    proc.terminate()
    proc.wait()
print('Exit status', proc.poll())


# ### Thread模块
# * 对于IO操作而言, 多线程与多进程性能差别不大
# * Python中使用多线程的方式:
#    1. Thread模块
#    2. 继承Thread类

# In[13]:


#Python的并行是伪并行, 因为GIL的存在
#因数分解，串行版本
def factorize(number):
    for i in range(1, number + 1):
        if number % i ==0:
            yield i 

numbers = [2139079, 1214759, 1516637, 1852285]
start = time()
for number in numbers:
    list(factorize(number))
end = time()
print('Took %.3f seconds' % (end - start))


# In[14]:


#下面用Thread 模块给出并行版本
from threading import Thread
from time import time
class FactorizeThread(Thread):
    def __init__(self, number):
        super().__init__()
        self.number = number
    def run(self):
        self.factors = list(factorize(self.number))

start = time()
threads = []
for number in numbers:
    thread = FactorizeThread(number)
    thread.start()
    threads.append(thread)
for thread in threads:
    thread.join()
end = time()
print('Took %.3f seconds' % (end - start))


# In[15]:


#那么为什么Python要支持多线程呢?
#1.多线程使你的程序 看上去 像是在干一件事。用多线程，你可以让Python来manage function in parallel
#2.用多线程处理I/O中断


# In[16]:


#比如有如下的需求:我们需要请求操作系统中断.1, 然后回到程序的控制
import select
def slow_systemcall():
    select.select([], [], [], .1)
#slow_systemcall()串行调用将线性增加运行时间
start = time()
for _ in range(5):
    slow_systemcall()
end = time()
print('Took %.3f seconds' % (end - start))


# In[17]:


#上面操作的问题是: 当 system_call运行时你的程序 cannot do anything, 因为你主线程被block了5s.
#正因如此, 你需要多线程~~
start = time()
threads = []
for _ in range(5):
    thread = Thread(target = slow_systemcall)
    thread.start()
    threads.append(thread)
#With the threads started, you can do other things you need
for thread in threads:
    thread.join()
end = time()
# 5x speed up!
print('Took %.3f seconds' % (end - start))


# ###### 通过继承Thread类实现多线程

# In[19]:


class GetDetailedHtml(Thread):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
           
    #重点: 重载run方法
    def run(self):
        print('Get detailed html started.')
        time.sleep(4)
        print('Get detailed html end.')


# #### Lock模块
# 1. lock会影响多线程性能
# 2. 会引起死锁

# In[9]:


#用锁来阻止 线程之间的竞争
#注意,即使python有global interpreter lock，你的数据结构也不是线程安全的！！！
from threading import Thread
#*1. work类
class Counter(object):
    def __init__(self):
        self.count = 0
    def increment(self, offset):
        # `+=`不是线程安全的
        self.count += offset


# In[10]:


#*2. worker函数/类
def worker(senser_index, how_many, counter):
    for _ in range(how_many):
        #Do something
        counter.increment(1)


# In[13]:


#*3. run thread 的函数
def run_threads(func, how_many, counter):
    threads = []
    for i in range(5):
        args = (i, how_many, counter)
        thread = Thread(target = func, args =args)
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()


# In[14]:


how_many = 10**5
counter = Counter()
#共5个线程, 它们访问相同的类的实例。调用increment函数 how_many次
run_threads(worker, how_many, counter)


# In[15]:


print('Counter should be %d, found %d' % (5 * how_many, counter.count))


# In[16]:


# counter.count += offset 相当于三句话:
"""
value = getattr(counter, 'count')
result = value + offset
setattr(counter, 'count', result)
"""
#Python 的线程在执行上面三个语句时的任何时刻,都可能被挂起


# In[21]:


#竞争条件的解决方案: Lock
from threading import Lock
class LockingCounter(object):
    def __init__(self):
        self.lock = Lock()
        self.count = 0
    def increment(self, offset):
        #self.lock.acquire()
        with self.lock:
            self.count += offset
        #self.lock.acquire()


# In[23]:


counter = LockingCounter()
run_threads(worker, how_many, counter)
print('Counter should be %d, found %d' % (5 * how_many, counter.count))


# #### RLock模块
# 在同一个线程里面, 你可以连续调用多次 acquire, 但是注意 release的次数必须和acquire次数相等

# In[2]:


from threading import RLock
lock = RLock()
total = 0
def add():
    global total
    global RLock
    for i in range(10):
        #如果是普通的Lock, 你连续acquire两次会造成死锁
        #但是用RLock不会造成死锁.注意在同一个线程里这么用才可以
        lock.acquire()
        lock.acquire()
        total += 1
        lock.release()
        lock.release()
    


# In[4]:


from threading import Thread
threads = []
for i in range(5):
    thread = Thread(target=add, args=())
    threads.append(thread)
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()


# In[5]:


print(total)


# #### Condition模块
# 用于复杂的线程同步:
# 1. 用同一个condition的两个线程, 需要注意启动顺序! 首先启动的是 首先调用wait的线程.
# 2. 要首先调用 with condition 语句(也就是condition.acquire()).
# 3. condtion里默认用RLock, 调用\_\_enter\_\_方法时,acquire这把锁. 当调用wait时, 首先:
#     1. 新建一把锁 waiter.
#     2. waiter 调用 acquire 方法
#     3. 将新建的锁加入到双端队列 waiters 中
#     4. 释放condition的锁, 并且保存当前状态
#     5. waiter 再一次调用 acquire 方法, **造成阻塞**, 只有使用同一个condition的另外一个线程调用notify方法(notify方法会调用 waiter的 release方法), 才有可能解除阻塞.
#     6. 无论是成功解除阻塞或者time out, 都会重新获取condition的锁, 回到原始状态.
#     7. 如果 5 中 waiter没有成功acquire, 会将它从waiters中移除.
# 4. 线程1调用 cond.acquire() --> 线程1调用wait(),首先释放cond的锁, 然后新建waiter,将waiter加入到双端队列,waiter调用两次acquire;</br>
#    线程2 因为线程1在wait中释放了cond的锁, 它得以acquire之.然后线程2 do something后, 首先调用notify, notify会调用waiter的release()</br>.
#    注意此时线程1任然堵塞, **只有线程2调用了wait()后, 线程1才能重新acquire cond的锁, 继续运行**.

# In[3]:


from threading import Thread
from threading import Condition
#通过Condition实现两个线程对话
#首先需要调用 with语句:
##1. wait 方法, 用于等待某个条件变量的通知
##2. notify 方法, 用于通知调用了wait方法的线程启动
class XiaoAi(Thread):
    def __init__(self, condition):
        super().__init__(name='小爱')
        self.cond = condition
    def run(self):
        with self.cond:
            self.cond.wait() #1
            print("{} : 在.".format(self.name))#2
            self.cond.notify() #2
            self.cond.wait() #3
            print('{} : 好啊.'.format(self.name))
class TianMao(Thread):
    def __init__(self, condition):
        super().__init__(name='天猫')
        self.cond = condition
    def run(self):
        with self.cond:
            print("{} : 小爱同学.".format(self.name))#1
            self.cond.notify() #1
            print('hahaha1')
            self.cond.wait() #2
            print('hahaha2')
            print('{} : 我们来对古诗吧.'.format(self.name))
            self.cond.notify() #3       


# In[4]:


condition = Condition()
Xiaoai = XiaoAi(condition)
Tianmao = TianMao(condition)
####!!!!注意用条件变量的时候现成先后启动的循序非常重要!!!先wait的线程先启动
Xiaoai.start()
Tianmao.start()


# #### Semaphore
# 用于控制锁的进入数量

# In[16]:


from threading import Semaphore, Thread
import time


# In[17]:


#模拟爬虫
class HtmlSpider(Thread):
    def __init__(self, url):
        super().__init__()
        self.url = url
    def run(self):
        time.sleep(2)
        print('成功爬取页面 : {0}.\n'.format(self.url))
class UrlProducer(Thread):
    #每次run就调用20个HtmlSpider线程
    def run(self):
        for i in range(10):
            html_thread = HtmlSpider("https://baidu.com/{0}".format(i))
            html_thread.start()


# In[18]:


url_producer = UrlProducer()
url_producer.start()


# In[24]:


#需求: 我们要控制并发爬虫的数量.
#解决方案: threading中的信号量模块
class HtmlSpider(Thread):
    def __init__(self, url, semaphore):
        super().__init__()
        self.url = url
        self.semaphore = semaphore
    def run(self):
        time.sleep(2)
        print('成功爬取页面 : {0}.'.format(self.url))
        #调用了信号量的release方法后, value会加1, 直到加到初始的值
        self.semaphore.release()
        
class UrlProducer(Thread):
    def __init__(self, semaphore):
        super().__init__()
        self.semaphore = semaphore
    def run(self):
        for i in range(10):
            # 调用了信号量的acquire方法后, 信号量会检查它的value属性, 
            # 每有一个新的线程 value减一, 减到零就阻塞.
            self.semaphore.acquire()
            html_thread = HtmlSpider("https://baidu.com/{0}".format(i), self.semaphore)
            html_thread.start()


# In[25]:


semaphore = Semaphore(3)
url_producer = UrlProducer(semaphore)
url_producer.start()


# ### 线程池

# In[2]:


from concurrent import futures


# In[3]:


#为什么需要线程池
## 1. 控制线程并发的数量
## 2. 在主线程中管理子线程的状态, 返回值
## 3. 子线程结束时, 主线程可以获知
## 4. 使得多线程多进程接口一致


# In[9]:


import time
def sleep(times):
    time.sleep(times)
    print('You sleep {0} s'.format(times))
    return 233


# In[10]:


executor = futures.ThreadPoolExecutor(max_workers=4)
#注意 submit方法是会立刻返回的
task_1 = executor.submit(sleep, (3))
task_2 = executor.submit(sleep, (4))

#down 方法用于判断任务是否完成
print(task_1.done())

# result 方法会阻塞直到返回值
print(task_1.result())

# cancel 方法用于取消任务, 但是如果任务正在执行中, 就无法取消
## print(task_2.cancel())


# In[11]:


print(task_1.done())


# In[12]:


#用 as_completed 获取已经成功的任务的返回值
#用 wait 方法 阻塞主线程直到一些子线程的任务返回
from concurrent.futures import as_completed, wait

#as_completed 方法返回成功执行任务的生成器
# for task in as_completed(all_task):
#     data = task.result()

#wait(all_task, return_when=FIRST_COMPLETED)


# ### 用队列实现线程之间的协作

# In[1]:


#用 Queue来实现线程之间的协作
#假设你要做这么一个系统:1. 用你的照相机照连续的相片，然后download到本地 2. 本地resize 照片 3. 把你的照片加进 online gallery里
#你的程序有三个Pipeline: 1.download 2.resize 3. upload


# In[1]:


#可以用生产者-消费者 Queue
from collections import deque
class MyQueue(object):
    def __init__(self):
        self.items = deque()
        self.lock = Lock()
    #生产者, 你的相机, 在队列尾部添加元素
    def put(self, item):
        with self.lock:
            self.items.append(item)
    #消费者, 从队列头部取走元素
    def get(self):
        with self.lock:
            return self.items.popleft()


# In[8]:


#下面把每个pipline用Python thread 表示
from threading import Thread, Lock
from time import sleep
#Worker类, 负责链接管道，输入->工作->输出
class Worker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.polled_count = 0
        self.work_done = 0
    def run(self):
        #每个worker不断的工作，这其实是一个副作用
        while True:
            self.polled_count += 1
            try:
                item = self.in_queue.get()
            except IndexError:
            #如果 in_queue是空
                sleep(.01)
            else:
            #如果in_queue不空,那么取走队列头部的元素后,开始工作
                result = self.func(item)
                self.out_queue.put(result)
                self.work_done +=1


# In[9]:


#下面可以将pipline的三个状态连接起来了
download_queue = MyQueue()
resize_queue = MyQueue()
upload_queue = MyQueue()
done_queue = MyQueue()
def download(item):
    return item
def resize(item):
    return item
def upload(item):
    return item
threads = [
    #downlaod 函数, 从保存照片的downloaded_queue取走照片, 放到resize_queue里
    Worker(download, download_queue, resize_queue),
    #resize 函数, 从保存照片的resize_queue取走照片, 放到upload_queue里
    Worker(resize, resize_queue, upload_queue),
    #upload 函数, 从保存照片的upload_queue取走照片, 放到done_queue里
    Worker(upload, upload_queue, done_queue)
]


# In[10]:


#下面可以开始线程了
#向download_queue 放进1000张"图片", 模拟你的相机
for _ in range(1000):
    download_queue.put(object())


# In[11]:


for thread in threads:
    thread.start()


# In[12]:


while len(done_queue.items) < 1000:
    #Do something else
    pass


# In[18]:


#上面的模式可以运行，但是有一个副作用: except的分支太多!!
#因为每个worker function 的速度不尽相同
#链接两个状态的queue太多， 如果数据很大的话程序可能会崩溃
processed = len(done_queue.items)
polled = sum(t.polled_count for t in threads)
print('Processed', processed, 'items after polling', polled, 'times')


# In[21]:


#解决方案， 用Queue代替 Myqueue
from queue import Queue
###Queue的get方法会自动挂起, 当Queue为空时
queue = Queue()
def consumer():
    print('Comsumer waiting')
    queue.get()
    print('Consumer done')
thread = Thread(target = consumer)
thread.start()


# In[22]:


print('Producer putting')
queue.put(object())
thread.join()
print('Producer done')


# In[28]:


#为了解决管道的挂起问题, Queue可以指定缓存大小
#缓存大小为1, 这意味着producer往 空queue 投放了一个item后, 他必须等待item被取出才能放进下一个
from time import sleep
queue = Queue(maxsize=1)
def consumer():
    sleep(.1)
    #这一句会挂起直到空queue里放进第一个元素
    queue.get()
    print('Consumer got 1') # 2
    queue.get()
    print('consumer got 2') # 4

thread = Thread(target = consumer)
thread.start()

queue.put(object()) 
print('Producer put 1') # 1
queue.put(object()) 
print('Producer put 2') # 3
thread.join() 
print('Producer done')


# In[25]:


#Queue也可以跟踪工作进程,通过**task_done方法**和**join**方法
in_queue = Queue()
def consumer():
    print('Consumer waiting')
    work = in_queue.get() #2
    print('Consumer working')
    #Doing work
    print('Consumer done')
    in_queue.task_done() #3
Thread(target = consumer).start()

in_queue.put(object())  #1
print('Producer waiting') 
#你必须在某个地方调用task_done方法, 不然join这里会一直阻塞!!!!!!!!
in_queue.join() #4
print('Producer done')


# In[62]:


#让我们为Queue加入一些新的功能让他更加适合我们的任务

#ClosableQueue继承了Queue, 增加了队列尾部的Flag
#ClosableQueue 实现了 __iter__他是一个可迭代对象, 并且自带for循环终止判断
class ClosableQueue(Queue):
    SENTINEL = object()
    #子类增加一个close方法, 在尾部放入 SENTINEL元素, 这是你放入的最后一个元素, 
    #当get到这一个元素时, 说明Queue已经为空
    def close(self):
        self.put(self.SENTINEL)
    def __iter__(self):
        while True:
            item = self.get()
            try:
                #如果迭代到最后一个元素,就 return 使得Thread终止
                if item is self.SENTINEL:
                    return
                #别忘了这句
                yield item
            finally:
                self.task_done()


# In[63]:


class StoppableWorker(Thread):
    def __init__(self, func, in_queue, out_queue):
        super().__init__()
        self.func = func
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.polled_count = 0
        self.work_done = 0
    def run(self):
        #ClosableQueue定义了 __iter__方法后,便能如此遍历queue了
        #循环退出的标志是get到最后一个元素
        for item in self.in_queue:
            result = self.func(item)
            self.out_queue.put(result)        


# In[64]:


#Re-create pipelines
download_queue = ClosableQueue()
resize_queue = ClosableQueue()
upload_queue = ClosableQueue()
done_queue = ClosableQueue()
def download(item):
    return item
def resize(item):
    return item
def upload(item):
    return item
threads = [
    #downlaod 函数, 从保存照片的downloaded_queue取走照片, 放到resize_queue里
    StoppableWorker(download, download_queue, resize_queue),
    #resize 函数, 从保存照片的resize_queue取走照片, 放到upload_queue里
    StoppableWorker(resize, resize_queue, upload_queue),
    #upload 函数, 从保存照片的upload_queue取走照片, 放到done_queue里
    StoppableWorker(upload, upload_queue, done_queue)
]


# In[65]:


#启动线程
for thread in threads:
    thread.start()
#模拟在线环境, 为download_queue填入元素, 然后关闭它
for _ in range(1000):
    download_queue.put(object())
download_queue.close()


# In[66]:


#help(Queue.join)


# In[67]:


#如何掌握线程的进度?
#Queue的 join方法, 程序暂停，直到queue里面所有的元素都被取出,程序继续运行
download_queue.join() 
resize_queue.close() 
resize_queue.join() 
upload_queue.close() 
upload_queue.join()


# In[68]:


print(done_queue.qsize(), 'items finished')


# In[69]:


#在用Pipeline时需要注意三个点: busy waiting, stopping workers, memory explosion


# ### 协程

# In[70]:


#用协程并发的跑若干函数
#python的Thread模块有以下缺点:
##1.Thread需要借助其他的工具来实现communicate, 如 Lock 和 Queue。增加了扩展和维护成本
##2.每个Thread需要大概 8MB 内存，如果要并发运行大量函数，那么给每个函数分配一个线程显然不现实
##3. 开启每个Thread耗费时间，要是你要并发运行大量函数那么线程的开启耗时是很可观的


# In[71]:


#下面展示routine的用法
def my_coroutine():
    while True:
        received = yield
        print('Received:', received)


# In[73]:


it = my_coroutine()
#首次使用协程时需要调用next方法
#这将使得生成器为 第一次接受 send() 函数的值做准备
next(it)


# In[74]:


it.send('First')
it.send('Second')


# In[78]:


#下面展示一个具体的例子
def minimize():
    #接受第一次的send()
    current = yield
    while True:
        value = yield current
        print(current, value)
        current = min(value, current)
        


# In[79]:


it = minimize()
next(it)
print(it.send(10))


# In[80]:


print(it.send(4))


# ### 使用cocurrent.futures 实现真正的并行化

# In[1]:


#下面用最大公约数算法来模拟 计算密集型的应用
#时间复杂度 O(n)
def gcd(pair):
    a, b = pair
    low = min(a, b)
    for i in range(low, 0, -1):
        if a % i == 0 and b % i == 0 :
            return i


# In[2]:


numbers = [(1963309, 2265973), (2030677, 3814172), 
           (1551645, 2229620), (2039045, 2020802)]


# In[3]:


from time import time
start = time()
results = list(map(gcd, numbers))
end = time()
print('Took %.3f seconds' % (end - start))


# In[5]:


#按照前面的结论, 用Thread模块不会加速, 因为GIL
#解决方案: concurrent.futures


# In[6]:


from concurrent.futures import ThreadPoolExecutor


# In[8]:


#这样会更慢, 因为线程的启动和交流耗时
start = time()
pool = ThreadPoolExecutor(max_workers = 2)
results = list(pool.map(gcd, numbers))
end = time()
print("Took %.3f seconds" % (end - start))


# In[9]:


from concurrent.futures import ProcessPoolExecutor
start = time()
pool = ProcessPoolExecutor(max_workers = 2)
results = list(pool.map(gcd, numbers))
end = time()
print("Took %.3f seconds" % (end - start))


# In[10]:


#下面简单解释一下 ProcessPoolExecutor 是如何工作的
##1. 从 numbers 将每个元素元素取到 map里
##2. 将map的数据 序列化, 通过pickle模块
##3. 将序列化的数据从主进程copy到子进程里
##4. 子进程中用pickle模块 将数据解序列化
##5. 子进程中将包含有 gcd函数的模块导入
##6. 每个子进程gcd函数
##7. 将结果序列化
##8. 将序列化的结果 copy回 socket
##9. 在主进程中将结果解序列化
##10. 主进程中将这些结果合并成列表


# In[19]:


from datetime import datetime
datetime.utcnow()


# In[20]:


help(datetime.utcnow)


# In[ ]:




