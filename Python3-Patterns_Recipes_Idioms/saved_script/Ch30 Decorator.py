#!/usr/bin/env python
# coding: utf-8

# The use of layered objects to dynamically and transparently add responsibilities to individual objects is referred to as the decorator pattern.

# In[10]:


# 一个咖啡店的例子


class DrinkComponent(object):
    """所有饮品的基类
    """
    _cost = 0
    @property
    def Description(self):
        return self.__class__.__name__

    @property
    def Cost(self):
        return self.__class__._cost


class Decorator(DrinkComponent):
    """我们没有用 python 的 @decorator 特性
    decortor 为 基类的两个属性添加了额外的操作,
    也因此他必须和DrinkCompont提供相同的接口
    """

    def __init__(self, drinkComponent):
        """

        Parameters
        ----------
        drinkComponent: 一个 DrinkCompont的子类的实例
        """
        self.drink = drinkComponent

    @property
    def Cost(self):
        return self.drink.Cost + super().Cost

    @property
    def Description(self):
        return super().Description +            ' : ' + self.drink.Description

#下面的 class 继承了 DrinkComponent

class Espresso(DrinkComponent):
    _cost = .75

class EspressoConPanna(DrinkComponent):
    _cost = 1.

class Cappuccino(DrinkComponent):
    _cost = 1.

class CafeLatte(DrinkComponent):
    _cost = 1.

class CafeMocha(DrinkComponent):
    _cost = 1.25

# 有的咖啡较上面的复杂, 比如加了牛奶的拿铁(我自己编的)
# 他们继承的是 Decorator
class Milked(Decorator):
    _cost = 1.0


# In[11]:


#现在我们需要加牛奶的拿铁
#如果不用Python装饰器而要用上面的定义
#我们就要在CafeLatte上面封装一层
MilkedLatte = Milked(CafeLatte())


# In[13]:


print(MilkedLatte.Description)
print(MilkedLatte.Cost)


# In[ ]:




