# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 16:14:59 2017

@author: pmgoa
"""
from reseau.baseagent import BaseAgent
from reseau.transaction import Transaction
from reseau.wind import Wind
from reseau.seller import Seller
import random
from reseau.contract import Contract

from utils.Slate import Slatefile, SLatefilenew, Slatefileclose, Slate, scribe, scribeln, comment, \
                        wordinline, IsNumber, IsText, list2str, type2str
from utils.reporter import Reporter 

DEBUG=  False
import matplotlib.pyplot as plt
import math




class Buyer(BaseAgent):
    """This is the Market buyer class"""
    def __init__(self,sys,name):
        if DEBUG:comment("Loading","Buyer",name)
        super().__init__(sys,name) 
        #add variables
         #Rawmaterial
        self.rmMaterial=[]
        self.rmQuantity=[]
        self.rmDemand=[]
        self.MSBuyerQuantity=[]
        self.store=[]
        self.averageP=0
        self.fofP=0 
        self.lenght=0
        self._active = False
        self.contracts=[]


        
        
        self._include=self._include+["rmMaterial","MSBuyerQuantity","rmQuantity"]
        
        
    def PredictRequirements(self,condition="random"):
       #work out the rm demand for this
       #self.rmDemand= based on input + random
        for i in range(len(self.MSBuyerQuantity)):                
            self.MSBuyerQuantity[i]=random.gauss(self.MSBuyerQuantity[i],self.MSBuyerQuantity[i]*0.03)
            self.rmDemand[i]=self.MSBuyerQuantity[i]
       
       #self.rmQuantity=0
  
    def ProductionStep(self):
        for i in range(0,len(self.rmQuantity)):
            if len(self.rmQuantity)==0:
                self.rmQuantity[i]=0
       
    def __repr__(self):
        return list2str(["Buyer",self.name,self.rmQuantity,self.rmDemand,"of",self.rmMaterial])

    @property
    def rmMaterial(self):
        return self._rmMaterial

    @rmMaterial.setter
    def rmMaterial(self, value):
        self._rmMaterial = value
       
    """@property
    def rmQuantity(self):
        return self._rmQuantity

    @rmQuantity.setter
    def rmQuantity(self,value):
        if value > 0:
            self._rmQuantity = value
            self.rm.append(self._rmQuantity)
        else:
            #comment("Quantity below 0 is not possible; set to zero")
            self._rmQuantity= 0"""
            
    

    def LoadParam(self,key,value):
        #factory name        
        rtn=super().LoadParam(key,value)
        if rtn : return rtn
        
        rtn=True
        
        #raw material dwescription
        if key.lower() == 'rm name':
            self.rmMaterial.append(value)
            self.rmQuantity.append(0)
            self.rmDemand.append(0)
            self.MSBuyerQuantity.append(0)

        elif key.lower() =='contract':
            self.contracts.append(Contract(self,self.rmMaterial[-1]))
        elif key.lower() =='duration':
            if len(self.contracts)<1 :
                self.contracts.append(Contract(self,self.rmMaterial[-1]))
            self.contracts[-1].endperiod =value
        elif key.lower() =='startperiod':
            if len(self.contracts)<1 :
                self.contracts.append(Contract(self,self.rmMaterial[-1]))
            self.contracts[-1].startperiod =value
        elif key.lower() == 'contract_comp':
            if len(self.contracts)<1 :
                self.contracts.append(Contract(self,self.rmMaterial[-1]))
            self.contracts[-1].Seltmp=value
        elif key.lower() == 'quantity':
            if len(self.contracts)<1 :
                self.contracts.append(Contract(self,self.rmMaterial[-1]))
            self.contracts[-1].contract_quantity=value

        elif key.lower() == 'rm stock':
            if value > 0:
                self.rmQuantity[len(self.rmMaterial)-1]=(value)


        #elif key.lower() == 'rm demand':
        #    self.rmDemand= value
        elif key.lower() == 'msbuyerquantity':
            self.MSBuyerQuantity[len(self.rmMaterial)-1]=(value)
        elif key.lower() == 'account balance':
            self.money = value
        else:
            rtn=False
            if type2str(self)=="Buyer":comment("Buyer",self.name,"does not have", key,value)
    
        return rtn 

    def calculateDistance(self,seller):  
        x1,y1=self.location
        x2,y2=seller.location
        self.distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)  
        return self.distance

    def calculateTrust(self,seller):  
        a=self.Fitness
        b=seller.Fitness
        self.trust = a * b
        return self.trust
        
    def ExcecuteContracts(self):   #pass system.ms to this sub
        for contract in self.contracts:
            contract.Execute
        
                
        #for contract in reversed( self.contracts):  i don't we need to remove again because Isvalid takes care of that
        #    if not contract.IsValid:
        #        self.contracts.remove(contract)
                    
             

    def BuyRM(self,sellers,selection_method):   #pass system.ms to this sub
        
        """ list of each seller is append here"""
        deals=[]
        #contract_deals=[]  #  This is just the list of prospective sellers that the agents that can do contract
                           #  can form contract with
        if DEBUG:comment("=========","=========",self.name,"=========","=========",)
        if DEBUG:comment("Needs",self.rmMaterial,self.rmDemand)        
        
        for i in range(len(self.rmMaterial)):          
            for seller in sellers:   
                deal=seller.gettransaction(self.rmMaterial[i])  #  This/ is where there is problem            
  
                if deal.valid:
                    self.calculateDistance(deal.seller)
                    self.calculateTrust(deal.seller)
                    deals.append(deal)                   
                    
                else:
                    pass #comment(seller.name,"sells",seller.prdQuantity,seller.product) 

        if DEBUG : comment('number of deals',len(deals))

       
        """Selection method begins here"""            
        
        if selection_method == 'random':
            """  This is to chose seller randomly"""            
            random.choice(deals)   
        elif selection_method == 'cheapestprice':
            """This is to chose seller by lowest price"""
            deals.sort(key=Transaction.Sort,reverse=False)  #how do you sort on seller.price?
            
            """This is to chose seller by lowest price and cost(distance)"""
        elif selection_method =='cost':
           deals.sort(key=Transaction.Sortdis,reverse=False)
       
           """This is to chose seller by Trust plus other factors"""
        elif selection_method =='trust':
            deals.sort(key=Transaction.Sorttrust,reverse=False)
             
            """This is to chose seller by experience plus other factors"""
        elif selection_method =='experience':
            pass


        n=0
        while (self.rmDemand[i]>0) and( n<len(deals)):
            #print('aaa',self.rmMaterial[i], self.name,self.rmDemand[i])
            deals[n].execute(self)
            n +=1
    


                                    

        #for i in range(len(contract_deals)):
        #    if contract_deals[i]==[]:
        #       print('cccc','empty')
        #    else:
        #         print('aaa',len(contract_deals),contract_deals[i].seller.name)
        #if self.sys.count > 0:
        #    for i in range(len(contract_deals)):
        #wq        print('aaa',len(contract_deals),contract_deals[i].seller.name)          
        
    def writeheader(self):
        self.Reporter.Writeheader()
        #self.Reporter.scribe("Average")
        #self.Reporter.scribe("std")
        #self.Reporter.scribe(self.name)
       
    def Reportme(self):
        self.q=1e-22        
        self.v=0
        for t in self.trades:
            #self.sys.Transactionreporter.Writeinstance(t)
            self.q=self.q+t.quantity
            self.v=self.v+t.quantity*t.price
        self.averageP=self.v/self.q
        self.store.append(self.averageP)
        self.fofP = self.weibulcdf(self.averageP,n,a)
        self.store.append(self.fofP)
                
                
        self.tradesarchive=self.tradesarchive+self.trades
        self.q2=1e-22
        self.v2=0
        if len(self.tradesarchive)>0:
            for i in range(0,min(10,len(self.tradesarchive))):
                t=self.tradesarchive[-i-1]
                self.q2=self.q+t.quantity
                self.v2=self.v+t.quantity*t.price
                
                
        
        self.trades=[] 
        #self.average2=self.v2/self.q2
        #self.ff.append(self.average2)
        
        #report additional Values
        self.Reporter.scribe(self.v/self.q)
        self.Reporter.scribe(self.v2/self.q2)
        self.Reporter.scribe("slope")

        
    
    def weib(self):
        for i in self.gg:
            
            self.weibulcdf(i,n,a)
    
    def print_balance(self):
        r"""
        Print balance
        """
        print("Printing Company %s input stock balance:..." %self.name.upper())
        print("Stock:",self.rmMaterial, "DemandQuantity:", self.rmDemand,\
             "rmQuantity:", self.rmQuantity)
        print("==========================================================================")
    
    @property    
    def active(self):
        return self._active            
"""

    @property    
    def active(self):
        print('ttt',self.name)
        if self.period ==self.endperiod or self.period>self.startperiod:
            print('zzz',self.name,self.period)
            return True

    @property    
    def notactive(self):
        if self.startperiod ==0:
            return True"""




"""    
 if active:
    while lenght < contract_lenght:
        print('yes')    
        lenght +=1

while lenght < contract_lenght:
    active = True
    print('yes')    
    lenght +=1 

for i in range(5):
    if contract_lenght  <= 5:
        active = True
        print('yes')
        contract_lenght -=1  
lenght=0
contract_lenght =8
 for i in range(5):
    if lenght  <= contract_lenght:
        active = True
        print('yes')
        lenght +=1         
    
        if self.contract =='yes':
            if self.period <self.startperiod: #self.lenght ==0:
                self._active =True
                if (self.rmDemand[i]>0) and( len(contract_deals) >0):
                    
                    contract_deals[0].execute(self)
                    del contract_deals[0]
                    
                    
                #self.lenght +=1  
                                    
                #lenght =
            elif self.startperiod == self.period  or self.period<= self.duration: #self.lenght >0 and self.lenght <= self.duration:
                self._active =True
                if (self.rmDemand[i]>0) and( len(contract_deals) >0):
                    contract_deals[0].execute(self)
                #print('ddd',seller.name,seller.product[i],seller.prdQuantity[i])
                #self.lenght +=1      
        elif self.contract =='no':   
        if contract.period <= contract.duration:
        deal.execute_contract(self)
        elif contract.finished:
        del contract"""