# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 16:32:55 2017

@author: pmgoa
"""
from utils.Tlist import Tlist
from utils.Slate import Slatefile, SLatefilenew, Slatefileclose, Slate, scribe, scribeln, comment, \
                        wordinline, IsNumber, IsText, list2str, type2str
from utils.reporter import Reporter 
from reseau.contract import Contract 

class history(Tlist):
    def __init__(self,MaterialName,sys):
       
       self.name=MaterialName
       self.sys=sys
       self.value=[]
       self.period=[]
       self.quantity=[]
       self.Reporter=Reporter('a', self.name) 

       
       
    def collate(self,period):
        self.period.append(period)
        self.value.append(0)
        self.quantity.append(0)
        for agent in self.sys.sellers:
            for transactions in agent.trades:
                if isinstance(transactions, Contract):
                    if transactions.material==self.name  and transactions.expired and transactions.period==period:
                        self.value[-1]=self.value[-1]+transactions.value
                        self.quantity[-1]=self.quantity[-1]+transactions.quantity
                else:
                
                    if transactions.material==self.name  and transactions.executed and transactions.period==period:
                        self.value[-1]=self.value[-1]+transactions.value
                        self.quantity[-1]=self.quantity[-1]+transactions.quantity
            
        vdum=0
        qdum=1
        #Nperiods=len(self.period)
        #for i in range(len(self.period) - Nperiods,len(self.period)):
        vdum=vdum+self.value[-1]
        qdum=qdum+self.quantity[-1]
       
        self.Reporter.scribe(self.name)
        self.Reporter.scribe(vdum/qdum)
        self.Reporter.scribe(vdum)
        self.Reporter.scribeln(qdum)
                
    def averagePrice(self,Nperiods):
        vdum=0
        qdum=1
        Nperiods=min(Nperiods,len(self.period)) 
        for i in range(1,Nperiods):
           vdum=vdum+self.value[-i]
           qdum=qdum+self.quantity[-i]
        Nperiods +=1   
        return vdum/qdum, qdum/Nperiods
        
          # sys.histories[0].averagePrice(1), to access history data    



               
                    
class Histories(Tlist):
    def __init__(self,sys):
        super(Tlist,self).__init__(name='Histories')
        self.sys = sys
        for agent in sys.sellers:
            for i in range(len(agent.product)):                      
                ok,h= self.findname(agent.product[i])
                if not ok:
                    h=history(agent.product[i],self.sys)
                    self.add(h)
        
        self._collated = False
    
    def collateall(self):
        for h in self:
            h.collate(self.sys.count)
        
    
    @property    
    def collated(self):
        return self._collated

                    
    """def PriceAverage(self,material, Nperiods):  
        ok,h=self.findname(self.material)
        if not ok:
            return -1 
        else:
            return h.averagePrice(Nperiods)"""
            
    def PriceAverage(self,Nperiods):  
        for h in self:
            a= h.averagePrice(Nperiods)
            #h.Reporter.scribe(a)
            
            

            

    def writeheader(self):
        for h in self:
            h.Reporter.Writeheader()
    
        
    def report(self):            
        for h in self:            
            h.Reporter.Writeval()
    

