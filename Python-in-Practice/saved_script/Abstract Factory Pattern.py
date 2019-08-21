#!/usr/bin/env python
# coding: utf-8

# ###### 抽象工厂 一个简单的例子

# In[ ]:





# #### 抽象工厂
# 
# 1. 用来生成复杂的对象
# 2. 所生成的对象由其他对象"组装"
# 3. 用来组装的对象全部来自同一个"家族"

# In[19]:


def create_diagram(factory):
    """接受一个 `对话框工厂类` 然后生成对话框
    """
    diagram = factory.make_diagram(30, 7)
    rectangle = factory.make_rectangle(4, 1, 22, 5, 'yellow')
    text = factory.make_text(7, 3, 'Abstract Factory')
    diagram.add(rectangle)
    diagram.add(text)
    return diagram  


# In[20]:


class DiagramFactory(object):
    """用于生成对话框的抽象工厂类, 它主要:
    1. 作为基类, 提供了接口
    2. 它本身也是一个具体的类
    """

    def make_diagram(self, width, height):
        return Diagram(width, height)

    def make_rectangle(self, x, y, width, height,
                       fill='white', stroke='black'):
        return Rectangle(x, y, width, height, fill, stroke)

    def make_text(self, x, y, text, fontsize=12):
        return Text(x, y, text, fontsize)


# In[21]:


class SvgDiagramFactory(DiagramFactory):
    """Svg对话框抽象工厂提供了和父类一样的接口但是返回的值不同
    """
    
    def make_diagram(self, width, height):
        return SvgDiagram(width, height)

    def make_rectangle(self, x, y, width, height,
                       fill='white', stroke='black'):
        return SvgRectangle(x, y, width, height, fill, stroke)

    def make_text(self, x, y, text, fontsize=12):
        return SvgText(x, y, text, fontsize)


# In[22]:


BLANK = " "
CORNER = "+"
HORIZONTAL = "-"
VERTICAL = "|"


# In[27]:


def _create_rectangle(width, height, fill=BLANK):
   """首先生成一个由空串组成的矩阵然后依次填入元素
   """
   #产生空字符串框
   rows = [[fill for _ in range(width)] for _ in range(height)]
   #在每一列的首尾填充
   for x in range(1, width - 1):
       rows[0][x] = HORIZONTAL
       rows[height - 1][x] = HORIZONTAL
   #在没一行的收尾填充
   for y in range(1, height - 1):
       rows[y][0] = VERTICAL
       rows[y][width - 1] = VERTICAL
   #在四个角填充
   for y, x in ((0, 0), (0, width - 1), 
                (height - 1, 0), (height - 1, width - 1)):
       rows[y][x] = CORNER
   return rows

#下面实现 对话框抽象工厂类生产的三个组件:对话框, 文本, 矩形
class Diagram(object):
   
   def __init__(self, width, height):
       self.width = width
       self.height = height
       self.diagram  = _create_rectangle(self.width, self.height)
   
   #add方法完成零件的组装
   def add(self, component):
       """为对话框加入组件, 这组件同样由对话框抽象工厂类生成
       """
       for y, row in enumerate(component.rows):
           for x, char in enumerate(row):
               self.diagram[y+component.y][x+component.x] = char
       return
   def save(self, filenameOrFile):
       """将对话框类保存到文件.
       如果参数是字符串, 就用它为名字新建文件; 如果参数是一个文件的句柄就直接写入.
       写入文件时,将每一行(一个字符串列表)合并为一个字符串写入
       """
       file = None if isinstance(filenameOrFile, str) else filenameOrFile
       try:
           if file is None:
               file = open(filenameOrFile, 'w', encoding='utf-8')
           for row in self.diagram:
               print(''.join(row), file=file)
       finally:
           #当 filenameOrFile是字符串时并且文件成功创建时, 需要在函数里
           #关闭它
           if isinstance(filenameOrFile, str) and file is not None:
               file.close()
       return

class Rectangle(object):
   
   def __init__(self, x, y, width, height, fill, stroke):
       self.x = x
       self.y = y
       self.rows = _create_rectangle(width, height, 
                                     BLANK if fill == 'white' else '%')
class Text(object):
   
   def __init__(self, x, y, text, fontsize):
       self.x = x
       self.y = y
       self.rows = [list(text)]


# In[28]:


SVG_START = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"
    "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">
<svg xmlns="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve"
    width="{pxwidth}px" height="{pxheight}px">"""

SVG_END = "</svg>\n"

SVG_RECTANGLE = """<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="{fill}" stroke="{stroke}"/>"""

SVG_TEXT = """<text x="{x}" y="{y}" text-anchor="left" font-family="sans-serif" font-size="{fontsize}">{text}</text>"""

SVG_SCALE = 20


# In[29]:


#下面实现Svg对话框
class SvgDiagram(object):
    
    def __init__(self, width, height):
        pxwidth = width * SVG_SCALE
        pxheight = width * SVG_SCALE
        self.diagram = [SVG_START.format(**locals())]
        outline = SvgRectangle(0, 0, width, height,
                               'lightgreen', 'black')
        self.diagram.append(outline.svg)
    
    def add(self, component):
        self.diagram.append(component.svg)
        return
    
    def save(self, filenameOrFile):
        file = None if isinstance(filenameOrFile, str) else filenameOrFile
        try:
            if file is None:
                file = open(filenameOrFile, "w", encoding="utf-8")
            file.write("\n".join(self.diagram))
            file.write("\n" + SVG_END)
        finally:
            if isinstance(filenameOrFile, str) and file is not None:
                file.close()
        return

class SvgRectangle(object):
    
    def __init__(self, x, y, width, height, 
                 fill, stroke):
        x *= SVG_SCALE
        y *= SVG_SCALE
        width *= SVG_SCALE
        height *= SVG_SCALE
        self.svg = SVG_RECTANGLE.format(**locals())

class SvgText(object):
    
    def __init__(self, x, y, text, fontsize):
        x *= SVG_SCALE
        y *= SVG_SCALE
        fontsize *= SVG_SCALE // 10
        self.svg = SVG_TEXT.format(**locals())
    


# <center>抽象工厂类的流程</center>
# 
# 1. {Diagram, Rectangle, Text}--->DiagramFactory--->make_diagram
# 2. {SvgDiagram, SvgRectangle, SvgText}--->SvgDiagramFactory--->make_diagram
# 3. {Diagram, Rectangle, Text} 与 {SvgDiagram, SvgRectangle, SvgText}是两类不同的零件, 可以看到实现方式是不同的, 因而无法混用！！！其中Diagram与SvgDiagram实现了同样的接口, 这是因为make_diagram里要调用他们分别实现对话框的组装和保存
# 4. DiagramFactory和SvgDiagramFactory只负责*生产全部零件*, 拼装过程放在make_diagram函数里, 因而这俩抽象工厂也要实现完全相同的接口.
# 5. make_diagram 函数接受一个抽象工厂类, 用它生成配件再把配件拼装起来(调用add方法)

# In[1]:


# import os
# import tempfile

# textFilename = os.path.join("diagram.txt")
# txtDiagram = create_diagram(DiagramFactory())
# txtDiagram.save(textFilename)

# svgFilename = os.path.join("diagram.svg")
# svgDiagram = create_diagram(SvgDiagramFactory())
# svgDiagram.save(svgFilename)


# ###### 改进: 更加pythonic的抽象工厂类
# 上面实现的缺点:
# 
# 1. 工厂类是纯虚的, 它们没有自己的state--我们无需用到它们的实例化!!!
# 2. SvgDiagramFactory与它的父类实现几乎一样, 除了返回值不同--代码复用性差!!!
# 3. 我们的命名空间里包含了从零件到工厂的所有的class: : DiagramFactory, Diagram, Rectangle, Text, etc.但是我们实际上只需要访问两个工厂类. 我们需要注意命名冲突问题,
# 这其实是不必要的.

# In[2]:


class DiagramFactory(object):
    
    #类变量
    BLANK = " "
    CORNER = "+"
    HORIZONTAL = "-"
    VERTICAL = "|"
    
    #私有函数
    def _create_rectangle(width, height, fill):
        rows = [[fill for _ in range(width)] for _ in range(height)]
        for x in range(1, width - 1):
            rows[0][x] = DiagramFactory.HORIZONTAL
            rows[height - 1][x] = DiagramFactory.HORIZONTAL
        for y in range(1, height - 1):
            rows[y][0] = DiagramFactory.VERTICAL
            rows[y][width - 1] = DiagramFactory.VERTICAL
        for y, x in ((0, 0), (0, width - 1), (height - 1, 0),
                (height - 1, width -1)):
            rows[y][x] = DiagramFactory.CORNER
        return rows    
    
    #类方法用于实例化
    @classmethod
    def make_diagram(cls, width, height):
        return cls.Diagram(width, height)
    
    @classmethod
    def make_rectangle(cls, x, y, width, height, 
                       fill='white', stroke='black'):
        return cls.Rectangle(x, y, width, height, fill, stroke)
    
    @classmethod
    def make_text(cls, x, y, text, fontsize=12):
        return cls.Text(x, y, text, fontsize)
    
    #将三个部件类嵌套在抽象工厂类里
    class Diagram:

        def __init__(self, width, height):
            self.width = width
            self.height = height
            self.diagram = DiagramFactory._create_rectangle(self.width,
                    self.height, DiagramFactory.BLANK)


        def add(self, component):
            for y, row in enumerate(component.rows):
                for x, char in enumerate(row):
                    self.diagram[y + component.y][x + component.x] = char


        def save(self, filenameOrFile):
            file = (None if isinstance(filenameOrFile, str) else
                    filenameOrFile)
            try:
                if file is None:
                    file = open(filenameOrFile, "w", encoding="utf-8")
                for row in self.diagram:
                    print("".join(row), file=file)
            finally:
                if isinstance(filenameOrFile, str) and file is not None:
                    file.close()


    class Rectangle:

        def __init__(self, x, y, width, height, fill, stroke):
            self.x = x
            self.y = y
            self.rows = DiagramFactory._create_rectangle(width, height,
                    DiagramFactory.BLANK if fill == "white" else "%")


    class Text:

        def __init__(self, x, y, text, fontsize):
            self.x = x
            self.y = y
            self.rows = [list(text)]
    


# In[ ]:


class SvgDiagramFactory(DiagramFactory):
    # 我们无须再写工厂方法了直接调用基类的即可
    SVG_START = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 20010904//EN"
    "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">
<svg xmlns="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink" xml:space="preserve"
    width="{pxwidth}px" height="{pxheight}px">"""

    SVG_END = "</svg>\n"

    SVG_RECTANGLE = """<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="{fill}" stroke="{stroke}"/>"""

    SVG_TEXT = """<text x="{x}" y="{y}" text-anchor="left" font-family="sans-serif" font-size="{fontsize}">{text}</text>"""

    SVG_SCALE = 20
    
    # 这样无需担心部件的名字冲突问题了
    class Diagram:

        def __init__(self, width, height):
            pxwidth = width * SvgDiagramFactory.SVG_SCALE
            pxheight = height * SvgDiagramFactory.SVG_SCALE
            self.diagram = [SvgDiagramFactory.SVG_START.format(**locals())]
            outline = SvgDiagramFactory.Rectangle(0, 0, width, height,
                    "lightgreen", "black")
            self.diagram.append(outline.svg)


        def add(self, component):
            self.diagram.append(component.svg)


        def save(self, filenameOrFile):
            file = (None if isinstance(filenameOrFile, str) else
                    filenameOrFile)
            try:
                if file is None:
                    file = open(filenameOrFile, "w", encoding="utf-8")
                file.write("\n".join(self.diagram))
                file.write("\n" + SvgDiagramFactory.SVG_END)
            finally:
                if isinstance(filenameOrFile, str) and file is not None:
                    file.close()


    class Rectangle:

        def __init__(self, x, y, width, height, fill, stroke):
            x *= SvgDiagramFactory.SVG_SCALE
            y *= SvgDiagramFactory.SVG_SCALE
            width *= SvgDiagramFactory.SVG_SCALE
            height *= SvgDiagramFactory.SVG_SCALE
            self.svg = SvgDiagramFactory.SVG_RECTANGLE.format(**locals())


    class Text:

        def __init__(self, x, y, text, fontsize):
            x *= SvgDiagramFactory.SVG_SCALE
            y *= SvgDiagramFactory.SVG_SCALE
            fontsize *= SvgDiagramFactory.SVG_SCALE // 10
            self.svg = SvgDiagramFactory.SVG_TEXT.format(**locals())


# <center>总结</center>
# 抽象工厂类**无需实例化**, 它包含:
# 
# 1. 生成零件的类方法
# 2. 内部嵌套定义的零件类
# 3. 其他类属性和私有函数
# 
# 除此之外, 一个额外的函数接受一个抽象工厂类 object, 然后调用抽象工厂类的零件生成的函数生成零件, 最后完成零件的拼装, 返回拼装后的产品

# In[ ]:




