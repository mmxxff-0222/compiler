#! /usr/bin/env python
#coding=utf-8
class node:

    def __init__(self, data):
        self._data = data       # 对应的终结符或非终结符
        self._children = []     # 子树结点
        self._value=None        # 针对终结符设计的属性，表示具体数值
        self.slice_variable = None
        self.slice_index = None

        # 针对 exp3 设计的属性
        self._place = None
        self._true = None
        self._false = None
        self._next = None
        self._begin = None

        self._flag = 0
 
    def getdata(self):
        return self._data

    def setvalue(self,value):
        self._value=value

    def getvalue(self):
        return self._value
    
    def getchild(self,i):
        return self._children[i]
 
    def getchildren(self):
        return self._children


    def setplace(self, place):
        self._place = place

    def getplace(self):
        return self._place

    def settrue(self, true):
        self._true = true

    def gettrue(self):
        return self._true

    def setfalse(self, false):
        self._false = false

    def getfalse(self):
        return self._false

    def setnext(self, next):
        self._next = next

    def getnext(self):
        return self._next

    def setbegin(self,begin):
        self._begin = begin

    def getbegin(self):
        return self._begin

    def add(self, node):
        self._children.append(node)
 
    def print_node(self, prefix):
        print('  '*prefix,'-',self._data)
        for child in self._children:
            child.print_node(prefix+1)
    
    def __str__(self):
        return "<Node: {}-{}>".format(self._data, self._value)
    
    def __repr__(self):
        return self.__str__()

            
def num_node(data):
    t=node(data)
    t.setvalue(int(data))
    return t
def float_node(data):
    t = node(data)
    t.setvalue(float(data))
    return t