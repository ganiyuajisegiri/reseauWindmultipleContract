# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 16:23:44 2017

@author: pmgoa
"""
from reseau.buyer import Buyer
from  reseau.seller import Seller
import random
#from reseau.contract import Contract
from reseau.contract import Contract

from utils.Slate import Slatefile, SLatefilenew, Slatefileclose, Slate, scribe, scribeln, comment, \
                        wordinline, IsNumber, IsText, list2str, type2str
from utils.reporter import Reporter  



DEBUG =  False

class Factory(Buyer,Seller):
    """This is the Factory class"""
    def __init__(self,sys,name):
        if DEBUG:comment("loading","Factory",name)
        super(Factory,self).__init__(sys,name) 
        
        #add variables
         #Rawmaterial
        #Product
        self.contract_comp=[]
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
           avrg_price, avrg_qty=history.averagePrice(10)
           if condition =="random" or self.scale <=0:
               self.prdPrice[i]=round(random.gauss(self.prdPrice[i],self.prdPriceVariance[i]),3)
           
           elif condition=="riskbased" and HOK and avrg_price ==0:
               deltaP= self.prdPrice[i]
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
                       self.prdPrice[i] =self.prdPrice[i] +(deltaP*random.random())                  

       #work out the rm demand for this  
       for i in range(len(self.SalesQuantity)): 
           for j in range(len(self.rmQuantity)):
               sums=0
               if self.conversion[j]>0 :
                   sums += ((self.SalesQuantity[i]/self.conversion[j]) +self.rmQuantity[j])
               self.rmDemand[j]=sums
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
        rtn=Buyer.LoadParam(self,key,value)
        if rtn : return rtn
        rtn=Seller.LoadParam(self,key,value)
        if rtn : return rtn
        
        rtn=True
        
        #raw material dwescription
        if key.lower() == 'rm usage':
            self.conversion.append(value)
        else:
            rtn=False
            if type2str(self)=="Factory":comment(self.name,"does not have", key,value)
    
        return rtn    
    """@property
    def conversion(self):
        return self._conversion

    @conversion.setter
    def conversion(self, value):
        if value >= 0:
            self._conversion = value
            self.conv.append(self.conversion)
        else:
            #comment("conversion below 0 is not possible; set to zero")
            self._conversion = 0"""
     
    def finished(self):
        self.period > self.endperiod
        return True
    
    def weib(self, i,n,a):
        return self.weibulcdf(i,n,a)            
            
    def writeheader(self):
        #super().writeheader()
        Buyer.writeheader(self)
        Seller.writeheader(self)
        
   
    def Reportme(self):
        #super().Report()
        #Buyer.Reportme(self)
        Seller.Reportme(self)
    
    def print_balance(self):
        r"""
        Print balance
        """
        print("Printing Company %s input stock balance:..." %self.name.upper())
        print("Stock:",self.rmMaterial, "DemandQuantity:", self.rmDemand,\
             "prdQuantity:", self.prdQuantity)
        print("==========================================================================")
        
    

 


        #    print(self.name, self.wind.product) 
            #random.shuffle(winds)                            
            #for wind in winds: 
            #    contract_deal=wind.get_contract(self.product[i])  
                
    
            #    if contract_deal.valid:  #  This is to get all the same prdouct for the agents to enter into contract
            #        contract_deals.append(contract_deal)
           #     else:
            #        pass 
        """This is to chose seller and have contract by lowest price"""
        #contract_deals.sort(key=Contract.Sort,reverse=False)  #how do you sort on seller.price?           
        """
        n = 0
        #if self.product[i] == 'Electricity':
        for j in range(len(self.product)):
            #if self.product[j] =='Electricity':
                #print('bbb',self.prdQuantity[j],self.name,self.product[j])
            #while (self.prdQuantity[j]>0) and( n<len(contract_deals) and self.product[j] == 'Electricity'):
                #contract_deals[n].execute_contract(self)
               # n +=1   
            if ((self.prdQuantity[j]>0) and self.product[j] == 'Electricity'):
                if contract_deals[0].current:
                    contract_deals[0].execute_contract(self)
                    del contract_deals[0]"""
                    
                    

