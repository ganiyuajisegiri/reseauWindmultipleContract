# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 16:21:56 2017

@author: pmgoa
"""

from reseau.baseagent import BaseAgent
from reseau.transaction import Transaction
import random

from utils.Slate import Slatefile, SLatefilenew, Slatefileclose, Slate, scribe, scribeln, comment, \
                        wordinline, IsNumber, IsText, list2str, type2str
from utils.reporter import Reporter  
DEBUG= False
import numpy as np
import matplotlib.pyplot as plt



class Seller(BaseAgent):
    """This is the Market buyer class"""    
    def __init__(self,sys,name):
        super().__init__(sys,name) 
        if DEBUG:comment("Loading","Seller",name)
        
        #add variables
         #Rawmaterial
        #Product
        self.product=[]
        self.prdPrice=[]
        self.prdQuantity=[]
        #self.prdPriceDelta=0
        self.prdPriceVariance=[]
        self.SalesQuantity=[]
        self.contribution=[]        
        self._include=self._include+["product","prdQuantity","prdPrice","SalesQuantity"]
        self.scale = 0
        self.shape = 0

    def __repr__(self):
        return list2str("Seller",[self.name,self.product,round(self.prdQuantity)]," ")

    
    def tossCoin(self):
        return random.random()    
    
    def PredictRequirements(self,condition="random"): 
       
       for i in range(len(self.SalesQuantity)):
           self.SalesQuantity[i]=random.gauss(self.SalesQuantity[i],self.SalesQuantity[i]*0.03)
           """ A Gaussian CDF is used here. A fair coin is thrown and the probability is traced out"""
       
       #condition = "riskbased"   
       for i in range(len(self.product)):
           HOK,history = self.sys.histories.find(self.product[i])
           avrg_price, avrg_qty=history.averagePrice(10)
           if condition =="random" or self.scale <=0:
               self.prdPrice[i]=round(random.gauss(self.prdPrice[i],self.prdPriceVariance[i]),3)
           elif condition =="riskbased" and HOK and avrg_price==0:
               deltaP=self.prdPrice[i]
           elif condition =="riskbased" and HOK:
               deltaP=(avrg_price - self.prdPrice[i])/avrg_price
               if abs(deltaP) >1e-21:
                   """
                   Note:
                   scale = lambda
                   shape = k"""
                   fofP=self.weib(abs(deltaP),self.scale,self.shape)
                   coin=random.random()
                   if coin < fofP:
                      self.prdPrice[i]=self.prdPrice[i]
                   else:
                       self.prdPrice[i] =self.prdPrice[i] +((avrg_price - self.prdPrice[i])*random.random())                  
                   

       

 
           
       #self.prdQuantity=self.SalesQuantity
       #comment("PSQ: "+self.name,round(self.SalesQuantity,2),self.product,round(self.priceV(),2))
       #tradesBook.append([sys.count, self.rmQuantity])

    def ProductionStep(self):
        self.prdQuantity=self.SalesQuantity
        #print('aaa',self.prdQuantity)
     
    # @property
    def gettransaction(self,material):
        return Transaction(self,material)       

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, value):
        if value >= 0:
            self._shape = value
        else:
            self._shape =0

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value            


    def LoadParam(self,key,value):
        #factory name
        rtn=super(Seller,self).LoadParam(key,value)
        if rtn : return rtn
        
        rtn=True
            
        #product description
        if key.lower() =='prd name':
            self.product.append(value)
            self.prdQuantity.append(0)
        #elif key.lower() == 'product stock':
        #    self.prdQuantity= value
        elif key.lower() == 'shape':
            self.shape = value
        elif key.lower() == 'scale':
            self.scale = value
        elif key.lower() == 'product target':
            self.SalesQuantity.append( value)
        elif key.lower() =='prod price':
            self.prdPrice.append(value)  
        elif key.lower() == 'price variance':
            self.prdPriceVariance.append(value)
        elif key.lower() == 'contr':
            self.contribution.append(value)
        elif key.lower() == 'account balance':
            self.money = value
        elif key.lower() == 'unit':
            self.unit = value
        else:
            rtn=False
            if type2str(self)=="Seller":comment("Seller",self.name,"does not have", key,value)
        return rtn    

    @property
    def product(self):
        return self._product

    @product.setter
    def product(self, value):
        self._product = value
   

    """@property
    def prdPrice(self):
        return self._prdPrice#+self._prdPriceDelta

    @prdPrice.setter
    def prdPrice(self, value):
        if value >= 0:
            self._prdPrice= value
            #self._prdPrice = random.gauss(self._prdPrice,self._prdPrice*0.03)
        else:
            #comment("Quantity below 0 is not possible; set to zero")
            self._prdPrice = 0
    
    @property
    def prdPriceVariance(self):
        return self._prdPriceVariance

    @prdPriceVariance.setter
    def prdPriceVariance(self, value):
        if value >= 0:
            self._prdPriceVariance= value
        else:
            #comment("Quantity below 0 is not possible; set to zero")
            self._prdPriceVariance = 0"""

    def writeheader(self):
        self.Reporter.Writeheader()
        #self.Reporter.scribe("plop")
        #self.Reporter.scribe("std")
        #self.Reporter.scribe("slope")
    

        
    def Reportme(self):
        #report trades
        self.q=1e-22
        self.v=0  
        for t in self.trades :
            #self.sys.Transactionreporter.Writeinstance(t)
            self.q=self.q+t.quantity
            self.v=self.v +t.quantity*t.price
        #self.averageP=self.v/self.q
        #self.fofP = self.weibulcdf(self.averageP,n,a)
        #self.store.append(self.fofP)
            
        self.tradesarchive=self.tradesarchive+self.trades
        self.q2=1e-22
        self.v2=0
        if len(self.tradesarchive)>0:
            for i in range(0,min(10,len(self.tradesarchive))):
                t=self.tradesarchive[-i-1]
                self.q2=self.q2+t.quantity
                self.v2=self.v2+t.quantity*t.price
        self.trades=[]           
        #reporte selected properties 
        #self.average2 =(self.v2/self.q2)
        #self.ff.append(self.average2)
        #report additional Values
        self.Reporter.scribe(self.v/self.q)
        self.Reporter.scribe(self.v2/self.q2)
        self.Reporter.scribe("slope")

    
    def weib(self, i,n,a):
        return self.weibulcdf(i,n,a)
        #plt.plot(np.asarray(self.gg),self.weibulcdf(np.asarray(self.gg),n,a)) 
    
    def print_balance(self):
        r"""
        Print balance
        """
        print("Printing Company %s input stock balance:..." %self.name.upper())
        print("Stock:",self.product, "DemandQuantity:", self.prdPrice,\
             "rmQuantity:", self.prdQuantity)
        print("==========================================================================")