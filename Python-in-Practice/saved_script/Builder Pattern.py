#!/usr/bin/env python
# coding: utf-8

# ###### Builder 模式 一个简单例子

# 1. 对象需要多个部分组合来一步一步创建, 并且创建和表示分离
# 2. 比如你要买电脑, 工厂模式直接返回一个你需要型号的电脑, 构造模式允许你自定义电脑的各种配置类型

# In[3]:


# Factory Pattern
MINI14 = '1.4GHz Mac mini'


class AppleFactory(object):
    class MacMini14(object):
        def __init__(self):
            self.memory = 4  # GB
            self.hdd = 500  # GB
            self.gpu = 'Intel HD Graphics 5000'

        def __str__(self):
            info = (
                f'Model : {MINI14}',
                f'Memory : {self.memory} GB',
                f'Hard Disk : {self.hdd} GB',
                f'Graphics Card : {self.gpu}'
            )
            return '\n'.join(info)

    @classmethod
    def build_computer(cls, model_name):
        if model_name == MINI14:
            # 返回一个 MacMini14的实例
            return cls.MacMini14()
        else:
            print(f'I don\'t how to build {model_name}.')


def build_computer(product_name):
    if product_name == MINI14:
        return AppleFactory.build_computer(MINI14)


# In[5]:


print(build_computer(MINI14))


# In[6]:


# builder 模式


class Computer(object):
    """Product Class
    这个类表示了我们的电脑
    """

    def __init__(self, serial_number):
        self.serial = serial_number
        self.memory = None
        self.hdd = None
        self.gpu = None

    def __str__(self):
        info = (
            f'Serial Number : {self.serial}',
            f'Memory : {self.memory} GB',
            f'Hard Disk : {self.hdd} GB',
            f'Graphics Card : {self.gpu}'
        )
        return '\n'.join(info)


class ComputerBuilder(object):
    """配置 Computer 的类. 用户可以通过这个类
    来配置他需要的电脑.  创建过程在这个类中进行
    """
    def __init__(self, serial_number):
        self.computer = Computer(serial_number)

    def configure_memory(self, amount):
        self.computer.memory = amount

    def configure_hdd(self, amount):
        self.computer.hdd = amount

    def configure_gpu(self, gpu_model):
        self.computer.gpu = gpu_model


# In[17]:


class Customer(object):
    """在构造模式中, 创建和表示是分离的, 用户可以控制创建的
    过程(通过调用 builder)来完成他想要的产品
    """
    def __init__(self):
        self.builder = None
    
    def construct_computer(self, **kwargs):
        """用于通过这个接口来DIY它的电脑
        """
        self.builder = kwargs.get('builder', None)
        if self.builder is None:
            self.builder = ComputerBuilder('AG23385193')
            
        memory = kwargs.get('memory', 16)
        hdd = kwargs.get('hdd', 500)
        gpu = kwargs.get('gpu', 'Intel HD Graphics 5000')
        # 开始配置电脑
        self.builder.configure_memory(memory)
        self.builder.configure_hdd(hdd)
        self.builder.configure_gpu(gpu)
    
    @property
    def computer(self):
        return self.builder.computer
      


# In[21]:


customer = Customer()
customer.construct_computer(hdd=500, memory=16, 
                            gpu='GeForce GTX 750 Ti')
print(customer.computer)


# ##### 构造模式

# In[1]:


from abc import ABCMeta, abstractmethod
# 让metaclass为abc.ABCMeta可以保证基类无法被实例化


class AbstractFormBuilder(metaclass=ABCMeta):
    """所有继承该抽象基类的子类, 都必须实现下面的抽象方法.
    """

    @abstractmethod
    def add_title(self, title):
        self.title = title

    @abstractmethod
    def form(self):
        pass

    @abstractmethod
    def add_label(self, text, row, column, **kwargs):
        pass


# In[2]:


from html import escape
class HtmlFormBuilder(AbstractFormBuilder):
    def __init__(self):
        self.title = 'HtmlFormBuilder'
        self.items = {}
    
    def add_title(self, title):
        #需要用html.escape函数处理title
        super().add_title(escape(title))
    
    def add_label(self, text, row, column, **kwargs):
        self.items[(row, column)] = (
            '<td><label for="{}">{}:</label></td>'.
            format(kwargs['target'], escape(text))
        )
    def add_entry(self, variable, row, column, **kwargs):
        html =        """
        <td><input name="{}" type="{}" /></td>
        """.format(variable, kwargs.get('kind', 'text'))
        self.items[(row, column)] = html
    def add_button(self, text, row, column, **kwargs):
        html =        """
        <td><input type="submit" value="{}" /></td>
        """.format(escape(text))
        self.items[(row, column)] = html
    def form(self):
        html =        [
            '<!doctype html>\n<html><head><title>{}</title></head>'
            '<body>'.format(self.title), '<form><table border="0">'
        ]
        thisRow = None
        for key, value in sorted(self.items.items()):
            row, column = key
            if thisRow is None:
                html.append(' <tr>')
            elif thisRow != row:
                html.append(' </tr>\n <tr>')
            thisRow = row
            html.append('  ' + value)
        html.append(' </tr>\n</table></form></body></html>')
        return '\n'.join(html)


# In[ ]:


class TkFormBuilder(AbstractFormBuilder):
    def __init__(self):
        self.title = 'TKFormBuilder'
        self.statements = []
        
    def add_title(self, title):
        super().add_title(title)
    
    def add_label(self, text, row, column, **kwargs):
        name = self._canonicalize(text)
        create = f"""self.{name}Label=ttk.Label(self, text="{text}:")"""
        layout = f"""self.{name}Label.grid(row={row}, column={column},
        sticky=tk.W, padx="0.75m", pady="0.75m")"""
        self.statements.extend((create, layout))
        
    

