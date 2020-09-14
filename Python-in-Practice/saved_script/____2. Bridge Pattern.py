#!/usr/bin/env python
# coding: utf-8

# <h1>Table of Contents<span class="tocSkip"></span></h1>
# <div class="toc"><ul class="toc-item"><li><span><a href="#Bridge-Pattern" data-toc-modified-id="Bridge-Pattern-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Bridge Pattern</a></span></li></ul></div>

# #### Bridge Pattern
# The Bridge Pattern is used in situations where we want to separate an abstraction from how it is implemented.
# 
# With the Bridge Pattern the approach is to create two independent class hierarchies:the “abstract” one defining the operations, 
# and the concrete one providing the implementations that the abstract operations will ultimately call.
# 
# The “abstract” class aggregates an instance of one of the concrete implementa- tion classes—and this instance serves as a bridge between the abstract interface and the concrete operations.

# In[1]:


class BarCharter(object):
    
    def __init__(self, renderer):
        
        if not isinstance(renderer, BarRenderer):
            raise TypeError(f'Expceted object of type BarRenderer, got {type(rednerer).__name__}.')
        self.__renderer = renderer
    
    def render(self, caption, pairs):
        """Implements a bar chart drawing algorithm,
        depending on the rednerer implementation
        """
        maximum = max(value for _, value in pairs)
        self.__renderer.initialize(len(pairs), maximum)
        self.__renderer.draw_caption(caption)
        for name, value in pairs:
            self.__renderer.draw_bar(name, value)
        self.__renderer.finalize()


# 下面实现 BarRednerer 抽象类 以及 \_\_subclasshook\_\_

# In[2]:


import collections
import abc

def has_methods(*methods):
    def decorator(cls):
        def __subclasshook__(Class, Subclass):

            if Class is cls:
                attributes = collections.ChainMap(*(cls_.__dict__ 
                                         for cls_ in Subclass.__mro__))
                if all(method in attributes for method in methods):
                    return True
                else:
                    return False
            return NotImplemented
        cls.__subclasshook__ = classmethod(__subclasshook__)
        return cls
    return decorator

@has_methods('initialize', 'draw_caption', 'draw_bar', 'finalize')
class BarRenderer(metaclass=abc.ABCMeta):
    pass


# 下面实现两种不同的Renderer

# In[3]:


class TextBarRenderer(object):
    
    def __init__(self, scaleFactor=40):
        
        self.scaleFactor = scaleFactor
    
    def initialize(self, bars, maximum):
        
        assert bars > 0 and maximum > 0
        self.scale = self.scaleFactor / maximum
    
    def draw_caption(self, caption):
        
        print('{0:^{2}}\n{1:^{2}}'
              .format(caption, "=" * len(caption), self.scaleFactor))
    
    def draw_bar(self, name, value):
        
        print('{} {}'.format('*' * int(value * self.scale), name))
    
    def finalize(self):
        
        pass


# In[4]:


pairs = (("Mon", 16), ("Tue", 17), ("Wed", 19), 
         ("Thu", 22),("Fri", 24), ("Sat", 21), 
         ("Sun", 19))

textBarCharter = BarCharter(TextBarRenderer())
textBarCharter.render('Forecast 6/8', pairs)


# In[7]:


class ImageBarRenderer(object):
    pass

