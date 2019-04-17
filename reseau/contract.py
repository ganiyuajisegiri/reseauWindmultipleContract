    # -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 16:02:18 2017

@author: pmgoa
"""
import math
#from system import System as sy
from reseau.transaction import Transaction
from utils.Slate import comment,list2str

import numpy as np
import random
DEBUG = False

def find(L,name):
    return next((x for x in L if x.name.lower() == name.lower()), None)

class Contract:
    #def __init__(self,sys,buyer , seller,material,quantity, price,startperiod,endperiod):
    def __init__(self,Buyer,RM):
        #these var are recorded
        self._buyer  = Buyer
        self._seller  = None
        self.Seltmp=""
        self.startperiod=0
        self.endperiod =0
        self._material=RM
        self.contract_quantity=0
        
        #self._sellers  = [seller]
        self._FinalQ=-1
        self._FinalP=-1
        self._value=-1
        self.distance=0

        
        #these are not (no underscore at the start)
        self._executed=False
        
        #include and exclude
        self._exclude=["executed"]
        self._include=["period","buyer","seller","material","FinalQ","FinalP","value","distance"]
    
    @property
    def activated(self):

        if self._seller is None:
           self._seller=find(self._buyer.sys.winds,self.Seltmp)  
        if self._seller is None:
           self._seller=find(self._buyer.sys.sellers,self.Seltmp)
        return  self._seller 
        
    @property
    def period(self):
        return self._buyer.sys.count
    
    @property
    def buyer(self):
        return self._buyer
    
    @property
    def seller(self):
        return self._seller

    @property
    def material(self):
        return self._material
    
    @property 
    def IsValid(self):
        ok=False
        #for Prod in self._seller.product:            
        #print('aaa', Prod)
        if self._seller.product == self.material: #Prod == self.material:
            ok=True 
            #print('aaa',self.period, self.startperiod,self.endperiod)
        return ok and self.period>=self.startperiod and self.period<=self.endperiod
    
    @property
    def Execute(self):

        if  self.IsValid :
            self.contract_Q
            t=Transaction(self.seller,self.material,self.contract_quantity)
            t.execute(self.buyer,0.05)#t.execute(self.buyer,self.Price)
    
        #if not self.IsValid :
        #    return
        #t=Transaction(self.seller,self.material,self.contract_quantity)
        #t.execute(self.buyer,self.Price)
    @property
    def contract_Q(self):             
        self.contract_quantity=self._seller.prdQuantity   


    
    
    @property    
    def nodeal(self):
        for i in range(len(self._seller.product)):            
            if self.seller.product[i] == self.material:
                self.seller.prdQuantity[i] = 0
        return self.seller.prdQuantity[i]
    
    @property    
    def yesdeal(self):
        for i in range(len(self._seller.product)):            
            if self.seller.product[i] == self.material:
                return self.seller.prdQuantity[i]
            
    @property    
    def current(self):
        if self.period<=self.endperiod and self.period>=self.startperiod:
            return True
    @property    
    def expired(self):
        #return self._expired
        if self.period>self.endperiod:
            return True
    
    @property
    def executed(self):
        return self._executed

    @property    
    def quantity(self):                    
        if self.executed :
            q=self._FinalQ
        else:
            q=0 
            if not self.buyer is None:
               for i in range(len(self.buyer.product)):
                    if self.buyer.product[i] ==self.material:
                        q=self.buyer.prdQuantity[i]
                        
                        
                        #q=min(qnow, self.seller.prdQuantity)
                        if self.seller is not None:
                            if self.seller.product== self.material:
                                q=min(self.seller.prdQuantity,q)             
                        else:
                            if self.seller is not None:
                                if self.seller.product == self.material:
                                    q=self.seller.prdQuantity    
        #print('aaaa',self.seller.prdQuantity[1])
        #q= min(self.seller.prdQuantity, q)
        return q  
    
    
        
    
    @property
    def price(self):
        if not self.executed: # and self.seller.sys.histories.collated:
            p=self.seller.prdPrice
           # print(self.seller.sys.histories[0].averagePrice(self.period))
        else:
            
            p=self._FinalP
        return p

    def Sorttrust(self):
        return self.seller.trust

    def Sortdis(self):
        return self.seller.distance
        
    def Sortexperience(self):
        return self.seller.experience
    
    def Sort(self):
        return self.price
    
    def __str__(self):#str(transaction) returns this function
        print("transaction: ",self._seller.name)
        if self.buyer==None:
            rtn=[self._seller.name,"is selling",round(self.quantity,2),"for",self.seller.prdPrice,"value",round(self.value,2)] 
        elif self._buyer.rmDemand< 0.00001:
            rtn=[self._buyer.name,"fullfilled","("+self.seller.name+")"]             
        elif self.seller.prdQuantity < 0.00001:
            rtn=[self._seller.name,"depleted"]             
        else:
            rtn=[self._seller.name,"sold",round(self.quantity,2),"to", self.buyer.name,"for",self.seller.prdPrice,"value",round(self.value,2)] 
        return list2str(rtn," ")

    @property
    def value(self):
        #comment('aaaaaa',self.quantity * self.price )

        self._value= self.quantity * self.price
        return self._value


    

    def execute_contract(self,buyer):
        self._buyer=buyer        
        for i in range(len(self.buyer.product)):
            if  self.material == self.buyer.product[i]:
                a = self.seller.prdQuantity
        self.buyer.prdQuantity[i] += a
        self._FinalQ=self.seller.prdQuantity
        self._FinalP=self.price
        self.buyer.money -= self.value
        self.seller.money += self.value
        self.distance=self.get_distance   
        #self.buyer.trades.append(self)
        #self.seller.trades.append(self)
        self.buyer.sys.Contractreporter.Writeinstance(self)                
        
        """
        if self.buyer is not None and self.seller is not None and self.quantity > 0.00001:
            print('bbb',self.buyer.name,self.seller.name)
            if DEBUG:comment("Executing trade",str(self).split(" "))
            if self.current:
                self._FinalQ=self.quantity
                
                self._FinalP=self.seller.prdPrice
                for i in range(len(self.seller.product)):
                    #print(self.buyer.rmMaterial[i],self.buyer.name)
                    #if  self.material == self.buyer.rmMaterial[i]:
                    #    print(self.buyer.rmMaterial[i],self.material)
                    #    #print('bbb', self.seller.product[j], self.quantity)                    
                        
                          
  
                     #   #print(self.buyer.rmQuantity[i])
                     #   #print(self.buyer.name, self.buyer.rmMaterial[i])                    
                     #   self.buyer.prdQuantity[i] +=self._FinalQ  #  This has been changed from +=self._FinalQ
                     #   print('aaa',self.buyer.prdQuantity)#self.buyer.rmDemand[i] -=self._FinalQ

                    self.seller.prdQuantity -=self._FinalQ 
                    self.seller.SalesQuantity +=self._FinalQ 
                        
                self.buyer.money -= self.value
                self.seller.money += self.value
                self.distance=self.get_distance   
                self.buyer.trades.append(self)
                self.seller.trades.append(self)
                self.buyer.sys.Contractreporter.Writeinstance(self)
            else:
                self.expired
        else:
            if DEBUG: comment("Deal can not proceed",self)"""  


    
    @property
    def get_distance(self):
        #print('aaaaaa',self.quantity * self.price )
        pos_1 = (self.buyer.X - self.seller.X)**2
        pos_2 = (self.buyer.Y - self.seller.Y)**2
        distance = math.sqrt(pos_1  +  pos_2)
        return distance
        
    def distanc(self,buyer):
        self._buyer=buyer
        if self.buyer is not None and self.seller is not None and self.quantity > 0.00001:
            return self.get_distance

    def weib(self, i,n,a):
        return 1 - np.exp(-(i/n)**a)          
"""    
self.period ==self.endperiod or self.period>self.startperiod:"""