# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 11:25:32 2018

@author: pmgoa
"""

from reseau.factory import Factory
from utils.Slate import Slatefile, SLatefilenew, Slatefileclose, Slate, scribe, scribeln, comment, \
                        wordinline, IsNumber, IsText, list2str, type2str
from utils.reporter import Reporter 
import random
 
DEBUG =  False

class Biorefinery(Factory):

    def __init__(self,sys,name):
        if DEBUG:comment("loading","Biorefinery",name)
        super().__init__(sys,name) 
        
        #add variables
         #Rawmaterial
        #Product
        self.conversion = []
        self._exclude=["MSBuyerQuantity", "rmDemand"]
        self._include=self._include+[]


    def __repr__(self):
        return list2str("Factory",[self.name,self.product,round(self.prdQuantity),self.rmMaterial,self.rmQuantity]," ")


    
    def PredictRequirements(self,condition="random"):
       #work out the toal amount of product to be generated in the this period 
       for i in range(len(self.SalesQuantity)):
           self.SalesQuantity[i]=random.gauss(self.SalesQuantity[i],self.SalesQuantity[i]*0.03)
       
       #condition = "riskbased"   
       for i in range(len(self.product)):
           HOK,history = self.sys.histories.find(self.product[i])
           psys=history.averagePrice(10)
           if condition =="random" or self.scale <=0:
               self.prdPrice[i]=round(random.gauss(self.prdPrice[i],self.prdPriceVariance[i]),3)
           
           elif condition=="riskbased" and HOK and psys ==0:
               deltaP= self.prdPrice[i]
           elif condition =="riskbased" and HOK:
               deltaP=(psys - self.prdPrice[i])/psys
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
                       self.prdPrice[i] =self.prdPrice[i] +(deltaP*random.random())                  

       #work out the rm demand for this  
       for i in range(len(self.rmQuantity)): 
           sums=0
           if self.conversion[i]>0 :
               sums += ((self.SalesQuantity[i]/self.conversion[i]) +self.rmQuantity[i])
           self.rmDemand[i]=sums
       #print(self.period,self.name,self.rmDemand,self.rmMaterial)
           #self.prdQuantity=self.rmQuantity*self.conversion
           #if DEBUG:comment(self.name,"predicted sales: ",round(self.prdQuantity[i],2), self.product[i],"target", round(self.SalesQuantity[i],2),"price",round(self.prdPrice[i],2))       
           
                
    def ProductionStep(self):
       self.prdQuantity =[]
       sums=0 
       for i in range(len(self.rmQuantity)):
           sums +=self.rmQuantity[i]*self.conversion[i]

       for i in range(len(self.contribution)):
           self.prdQuantity.append(sums *self.contribution[i])
                  
       #for i in range(len(self.rmQuantity)):
       #    self.rmQuantity[i]=0
       
     
    def LoadParam(self,key,value):
        #factory name
        rtn=Factory.LoadParam(self,key,value)
        if rtn : return rtn
        #rtn=Seller.LoadParam(self,key,value)
        #if rtn : return rtn
        
        rtn=True
        
        #raw material dwescription
        if key.lower() == 'rm usage':
            self.conversion.append(value)
        else:
            rtn=False
            if type2str(self)=="Factory":comment(self.name,"does not have", key,value)