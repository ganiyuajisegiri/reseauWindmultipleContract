# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 23:33:13 2017

@author: Ajisegiri Ganiyu
"""

class Material:
    def __init__(self,name=None):
        self.name = name
        
        
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name= str(value).strip()
        
    #object to string functions to allow the object to be printed!
    def __str__(self):
        return self._name
    def __repr__(self):
        rtn=[self.name]
        return ", ".join(rtn)
    
    
    def LoadParam(self,key,value):
        #factory name
        
        rtn=True
        if key.lower() == 'name':
            self.name= value
        elif key.lower() == 'xaxis':
            self.X =value
        elif key.lower() == 'yaxis':
            self.Y =value        
        else:
            rtn=False
            #comment("Data not recognised:", key,value)
    
        return rtn    
