#!/usr/bin/env python
# coding: utf-8

# In[21]:


def foo():
    x = 3
    return x + 1
class Cat(object):
    """
    喵喵喵
    """
    def __init__(self, name = 'kitty'):
        self.name = name
    def Miao(self):
        print(self.name + ' : MiaoMiao\n')
cat = Cat()


# <table border="1"><thead><tr><th>Type</th>
# 			<th>Attribute</th>
# 			<th>Description</th>
# 			<th>Notes</th>
# 		</tr></thead><tbody><tr><td>module</td>
# 			<td>__doc__</td>
# 			<td>documentation string</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>__file__</td>
# 			<td>filename (missing for built-in modules)</td>
# 			<td> </td>
# 		</tr><tr><td>class</td>
# 			<td>__doc__</td>
# 			<td>documentation string</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>__module__</td>
# 			<td>name of module in which this class was defined</td>
# 			<td> </td>
# 		</tr><tr><td>method</td>
# 			<td>__doc__</td>
# 			<td>documentation string</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>__name__</td>
# 			<td>name with which this method was defined</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>im_class</td>
# 			<td>class object that asked for this method</td>
# 			<td>(1)</td>
# 		</tr><tr><td> </td>
# 			<td>im_func or __func__</td>
# 			<td>function object containing implementation of method</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>im_self or __self__</td>
# 			<td>instance to which this method is bound, or None</td>
# 			<td> </td>
# 		</tr><tr><td>function</td>
# 			<td>__doc__</td>
# 			<td>documentation string</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>__name__</td>
# 			<td>name with which this function was defined</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>func_code</td>
# 			<td>code object containing compiled function <a href="https://docs.python.org/release/2.7.2/glossary.html#term-bytecode" rel="nofollow">bytecode</a></td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>func_defaults</td>
# 			<td>tuple of any default values for arguments</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>func_doc</td>
# 			<td>(same as __doc__)</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>func_globals</td>
# 			<td>global namespace in which this function was defined</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>func_name</td>
# 			<td>(same as __name__)</td>
# 			<td> </td>
# 		</tr><tr><td>generator</td>
# 			<td>__iter__</td>
# 			<td>defined to support iteration over container</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>close</td>
# 			<td>raises new GeneratorExit exception inside the generator to terminate the iteration</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>gi_code</td>
# 			<td>code object</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>gi_frame</td>
# 			<td>frame object or possibly None once the generator has been exhausted</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>gi_running</td>
# 			<td>set to 1 when generator is executing, 0 otherwise</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>next</td>
# 			<td>return the next item from the container</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>send</td>
# 			<td>resumes the generator and “sends” a value that becomes the result of the current yield-expression</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>throw</td>
# 			<td>used to raise an exception inside the generator</td>
# 			<td> </td>
# 		</tr><tr><td>traceback</td>
# 			<td>tb_frame</td>
# 			<td>frame object at this level</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>tb_lasti</td>
# 			<td>index of last attempted instruction in bytecode</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>tb_lineno</td>
# 			<td>current line number in Python source code</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>tb_next</td>
# 			<td>next inner traceback object (called by this level)</td>
# 			<td> </td>
# 		</tr><tr><td>frame</td>
# 			<td>f_back</td>
# 			<td>next outer frame object (this frame’s caller)</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>f_builtins</td>
# 			<td>builtins namespace seen by this frame</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>f_code</td>
# 			<td>code object being executed in this frame</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>f_exc_traceback</td>
# 			<td>traceback if raised in this frame, or None</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>f_exc_type</td>
# 			<td>exception type if raised in this frame, or None</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>f_exc_value</td>
# 			<td>exception value if raised in this frame, or None</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>f_globals</td>
# 			<td>global namespace seen by this frame</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>f_lasti</td>
# 			<td>index of last attempted instruction in bytecode</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>f_lineno</td>
# 			<td>current line number in Python source code</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>f_locals</td>
# 			<td>local namespace seen by this frame</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>f_restricted</td>
# 			<td>0 or 1 if frame is in restricted execution mode</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>f_trace</td>
# 			<td>tracing function for this frame, or None</td>
# 			<td> </td>
# 		</tr><tr><td>code</td>
# 			<td>co_argcount</td>
# 			<td>number of arguments (not including * or ** args)</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>co_code</td>
# 			<td>string of raw compiled bytecode</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>co_consts</td>
# 			<td>tuple of constants used in the bytecode</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>co_filename</td>
# 			<td>name of file in which this code object was created</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>co_firstlineno</td>
# 			<td>number of first line in Python source code</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>co_flags</td>
# 			<td>bitmap: 1=optimized | 2=newlocals | 4=*arg |8=**arg</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>co_lnotab</td>
# 			<td>encoded mapping of line numbers to bytecode indices</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>co_name</td>
# 			<td>name with which this code object was defined</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>co_names</td>
# 			<td>tuple of names of local variables</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>co_nlocals</td>
# 			<td>number of local variables</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>co_stacksize</td>
# 			<td>virtual machine stack space required</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>co_varnames</td>
# 			<td>tuple of names of arguments and local variables</td>
# 			<td> </td>
# 		</tr><tr><td>builtin</td>
# 			<td>__doc__</td>
# 			<td>documentation string</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>__name__</td>
# 			<td>original name of this function or method</td>
# 			<td> </td>
# 		</tr><tr><td> </td>
# 			<td>__self__</td>
# 			<td>instance to which a method is bound, or None</td>
# 			<td> </td>
# 		</tr></tbody></table><p> </p>

# ###### 访问实例的元数据
# * \_\_dict__
# * \_\_class\_\_

# In[3]:


cat.__dict__


# In[27]:


cat.__class__


# ###### 访问模块的原数据
# * \_\_doc\_\_
# * \_\_name\_\_
# * \_\_file\_\_
# * \_\_dict\_\_

# In[4]:


import numpy as np


# In[6]:


print(np.__doc__.splitlines()[0:3])


# In[7]:


print(np.__name__)


# In[8]:


print(np.__file__)


# In[18]:


#返回这个模块的全部信息
print(np.__dict__['__name__'])
print(np.__dict__['__file__'])


# ###### 访问类的元数据
# * \_\_doc\_\_
# * \_\_name\_\_ **直接父类**对象的元组
# * \_\_module\_\_
# * \_\_bases\_\_
# * \_\_dict\_\_

# In[22]:


print(Cat.__doc__)


# In[23]:


print(Cat.__name__)


# In[24]:


print(Cat.__module__)


# In[25]:


print(Cat.__bases__)


# In[26]:


print(Cat.__dict__)


# ###### 访问内建函数和方法的元数据
# * \_\_doc\_\_
# * \_\_name\_\_
# * \_\_self\_\_ 仅方法可用，如果是绑定的(bound)，则指向调用该方法的类（如果是类方法）或实例（如果是实例方法），否则为None。
# * \_\_module\_\_

# In[28]:


import sys


# In[31]:


#用 sys的 builtin_modules_names字段查看所有的内建函数
print(sys.builtin_module_names[0])


# In[32]:


from functools import wraps


# In[35]:


print(wraps.__doc__)


# In[37]:


print(wraps.__name__)


# In[39]:


print(wraps.__module__)


# In[40]:


from collections import Iterable


# In[41]:


print(Iterable.mro.__self__)


# ###### 查看函数的元数据
# * \_\_doc\_\_
# * \_\_name\_\_
# * \_\_file\_\_
# * \_\_dict\_\_
# * \_\_defaults\_\_
# * \_\_code\_\_ 这个属性指向一个该函数对应的code对象，code对象中定义了其他的一些特殊属性
# * \_\_globals\_\_  这个属性指向当前的全局命名空间而不是定义函数时的全局命名空间
# * \_\_closure\_\_ 这个属性仅当函数是一个闭包时有效, 指向一个保存了所引用到的外部函数的变量cell的元组

# In[44]:


def func(a=3, b=4):
    return a + b


# In[47]:


print(func.__defaults__)


# In[51]:


print(func.__globals__['__builtins__'])


# In[53]:


print(func.__code__)


# In[58]:


def func(a = 3):
    def f():
        return a + 3
    return f    


# In[64]:


func().__closure__


# ###### 查看方法的元数据
# * \_\_doc\_\_
# * \_\_name\_\_ 
# * \_\_module\_\_
# * \_\_func\_\_ 使用这个属性可以拿到方法里实际的函数对象的引用
# * \_\_class\_\_ 如果是绑定的(bound)，则指向调用该方法的类（如果是类方法）或实例（如果是实例方法），否则为None
# * \_\_self\_\_

# In[65]:


method = cat.Miao


# In[66]:


print(method.__func__)


# In[67]:


print(method.__class__)


# In[69]:


print(method.__self__)


# ###### 查看生成器的元数据
# * \_\_class\_\_ 返回generator
# * \_\_iter\_\_
# * gi_code 生成器对应的code对象
# * gi_frame 生成器对应的frame对象
# * gi_running 生成器函数是否在执行。生成器函数在yield以后、执行yield的下一行代码前处于frozen状态，此时这个属性的值为0。

# In[70]:


g = (n for n in range(10))


# In[72]:


print(g.__class__)


# In[79]:


print(g.__iter__)


# In[82]:


print(g.gi_code)


# In[83]:


print(g.gi_frame)


# In[84]:


print(g.gi_running)


# ###### 查看代码块的元数据
# * co_argcount 通参数的总数，不包括\*参数和\*\*参数。
# * co_names 所有的参数名（包括\*参数和\*\*参数）和局部变量名的元组。
# * co_varnames 所有的局部变量名的元组。
# * co_filename 源代码所在的文件名。
# * co_flags  这是一个数值，每一个二进制位都包含了特定信息。较关注的是0b100(0x4)和0b1000(0x8)，如果co_flags & 0b100 != 0，说明使用了\*args参数；如果co_flags & 0b1000 != 0，说明使用了\*\*kwargs参数。另外，如果co_flags & 0b100000(0x20) != 0，则说明这是一个生成器函数(generator function)

# In[85]:


#获取函数的code对象
code = cat.Miao.__code__


# In[86]:


print(code.co_argcount)


# In[87]:


print(code.co_names)


# In[88]:


print(code.co_varnames)


# In[89]:


print(code.co_filename)


# In[90]:


print(code.co_flags)


# In[91]:


print(code.co_code)


# ###### 查看栈帧(frame)的元数据
# 栈帧表示程序运行时函数调用栈中的某一帧。函数没有属性可以获取它，因为它在函数调用时才会产生，而生成器则是由函数调用返回的，所以有属性指向栈帧。想要获得某个函数相关的栈帧，则<u>必须在调用这个函数且这个函数尚未返回时获取</u>。你可以使用sys模块的_getframe()函数、或inspect模块的currentframe()函数获取当前栈帧。这里列出来的属性全部是只读的。
# * f_back 调用栈的前一帧。
# * f_code 栈帧对应的code对象。
# * f_locals 用在当前栈帧时与内建函数locals()相同，但你可以先获取其他帧然后使用这个属性获取那个帧的locals()。
# * f_globals 用在当前栈帧时与内建函数globals()相同。

# In[100]:


from inspect import currentframe
def add(x, y = 1):
    f = currentframe()
    print(f.f_locals)
    print(f.f_back)
    a = x + y + 3
    print(f.f_locals)
    print(f.f_back)
    print(f.f_code)
    return a


# In[101]:


add(2)


# ###### 查看追踪(traceback)的元数据
# 追踪是在出现异常时用于回溯的对象，与栈帧相反。由于异常时才会构建，而异常未捕获时会一直向外层栈帧抛出，所以需要使用try才能见到这个对象。你可以使用sys模块的exc_info()函数获得它，这个函数返回一个元组，元素分别是异常类型、异常对象、追踪。traceback的属性全部是只读的。
# * tb_next: 追踪的下一个追踪对象。
# * tb_frame: 当前追踪对应的栈帧。
# * tb_lineno: 当前追踪的行号。

# In[1]:


import sys
def div(x, y):
    try:
        return x / y
    except:
        tb = sys.exc_info()
        print(tb)
        print(tb[2].tb_lineno)
        print(tb[2].tb_next)
        print(tb[2].tb_frame.f_locals)
        print(tb[2].tb_frame.f_back)


# In[2]:


div(1, 0)


# ##### 使用 inspect模块
# inspect模块主要提供了四种用途, 用于自省:
# 1. 对是否是模块, 框架, 函数等进行类型检查
# 2. 获取源码
# 3. 获取类或函数的参数信息
# 4. 解析堆栈

# ###### 查看对象类型
# * is{module|class|function|method|builtin}

# In[110]:


from inspect import isroutine
print(isroutine(cat.Miao))


# ###### 获取code信息
# 1. inspect.getdoc(object)： 获取object的documentation信息
# 
# 2. inspect.getcomments(object)
# 
# 3. inspect.getfile(object): 返回对象的文件名
# 
# 4. inspect.getmodule(object)：返回object所属的模块名
# 
# 5. inspect.getsourcefile(object)： 返回object的python源文件名；object不能使built-in的module, class, mothod
# 
# 6. inspect.getsourcelines(object)：返回object的python源文件代码的内容，行号+代码行
# 
# 7. inspect.getsource(object)：以string形式返回object的源代码

# In[111]:


from inspect import getsource
getsource(cat.Miao)


# In[112]:


from inspect import getmodule
getmodule(cat.Miao)


# ###### 获取类和函数的信息
# 1. inspect.getclasstree(classes[, unique])
# 
# 2. inspect.getargspec(func)
# 
# 3. inspect.getargvalues(frame)
# 
# 4. inspect.formatargspec(args[, varargs, varkw, defaults, formatarg, formatvarargs, formatvarkw, formatvalue, join])
# 
# 5. inspect.formatargvalues(args[, varargs, varkw, locals, formatarg, formatvarargs, formatvarkw, formatvalue, join])
# 
# 6. inspect.getmro(cls)： 元组形式返回cls类的基类（包括cls类），以method resolution顺序;通常cls类为元素的第一个元素
# 
# 7. inspect.getcallargs(func[, *args][, **kwds])：将args和kwds参数到绑定到为func的参数名；对bound方法，也绑定第一个参数（通常为self）到相应的实例；返回字典，对应参数名及其值

# In[115]:


from inspect import getclasstree
getclasstree([Cat])


# In[116]:


from inspect import getargspec
getargspec(Cat.Miao)


# In[118]:


from inspect import getargvalues
g = (i for i in range(10))
getargvalues(g.gi_frame)


# In[128]:


from inspect import formatargspec, getfullargspec
getfullargspec(Cat.Miao)


# In[134]:


#formatargspec(getfullargspec(Cat.Miao))


# ###### 获取堆栈的信息

# In[147]:


from inspect import stack
def func():
    print(stack()[1])
    print(stack()[1][0].f_locals['__name__'])
    return
    


# In[148]:


func()


# In[155]:


#获取堆栈信息 + 装饰器
def main(func):

    if stack()[1][0].f_locals['__name__'] == '__main__':
        # Discard the script name from command line.
        #args = sys.argv[1: ]
        # Call the main function
        func()
    return func


# In[156]:


@main
def f():
    print('haha')  


# In[ ]:




