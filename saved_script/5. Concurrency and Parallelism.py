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
#1.用多线程，你可以让Python来manage function in parallel
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


# python的Thread模块有以下缺点:
# 
# 1. Thread需要借助其他的工具来实现communicate, 如 Lock 和 Queue。增加了扩展和维护成本
# 2. 每个Thread需要大概 8MB 内存，如果要并发运行大量函数，那么给每个函数分配一个线程显然不现实
# 3. 开启每个Thread耗费时间，要是你要并发运行大量函数那么线程的开启耗时是很可观的

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


# ###### Future 对象
# 1. executor submit后将返回一个 concurrent.futures 下面的 Future class的一个实例对象, 这是task的返回容器

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


# In[63]:


#在用Pipeline时需要注意三个点: busy waiting, stopping workers, memory explosion


# ### 多进程multiprocessing
# 1. 用多进程来执行 耗CPU的任务
# 2. 用多线程来执行 IO任务

# In[65]:


#使用 multiprocessing 的进程池
import multiprocessing


# In[4]:


import time
def get_html(n):
    time.sleep(n)
    return [1, 2, 3]   


# In[77]:


#创建一个最多容纳5个进程的进程池
pool = multiprocessing.Pool(processes=5)

#用异步调用函数来执行
#注意args参数后面要有一个逗号
result_1 = pool.apply_async(get_html, args=(3, ))
result_2 = pool.apply_async(get_html, args=(3, ))

#用join方法等待所有进程完成, 注意在join之前必须调用close方法!!!
pool.close()
pool.join()

#打印结果
print(result_1.get())
print(result_2.get())


# ### 使用Queue, Pipe 和 Manager 完成进程间通信
# 1. 注意Thread模块中的各种锁显然不能在多进程中使用
# 2. 同样线程安全的Queue也无法在多进程中使用, 取而代之用 multiprocessing 中的 Queue
# 3. 但是多进程中的Queue模块无法用于进程的进程池(Pool), 取而代之用 Manager.Queue
# 4. 共享全局变量无法用于多进程编程
# 5. Pipe只能适用于两个指定的进程

# In[5]:


from multiprocessing import Pipe, Queue, Manager
from multiprocessing import Process
import time

#下面通过Pipe实现进程间通信
#实例化Pipe后得到两个 connection对象: 接收管道和发送管道
rev, send = Pipe()
def producer(send_pipe):
    send_pipe.send('zzj')
    time.sleep(2)
    return
def consumer(recv_pipe):
    print('I get {0}.'.format(recv_pipe.recv()))
    return
my_producer = Process(target=producer, args=(send, ))
my_consumer = Process(target=consumer, args=(rev, ))

my_producer.start()
my_consumer.start()

my_producer.join()
my_consumer.join()


# ###### 通过 Manager 进程间共享内存

# In[11]:


from multiprocessing import Manager


# ### 协程和异步IO
# 一些常见概念:
# 
# 1. 并发: 一个*时间段*内有几个程序同时在*同个CPU*上运行, 但是任意时刻只准有一个程序在该CPU上运行.
# 2. 并行: 在任意时间点上, 同时多个程序运行在多个CPU上
# 3. 同步: 指代码调用IO操作时, 必须等待IO操作完成才能返回的调用方式
# 4. 异步: 指代码调用IO操作时, 无需等待IO操作完成才能返回的调用方式
# 5. 阻塞: 调用函数的时候当前线程被挂起
# 6. 非阻塞: 调用函数的时候当前线程不会挂起, 而是立即返回

# ###### Unix下的五种I/O模型
# 1. 阻塞式IO
# 2. 非阻塞式IO
# 3. IO多路复用(重点!!!): 通过一种机制, 一个进程可以监视多个描述符, 一旦某个描述符就绪(一般是读就绪), 能够通知程序进行相应的读写操作.
# 4. 信号驱动式IO
# 5. 异步IO
# 
# <center>select, poll, epoll</center>
# 
# 1. 三者都是I/O多路复用的机制, 本质上都是同步I/O, 因为都需要读写时间就绪后自己负责读写,也就是说读写过程是阻塞的.
# 2. 注意真.异步I/O无需自己负责读写, 异步I/O的实现会负责把数据从内核拷贝到用户空间.
# 3. select: select函数监事的文件描述符分为3类, 分别是 writefds, readfds 和 exceptfds. 调用select后会阻塞, 直到有描述符就绪或超时函数返回, select返回后便利fdset可以找到就绪的描述符
# 4. poll: 不同于select使用三个位图来表示三个fdset, poll使用一个人pollfd指针实现. pollfd结构包含了要监视的event和发生的event, 不再使用select参数-值传递的方式. 同时pollfd**有最大数量限制**和select函数一样poll返回后通过pollfd来获取就绪的描述符
# 5. epoll: 在linux2.6内核中提出. epoll没有描述符限制, epoll使用一个文件描述符管理多个描述符, 将用户关系的文件描述符的事件存放到内核的一个事件表中.这样在用户空间和内和空间的copy只需要一次.

# ###### select+回调+事件循环获取html

# In[18]:


# 通过非阻塞io实现http请求
# select + 回调 + 事件循环
# 并发性高
# 使用单线程

import socket
from urllib.parse import urlparse
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE
selector = DefaultSelector()
urls = []
stop = False
request = "GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n"


# In[19]:


class Fetcher(object):
    def _connected(self, key):
        """socket 链接建立好之后的回调函数, 完成发送数据
        """
        #首先需要取消原来注册的事件
        selector.unregister(key.fd)
        self.client.send(
            request.format(self.path, self.host).encode("utf8"))
        #发送数据后, 继续监听socket是否可读
        selector.register(self.client.fileno(), EVENT_READ, self._readable)

    def _readable(self, key):
        """从内核空间读取数据到用户空间, 注意这里不能用while循环.
        因为可读状态不代表内核空间的数据已经完成!而只要状态是可读的,
        那么我们的时间循环里面就会一直调用回调函数完成隐式的while循环
        """
        d = self.client.recv(1024)
        if d:
            self.data += d
        else:
            selector.unregister(key.fd)
            data = self.data.decode('utf8')
            html_data = data.split('\r\n\r\n')[1]
            print(html_data)
            self.client.close()
            urls.remove(self.spider_url)
            if not urls:
                global stop
                stop = True

    def get_url(self, url):
        self.spider_url = url
        url = urlparse(url)
        self.host = url.netloc
        self.path = url.path
        self.data = b''
        if self.path == '':
            self.path = '/'
        # 建立socket链接
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.setblocking(False)

        try:
            self.client.connect((self.host, 80))  # 阻塞不会消耗cpu
        except BlockingIOError as e:
            pass
        # 注册
        selector.register(fileobj=self.client.fileno(), #socket的文件描述符 
                          events=EVENT_WRITE, #事件, 我们建立好链接后要向它发送请求
                          data=self._connected #回调函数
                         )


# 1. selector 的 select方法返回一个 namedtuple list.
# 2. 这个namedtuple(名字叫SelectorKey) 有四个值: fileobj, fd, events, data
# 3. 回调函数放在data里, 注册时的文件描述符在fd里

# In[20]:


def loop():
    """事件循环, 不停地请求socket的状态并且调用对应的回调函数, 注意:
    1. select本身不支持register模式
    2. socket状态变化后的回调是由程序员完成的
    """
    while not stop:
        ready = selector.select()
        for key, value in ready:
            #获得回调函数
            call_back = key.data
            call_back(key)


# In[21]:


import time
fetcher = Fetcher()
start_time = time.time()
for url in range(3):
    url = 'http://shop.projectsedu.com/goods/{}/'.format(url)
    urls.append(url)
    fetcher = Fetcher()
    fetcher.get_url(url)
loop()
print(time.time()-start_time)


# ###### 回调之痛
# 
# 1. 原本深度优先的同步代码被割裂
# 2. 回调函数执行不正常该怎么办?
# 3. 回调里面嵌套回调怎么办??
# 4. 嵌套回调里面出了异常怎么办??
# 5. 变量共享??

# #### 协程

# ###### 生成器的 send close 和 throw方法
# 

# 在生成器内部使用:
# ```python
# a = yield 1
# ```
# 这行代码有两个用处: 
# 
# 1. 向外部发送值(1) 
# 2. 从外部接受值并且赋值到 a
# 当生成器运行到上面语句的位置时:
# 
# ```python
# #接收到1
# next(gen)
# #传递值并且赋值给a
# gen.send('a')
# 
# ```

# In[28]:


def gen_func(): 
    yield 0
    a = yield 1
    print(a)
    yield 2
    yield 3


# In[29]:


gen = gen_func()
print(next(gen))
#注意, 第二次调用next方法, 会先执行等式右边的语句, 传出 1
print(next(gen))
#send方法重启生成器并且执行到下一句yield
print(gen.send('a'))


# 通过使用
# 
# ```python
# gen.close()
# ```
# 在生成器暂停的yield语句之前抛入**GeneratorExit**异常, 注意:
# 
# 1. 调用了close方法后如果**生成器内部捕捉到异常并且不作任何处理**, 且**还有未执行的yield语句**则会向外抛出**RuntimeError**异常.
# 2. 如果不想抛出RuntimeError异常可以不做异常捕捉, 或者在生成器内部捕捉到GeneratorExit异常后 raise StopIteraion

# In[1]:


def gen_func():
    yield 1
    try:
        yield 2
    except RuntimeError:
        yield 5
    yield 3
    yield 4


# 下面调用生成器的throw方法, 注意:
# 
# 1. 在生成器内部异常的位置是当前**暂停处yield的之前的yield的位置**;
# 2. 如果生成器内部捕捉到到了异常, 那么暂停处之前的yield不会被执行(它在try语句里面), 会转而执行except; 如果except为里面没有yield,当前暂停处的yield语句会被执行.

# In[2]:


gen = gen_func()
print(next(gen))
print(next(gen))
#gen.throw(RuntimeError, '')


# In[5]:


gen = gen_func()
print(next(gen))
print(next(gen))
#注意此时生成器停在 yield 3的位置,
#调用 throw 方法后会进入 yield 3 之前的
#那个 yield语句(也就是 yield 2)的位置
#抛入异常
print(gen.throw(RuntimeError, ''))


# ###### 生成器的 yield from 方法
# 
# yield from 后面需要跟 iterable 对象(注意生成器函数也是可迭代的)

# In[6]:


#实现 itertools.chain方法
def my_chain(*args):
    for arg in args:
        yield from arg


# In[12]:


my_list = [1]
my_dict = {'a': 1}
my_range = range(-2,-1)
for value in my_chain(my_list, my_dict, my_range):
    print(value)


# 注意 yield 和 yield from 的区别

# In[17]:


#直接生成 range(1, 3)
def g1():
    yield range(1, 3)

#可以直接拿来迭代
def g2():
    yield from range(1, 3)

for g in g1():
    print(g)
for g in g2():
    print(g)


# **重要**: yield from 在调用方和子生成器之间建立了**双向通道**
# 在下面的代码中:
# 
# 1. main函数: 调用方
# 2. g1: 委托生成器
# 3. gen: 子生成器
# 
# **子生成器退出时会发出StopIteration异常**, 这个异常只能在调用者处处理, 如果不想处理
# 需要在委托生成器中加入while循环

# In[20]:


def gen():
    print('子生成器激活')
    x = yield
    print(x)
    print('子生成器终止')
    return
def g1():
    print('委托生成器激活')
    yield 3
    print('委托生成器激活子生成器')
    yield from gen()
    print('委托生成器终止')

def g2():
    print('委托生成器激活')
    yield 3
    while True:
        print('委托生成器激活子生成器')
        yield from gen()
    print('委托生成器终止')
    

#调用方可以直接访问到子生成器 gen
def main1():
    g = g1()
    # 激活委托生成器
    print(next(g))
    # 激活子生成器
    next(g)
    try:
        g.send(15)
    except StopIteration:
        print('调用者退出')


def main2():
    g = g2()
    print(next(g))
    # 激活子生成器
    next(g)
    g.send(15)
    g.send(None)
    print('调用者退出')    
    


# In[21]:


main1()


# In[22]:


main2()


# 一个简单的应用:

# In[5]:


final_result = {}
#子生成器
def sales_sum(pro_name):
    total = 0
    nums = []
    print('子生成器激活')
    while True:
        print(pro_name + '等待接受.')
        x = yield
        if x is None:
            print('子生成器终止')
            break
        else:
            print(pro_name+'销量: ', x)
            total += x
            nums.append(x)
    print('子生成器循环终止.')
    return total, nums
    
    
        
#委托生成器
def middle(key):
    print('委托生成器激活.')
    i = 0
    while True:
        print('第{0}次进入while循环'.format(i+1))
#         a = yield
#         print(a)
        final_result[key] = yield from sales_sum(key)
        print(key+ '销量统计完成.')
        i += 1
    print('委托生成器循环终止.')

def main():
    #准备测试数据集,
    #注意实际应用中数据集可能是不定长的
    data_sets = {
        '面膜' : [1200, 1500, 3000],
        '手机' : [28, 55, 98, 108],
        '大衣' : [280, 560, 778, 70]
    }
    for key, data_set in data_sets.items():
        print('开始统计: ', key)
        #建立子生成器和调用者的通道
        m = middle(key)
        
        print('调用者开始激活.')
        #重要: 调用者通过激活委托生成器来激活子生成器
        #1. 委托生成器激活
        #2. 第一次进入(委托生成器)while循环
        #3. 子生成器激活
        next(m)
        for value in data_set:
            #4. XX等待接受
            m.send(value)
            #5. XX销量: YY
        
        #6.子生成器终止
        #7. 子生成器循环终止
        
        #子生成器return, 并且抛出 StopIteration异常;
        #yield from 会自动将return赋值给等号左边
        
        #8. XX销量统计完成
        #注意看这里: 
        ###9.第二次进入while循环
        ###10. 自生成器激活
        ###11. 面膜等待接受
        m.send(None)
        #这时我们可以再send一个, 当然无意义.....
        m.send(30000)
        break
    print('Final Result:', final_result)


# In[6]:


main()


# ###### yield from 大致原理
# 
# ```python
# RESULT = yield from EXPR
# ```
# 
# 一些说明:
# 1. \_i: 子生成器, 同时也是迭代器
# 2. \_y: 子生成器 yield的值
# 3. \_r: yield from 表达式的最终值
# 4. \_s: 调用者通过send 发送的值
# 5. \_e: 异常对象

# In[23]:


#这个函数模拟了委托生成器内部的 yield from语句
def do_not_run():
    
    # EXPR 是可迭代对象, _i 是子生成器
    _i = iter(EXPR) 
    try:
        #激活子生成器并且把子生成器
        #第一个产出的值存储在_y中
        _y = next(_i) 
    except StopIteration as _e:
        #如果抛出了 StopIteration 异常,
        #那么将异常的值储存在 _r中
        _r = _e.value
    else:
        #子生成器进入循环
        #委托生成器阻塞
        while True:
            #将子生成器的第一个值 _y发送给调用者并且
            #等待调用者传递 _s给委托生成器
            _s = yield _y
            try:
                #委托生成器将_s转发给子生成器_i
                #并且接受子生成器生成的值 _y
                _y = _i.send(_s)
            except StopIteration as _e:
                #获取异常
                _r = _e.value
                break
    
    #_r是整个 yield from 表达式的返回值
    RESULT = _r


# 上面的代码只是简化了 yield from 的流程, 我们还需要考虑更多的边界情况:
# 
# 1. 子生成器可能只是一个迭代器, 而不是生成器函数, 所以不支持throw和send方法
# 2. 子生成器是生成器函数, 但是在调用子生成器的 throw 和 close 方法都会抛出异常
# 3. 调用者让子生成器自己抛出异常
# 4. 当调方使用next或者send时, 都要在子生成器上调用next函数; 当调用方使用send发送非 None值时, 才会调用子生成器的 send 方法.

# In[ ]:


import sys
def do_not_fucking_run():
    _i = iter(EXPR)
    try:
        _y = next(_i)
    except StopIteration as _e:
        _r = _e.value
    else:
        while True:
            try:
                _s = yield _y
            ##调用者可能会终止委托生成器
            ##此时如果_i是生成器需要调用_i 的close方法
            except GeneratorExit as _e:
                try:
                    _m = _i.close
                except AttributeError:
                    pass
                else:
                    _m()
                finally:
                    raise _e
            ## 委托生成器也可能捕获到其它异常
            ## 此时如果_i是生成器需要调用_i的throw
            ## 方法抛入这个异常;如果_i不是生成器
            ## 就直接raise这个异常
            except BaseException as _e:
                _x = sys.exc_info()
                try:
                    _m = _i.throw
                except AttributeError:
                    raise _e
                else:
                    try:
                        _y = _m(*_x)
                    except StopIteration as _e:
                        _r = _e.value
                        break
            ##如果成功yield了_i产生的第一个值
            ##并且成功接收到调用者发送来的值
            ##那么调用子生成器的next或者send方法
            ##需要捕捉子生成器的StopIteration异常
            else:
                try:
                    if _s is None:
                        _y = next(_i)
                    else:
                        _y = _i.send(_s)
                except StopIteration as _e:
                    _r = _e.value
                    break
    RESULT = _r       


# <center>总结</center>
# 
# 1. 子生成器退出时在 return处会抛出StopIteration异常
# 2. yield from表达式的值, 是子生成器终止时传递给子生成器的**SopIteration异常的第一个参数**
# 3. 如果子生成器抛出StopIteration异常, 委托生成器会停止阻塞(while循环终止),同时StopIteration异常会"冒泡"上传
# 4. 传入委托生成器的异常除了GeneratorExit外, 都会调用子生成器的throw方法传入子生成器
# 5. 如果调用委托生成器的close方法 或者传入GeneratorExit异常, 会调用子生成器的close方法
# 6. 4和5中调用子生成器的的throw和close方法时如果子生成器抛出StopIteration异常, 那么委托生成器停止阻塞, 异常向上"冒泡"

# ### 进程池

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

