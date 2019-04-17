# -*- coding: utf-8 -*-
"""
Created on Wed Oct 11 18:13:27 2017

@author: preflm
"""



# base class for an object with a name and value that can be sorted on name
class FLMSort(object):
    _name=None
    _value=None
    _separator="."
    __bool__=True
    parent=None
    defaultvalue=-111

    def __init__(me,parent=None,name=None,value=None):
        if parent:me.parent=parent
        if name:me._name=name
        if value:me._value=value

    def owner(me,classname=None):
        if classname is None:
            return me.parent
        elif me.parent is None:
            return me #guarantees parent always returns OPA
        else:
            return me.parent.__Owner(classname)

    def __owner(me,classname=None):
        if isinstance(me, classname):
            return me
        elif me.parent is None:
            return me #guarantees parent always returns OPA
        else:
            return me.parent.__Owner(classname)

    @property 
    def name(me):
        if not me._name:
            return  type(me).__name__
        else:
            return me._name
    @name.setter 
    def name(me,name):
        me._name=name

    @property 
    def value(me):
        if me._value is None:
            return me.defaultvalue
        else:
            return me._value

    @value.setter 
    def value(me,value):
        me._value=value
    
    def __call__(me):
        #Returns a (worksheet,Success) by its name and index
        if me.value:
            return me.value
        else:
            return me.fullname

    @property 
    def fullname(me):
        if me.parent is None :
            return me._name
        else:
            return me.parent.fullname+me._separator+me.name

      
    def __str__(me):
        #called when print(obj)
        return me.name
    
    def __repr__(me):
        #called when print([obj])
        if me.value:
            return me.fullname+" (%s)" % me.value
        else:
            return me.fullname
    
    def __bool__(me):
        #this allows: if obj: return
        return me.name!="" or me.Value is not None
    
    def __eq__(me, other):
        if hasattr(other, "fullname"):
            return me.fullname.lower() == other.fullname.lower()
        elif hasattr(other, "name") :
            return me.name.lower() == other.name.lower()
        elif hasattr(other, "text") :
            return me.name.lower() == other.text.lower()
        else:
            return notImplemented
 
    def __lt__(me, other):
        if hasattr(other, "fullname") :
            return me.fullname.lower() < other.fullname.lower()
        elif hasattr(other, "name") :
            return me.name.lower() < other.name.lower()
        elif hasattr(other, "text") :
            return me.name.lower() < other.text.lower()
        else:
            return notImplemented
        
    def __gt__(me, other):
        if hasattr(other, "fullname") :
            return me.fullname.lower() > other.fullname.lower()
        elif hasattr(other, "name") :
            return me.name.lower() > other.name.lower()
        elif hasattr(other, "text") :
            return me.name.lower() > other.text.lower()
        else:
            return notImplemented

    def __le__(me, other):
        return me.__lt__(other) or me.__eq__(other)
     
    def __ge__(me, other):
        return me.__gt__(other) or me.__eq__(other)
     
    def __ne__(me, other):
        return not me.__eq__(other)

