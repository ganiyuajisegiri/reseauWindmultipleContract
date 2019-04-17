# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 16:09:52 2017

@author: pmgoa
"""
#from reseau import System as sys
from utils.Slate import Slatefile, SLatefilenew, Slatefileclose, Slate, scribe, scribeln, comment, \
                        wordinline, IsNumber, IsText, list2str, type2str
from utils.reporter import Reporter  
import numpy as np
import random


class BaseAgent:
    """This is the BaseAgent class where all other classes inherited from"""
    active = False     
    def __init__(self,sys,name):
        super(BaseAgent,self).__init__()
        self.sys = sys
        self.name = name  
        #store this cycle trade, and move to archive at the end
        self.trades=[]
        self.types=""
        self.tradesarchive=[]     
        self.money = 0
        self.contract=""
        self.duration=0
        
        #location
        self.X =0
        self.Y =0
        self.distance = 0
        self.trust=0   
        self.startperiod =0
          

        

        #reporting section, all self._Properties are reported
        self._include=["period","name","money"]
        self._exclude=[]
        self.Reporter=Reporter(self) 
        
    
    
    @property
    def period(self):
        return self.sys.count
    
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
        rtn=[self.name,self.money]
        return ", ".join(rtn)

        
    @property
    def money(self):
        return self._money

    @money.setter
    def money(self, value):
        if value >= 0:
            self._money = value
        else:
            #comment("Quantity below 0 is not possible; set to zero")
            self._money = 0

    @property
    def contract(self):
        return self._contract

    @contract.setter
    def contract(self, value):
        self._contract = value

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = value
        
    @property
    def xaxis(self):
        return self.X

    @xaxis.setter
    def xaxis(self, value):
        self._X = value

    @property
    def yaxis(self):
        return self._Y

    @yaxis.setter
    def yaxis(self, value):
        self._Y = value
        
        
    @property
    def startperiod(self):
        return self._startperiod    
    
    @startperiod.setter
    def startperiod(self, value):
        self._startperiod = value


    @property
    def Fitness(self):
        self.fitness = random.random()
        return self.fitness
        
    @property
    def location(self):
        self.pos= self.X,self.Y
        return self.pos
   
    def LoadParam(self,key,value):
        #factory name
        
        rtn=True
        if key.lower() == 'name':
            self.name= value
        elif key.lower() == 'xaxis':
            self.X =value
        elif key.lower() == 'yaxis':
            self.Y =value  
        elif key.lower() == 'types':
            self.types =value 
        else:
            rtn=False
            #comment("Data not recognised:", key,value)
    
        return rtn    
        

    def writeheader(self):
        self.Reporter.Writeheader()
        
    def Report(self):            
            
        self.Reporter.Writeval()

    @property
    def types(self):
        return self._types
    
    @types.setter
    def types(self, value):
        self._types= value

        

        

    def Final(self) :
        #report trades
        self.tradesarchive=self.tradesarchive+self.trades
        self.trades=[]


    def weibulcdf(self,x,n,a):
       return 1 - np.exp(-(x/n)**a)
    
    @property
    def hascontract(self):
        return self.contract
            
    
    def nocontract(self):
        if self.contract =='no':
            return True
    
    def contractactive(sef):
        pass

    def contractnotactive(sef):
        pass
        