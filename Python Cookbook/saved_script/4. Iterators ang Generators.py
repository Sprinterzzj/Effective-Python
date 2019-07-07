#!/usr/bin/env python
# coding: utf-8

# ###### 14. 展平嵌套序列

# In[ ]:


from collections import Iterable


def flatten(items, ignore_types=(str, bytes)):
    """递归展开嵌套的序列, 注意处理特殊类型 str 和 bytes
    """
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            yield from flatten(x)
        else:
            yield x


# 当然这里也可以显式地调用 flatten生成器函数而不用yield from
def flatten(items, ignore_types=(str, bytes)):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, ignore_types):
            for i in flatten(x):
                yield i
            else:
                yield x

