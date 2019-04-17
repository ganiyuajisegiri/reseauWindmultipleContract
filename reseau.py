# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 16:06:50 2017

@author: pmgoa
"""
import xlrd
from reseau.buyer import Buyer
from reseau.seller import Seller
from reseau.factory import Factory
from reseau.history import Histories
from reseau.wind import Wind


from utils.Slate import SLatefilenew, Slatefileclose, Slate, comment

from utils.reporter import Reporter 

from datetime import datetime
import timeit

start =datetime.now()
starttime=timeit.default_timer()


xl_workbook = xlrd.open_workbook("reseau multipleInputoutputContract.xlsx")
sheet_names = xl_workbook.sheet_names()

SLatefilenew('EIP Output'); 
Slate("Comments")
DEBUG= False

condition = 'riskbased'
"""seller parameter to make decision on how to set it's selling price either randomly or riskbased"""

selection_method = 'chepestprice'
"""buyer parameter to make the decision on how to buy from the seller
   the decision criteria are five.  these are:

   random 
   cheapestprice
   cost
   trust
   experience"""

        
    
class System(object): 
    def __init__(self,c):
        self._count=c
        self.factories=[]
        self.sellers=[]
        self.buyers=[]
        self.agents=[]
        self.winds=[]
        self.details=[]        
        for r in sheet_names:
            ab=xl_workbook.sheet_by_name(r)
            for t in range(0,ab.nrows):
                row = ab.row_values(t)
                a=list(filter(None,row))
            
                if  a[0] =='finished':
                    break
                
                                    
                elif a[0].lower() =='factory':
                    agent=Factory(self,a[1])
                    self.factories.append(agent)
                    self.buyers.append(agent)  
                    self.sellers.append(agent)
                    self.agents.append(agent)


                elif a[0].lower() =='wind':
                    agent=Wind(self,a[1])
                    self.winds.append(agent)
                    self.agents.append(agent)
                    
                elif a[0].lower() =='mseller':
                    agent=Seller(self,a[1])
                    self.sellers.append(agent)
                    self.agents.append(agent)                 
        
                elif a[0].lower() =='mbuyer':
                    agent=Buyer(self,a[1])
                    self.buyers.append(agent)
                    self.agents.append(agent)
                    
                for i in range(0,len(a)-1,2):
                    agent.LoadParam(a[i],a[i+1])

        for agent in self.buyers:
            for contract in agent.contracts:                
                contract.activated
                       
        self.histories=Histories(self)


        self.Transactionreporter=Reporter(self.sellers[0].gettransaction("materialX"),"Transactions")
        self.Contractreporter=Reporter(self.winds[0].get_contract("materialX"),"Contracts")
        
   
        
    @property
    def count(self):
        return self._count
        
    @count.setter  
    def count(self,value):
        self._count=value
        
      
       
       
    def run(self,step_count=0):
        if DEBUG:comment("Market Suppliers")
        if DEBUG:comment()
        if DEBUG:comment("Market Buyers")
        for agent in self.agents:
            comment (agent.name)
            agent.writeheader()

        
        
        comment("=========","=========","=========","START RUN","=========","=========","=========")
        for i in range(step_count):
            self.cycle()
            

        comment("=========","=========","=========","END RUN","=========","=========","=========")

    #system period
    def cycle(self):  
        self.count+=1
        comment("=========","=========","=========","Cycle",self.count,"=========","=========",)

        """Generate buyers and sellers  to estimate their """
        for agent in self.agents:
            agent.ProductionStep()
            agent.PredictRequirements(condition)
            
        for agent in self.buyers:        
            agent.ExcecuteContracts()
                
        for agent in self.buyers:
            agent.BuyRM(self.sellers,selection_method)
         
        self.histories.collateall()         
        
        for agent in self.agents:
           agent.Report()
        
        if DEBUG:comment("End of Cycle: ",self.count)
        
comment("Seller's decision is by ==>", condition,)
comment("Buyer's decision is by ==>", selection_method,)


 
comment("debug",not True)  

sys=System(0)

if __name__ == "__main__":
    sys.run(100)   
    Slatefileclose()

stoptime=timeit.default_timer()        
stop=datetime.now()
print('Programme runtime is: ', stoptime - starttime)  
print('Programme runtime is: ',"--- %s seconds ---" % (stop -start))