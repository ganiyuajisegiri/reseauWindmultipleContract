    # -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 16:02:18 2017

@author: pmgoa
"""
import math
#from system import System as sy
from utils.Slate import comment,list2str
import numpy as np


DEBUG = False


class Transaction:
    def __init__(self,seller,material,Qmax=0):
        #these var are recorded
        self._period = seller.sys.count
        self._buyer  = None
        self._seller  = seller
        self._material=material
        self._FinalQ=-1
        self._FinalP=-1
        self._value=-1
        self.distance=0
        self.MaxQuantity=Qmax
        self.transaction_type=""


        
        #these are not (no underscore at the start)
        self._executed=False
        
        #include and exclude
        self._exclude=["executed"]
        self._include=["period","buyer","seller","material","FinalQ","FinalP","value","distance","transaction_type"]
    
    @property
    def period(self):
        return self._period
    
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
    def valid(self):
        for i in range(len(self._seller.product)):
            
            if self.seller.product[i] == self.material:
                return self.seller.product[i].lower()
                
    
    @property    
    def nodeal(self):
        return self.quantity == 0
            
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
                for i in range(len(self.buyer.rmDemand)):
                    if self.buyer.rmMaterial[i] ==self.material:
                        q=self.buyer.rmDemand[i]
                        for j in range(len(self.seller.product)):
                            if self.seller is not None:
                                if self.seller.product[j] == self.material:
                                    q=min(self.seller.prdQuantity[j],q)  
                            else:
                                if self.seller is not None:
                                    if self.seller.product[j] == self.material:
                                        q=self.seller.prdQuantity[j] 
        if self.MaxQuantity <=0 :
            return q
        else:
            return min(q,self.MaxQuantity)
    
    @property
    def price(self):
        if not self.executed: # and self.seller.sys.histories.collated:
            for i in range(len(self._seller.product)):
                    p=self.seller.prdPrice[i]
                    #print('aaa',self.seller.product[i],p)
           # print(self.seller.sys.histories[0].averagePrice(self.period))
        else:
            p=self._FinalP
            #print('bbb',self.material,p)
        #print('ccc',self.material,p)
        return p

        
    
    def Sort(self):
        return self.price

    def Sorttrust(self):
        return self.seller.trust
    
    def Sortdis(self):
        return self.seller.distance
    
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


        
        
    def execute(self,buyer,ContractPrice=0):
        self._buyer=buyer
        #print('aaaaaaaaaa',self.buyer,self.seller.self.seller.prdQuantity)
        if self.buyer is not None and self.seller is not None and self.quantity > 0.00001:           
            if DEBUG:comment("Executing trade",str(self).split(" "))
            self._FinalQ=self.quantity
            
            if ContractPrice<=0:
                for j in range(len(self.seller.product)):
                    for i in range(len(self.buyer.rmMaterial)):
                        if self.material == self.seller.product[j] and self.material == self.buyer.rmMaterial[i]:
                            #print('bbb', self.seller.product[j], self.quantity)  
                            #print('aaaa',self.seller.name)
                            ContractPrice=self.seller.prdPrice[j]
            
            self._FinalP=ContractPrice            
            self._executed =True
            for j in range(len(self.seller.product)):
                for i in range(len(self.buyer.rmMaterial)):
                    if self.material == self.seller.product[j] and self.material == self.buyer.rmMaterial[i]:
                        #print(self.buyer.rmQuantity[i])
                        #print(self.buyer.name, self.buyer.rmMaterial[i])                    
                        self.buyer.rmQuantity[i] +=self._FinalQ  #  This has been changed from +=self._FinalQ
                        self.buyer.rmDemand[i] -=self._FinalQ

                        self.seller.prdQuantity[j] -=self._FinalQ 
                        
            self.buyer.money -= self.value
            self.seller.money += self.value
            self.distance=self.get_distance 
            self.transaction_type=self.get_transaction_type
            self.buyer.trades.append(self)
            self.seller.trades.append(self)
            
            self.buyer.sys.Transactionreporter.Writeinstance(self)

        else:
            if DEBUG: comment("Deal can not proceed",self)  

    
    @property
    def get_distance(self):
        #print('aaaaaa',self.quantity * self.price )
        pos_1 = (self.buyer.X - self.seller.X)**2
        pos_2 = (self.buyer.Y - self.seller.Y)**2
        distance = math.sqrt(pos_1  +  pos_2)
        return distance
        


    def weib(self, i,n,a):
        return 1 - np.exp(-(i/n)**a)

    @property    
    def active(self):
        if self.period<=self.endperiod and self.period>self.startperiod:
            return True

    @property    
    def notactive(self):
        if self.period ==self.startperiod:
            return True

    @property
    def get_transaction_type(self):
        buyer_type =self.buyer.types
        seller_type =self.seller.types
        transaction_type =buyer_type + "-" + seller_type
        return transaction_type
