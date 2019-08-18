#!/usr/bin/env python
# coding: utf-8

# In[9]:


class State(object):
    """定义了单个状态的基类
    """

    def run(self):
        raise NotImplementedError

    def next(self):
        raise NotImplementedError


class StateMachine(object):
    """状态机模板类
    """

    def __init__(self, init_state:State):
        
        self.current_state = init_state
        self.current_state.run()

    def runAll(self, input_states:[State]):
        """Template method:
        """
        for input_state in input_states:
            print(input_state)
            self.current_state = self.current_state.next(input_state)
            self.current_state.run()


# In[3]:


class MouseAction(object):
    """定义了🐀动作的类
    """

    def __init__(self, action:str):
        self.action = action

    def __str__(self):
        return self.action

    def __eq__(self, other):
        return self.action == other.action

    def __hash__(self):
        return hash(self.action)


# Static fields; an enumeration of instances:
MouseAction.appears = MouseAction('mouse appears')
MouseAction.runsAway = MouseAction('mouse runs away')
MouseAction.enters = MouseAction('mouse enters trap')
MouseAction.escapes = MouseAction('mouse escapes')
MouseAction.trapped = MouseAction('mouse trapped')
MouseAction.removed = MouseAction('mouse removed')


# 测试抓🐭

# In[4]:


# Waiting, Luring, Trapping 和 Holding 定义了 陷阱的状态,
# 它们都是 State 的子类
# 它和 MouseAction 的实例交互
class Waiting(State):
    """等待🐀
    """

    def run(self):
        print('Waiting: Broadcasting cheese smell.')

    def next(self, input_state):
#         print('The input state is: ', str(input_state))
        if input_state == MouseAction.appears:
            return MouseTrap.luring
        else:
            return MouseTrap.waiting


class Luring(State):
    """诱惑🐀
    """

    def run(self):
        print('Luring: Presenting cheese, door open.')

    def next(self, input_state):
        if input_state == MouseAction.runsAway:
            return MouseTrap.waiting
        elif input_state == MouseAction.enters:
            return MouseTrap.trapping
        else:
            return MouseTrap.luring


class Trapping(State):
    """抓捕🐀
    """

    def run(self):
        print('Trapping: Closing door.')

    def next(self, input_state):
        if input_state == MouseAction.escapes:
            return MouseTrap.waiting
        elif input_state == MouseAction.trapped:
            return MouseTrap.holding
        else:
            return MouseTrap.trapping


class Holding(State):
    """抓到🐀了!!!!!
    """
    def run(self):
        print('Holding: Mouse caught.')

    def next(self, input_state):
        if input_state == MouseAction.removed:
            return MouseTrap.waiting
        else:
            return MouseTrap.holding



# In[5]:


class MouseTrap(StateMachine):
    """捕鼠器类是 StateMachine 的子类
    """
    def __init__(self):
        """初始化捕鼠夹状态
        """
        super().__init__(init_state=MouseTrap.waiting)

# Static variable initialization
MouseTrap.waiting = Waiting()
MouseTrap.luring = Luring()
MouseTrap.trapping = Trapping()
MouseTrap.holding = Holding()


# In[6]:


import string
moves = []
with open('MouseMoves.txt') as f:
    for line in f.readlines():
        moves.append(line.split('\n')[0])


# In[8]:


MouseTrap().runAll(map(MouseAction, moves))


# 一些改进
# 
# 通过惰性初始化, 移除了 cyclic initialization dependencies.
# 
# 定义 MouseAction --> 定义 Waiting/Luring/Trapping/Holding --> 定义 MouseTrap

# In[10]:


class StateT(State):
    """状态机的节点类, 每个节点代表了陷阱的状态
    输入: 老鼠的状态
    输出: 陷阱的状态
    """
    def __init__(self):
        self.transitions = None

    def next(self, input_state):
        if input_state in self.transitions:
            return self.transitions[input_state]
        else:
            raise KeyError('Input not supported'
                           'for current state')


class Waiting(StateT):
    def run(self):
        print("Waiting: Broadcasting cheese smell")

    def next(self, input_state):
        """Lazy initialization
        """
        if self.transitions is None:
            self.transitions = {
                MouseAction.appears: MouseTrap.luring
            }
        return super().next(input_state)


class Luring(StateT):
    def run(self):
        print("Luring: Presenting Cheese, door open")

    def next(self, input_state):
        """Lazy initialization
        """
        if self.transitions is None:
            self.transitions = {
                MouseAction.enters: MouseTrap.trapping,
                MouseAction.runsAway: MouseTrap.waiting
            }
        return super().next(input_state)


class Trapping(StateT):
    def run(self):
        print("Trapping: Closing door")

    def next(self, input):
        # Lazy initialization:
        if not self.transitions:
            self.transitions = {
                MouseAction.escapes: MouseTrap.waiting,
                MouseAction.trapped: MouseTrap.holding
            }
        return super().next(input_state)


class Holding(StateT):
    def run(self):
        print("Holding: Mouse caught")

    def next(self, input):
        # Lazy initialization:
        if not self.transitions:
            self.transitions = {
                MouseAction.removed: MouseTrap.waiting
            }
        return super().next(input_state)


class MouseTrap(StateMachine):
    """捕鼠器类是 StateMachine 的子类
    """

    def __init__(self):
        """初始化捕鼠夹状态
        """
        super().__init__(init_state=MouseTrap.waiting)


# Static variable initialization
MouseTrap.waiting = Waiting()
MouseTrap.luring = Luring()
MouseTrap.trapping = Trapping()
MouseTrap.holding = Holding()


# ###### Table-Driven State Machine

# In[11]:


class State(object):
    """状态机的节点
    """
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str(self.name)


class Input(object):
    """每个节点的接受的状态
    """
    pass


class Condition(object):
    """判断是否状态转移的类
    """
    def condition(self, input_class):
        raise NotImplementedError


class Transition(object):
    """执行状态转移动作的类
    """
    def transition(self, input_class):
        raise NotImplementedError


# <center>Table</center>
# 
# ```python
# {
# (CurrentState, InputA) : (ConditionA, TransitionA, NextA), 
# (CurrentState, InputB) : (ConditionB, TransitionB, NextB), 
# (CurrentState, InputC) : (ConditionC, TransitionC, NextC)
# }
# ```

# In[12]:


class StateMachine(object):
    """A table-driven state machine
    """
    def __init__(self, init_state:State, tranTable):
        self.state = init_state
        self.transition_table = tranTable
    
    
    def next(self, input_state):
        pass


# In[ ]:




