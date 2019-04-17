# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 13:09:36 2018

@author: pmgoa
"""

import xlrd
from reseau.seller import Seller
from reseau.baseagent import BaseAgent
from reseau.transaction import Transaction
from reseau.contract import Contract
from utils.Slate import Slatefile, SLatefilenew, Slatefileclose, Slate, scribe, scribeln, comment, \
                        wordinline, IsNumber, IsText, list2str, type2str
                        


    
xl_workbook = xlrd.open_workbook("reseau multipleInputoutputContract.xlsx")
sheet_names = xl_workbook.sheet_names()
#sheet2= xl_workbook.sheet_by_name(sheet_names[9])
sheetlist=[]
for sheetname in sheet_names:
    a=xl_workbook.sheet_by_name(sheetname)
    sheetlist.append(a)
    
sheets = sheetlist[9:]
import random                       
DEBUG= False
                        
class Wind(BaseAgent):
    #This is the Market buyer class
    def __init__(self,sys,name):
        if DEBUG:comment("Loading","Seller",name)
        super().__init__(sys,name) 
        self.SalesQuantity =0  
        self.prdQuantity=0
        self.powerSum = []
        self.product=""
        self.prdPrice=0
        self.prdPriceVariance=0
        self._exclude=["powerSum"]
        self._include=self._include+[]
        self.scale = 0
        self.shape = 0
           
    def ProductionStep(self):
        
        #print(self.powerSum[self.sys.count-1],self.name)

            self.prdQuantity = self.powerSum[self.sys.count+1]

    
    def PredictRequirements(self,condition="random"): 
       
       self.SalesQuantity=0

    def gettransaction(self,material):
        return Transaction(self,material) 
    
    def get_contract(self, material):
        return Contract(self,material) 
    
    def LoadParam(self,key,value):
        rtn=super().LoadParam(key,value)
        if rtn : return rtn
        
        rtn=True
        for sheet2 in sheets:
            if sheet2.name ==self.name:
                #print(self.name)
                x=0
                cell = sheet2.cell(x,6)
                while cell.value != "Wind_Mean_Speed":  #this is in m/s
                    x=x+1
                    cell = sheet2.cell(x,6)
                x=x+1
                cell = sheet2.cell(x,6)
                '''Finds the first row which will contain wind data just incase other files are 
                not in the exact format. The data needs to be in the 6th column with the title 
                Wind - Mean Speed (mps) in a row above.'''
                
                windData = [] 
                for i in range(x,sheet2.nrows):
                    cell = sheet2.cell(i,6)
                    windData.append(cell.value)
                '''convert's the wind velocity data (mps) to the windData array'''    
                    
                area = 8495 # area of turbine's rotation m^2
                rho = 1.23 # density of air kg/m^3

                windpower=[]
                try:
                    powerCoefficient=random.uniform(0,0.65)
                    if powerCoefficient > 0.59:
                        powerCoefficient = 0.55 #"Not Possible" #to break code
                except:
                    print ("Power Coefficient must be less than 0.59 due to Betz limit")
                    return()
            
                half = 0.5
                for i in range(0,len(windData)):
                    windEnergy = (half*rho*area*windData[i]**3 *powerCoefficient)
                    windpower.append(windEnergy)
                '''converts the wind velocity to power (W)'''
                
                for i in range(0,len(windpower),168):
                    self.powerSum.append(sum(windpower[i:i+168])/168)
                    '''sums up the power in increments of 7 days (W/week)'''

           
        #product description
        if key.lower() =='prd name':
            self.product = value
            
        #elif key.lower() == 'product stock':
        #    self.prdQuantity= value
        elif key.lower() == 'shape':
            self.shape = value
        elif key.lower() == 'scale':
            self.scale = value
        elif key.lower() == 'product target':
            self.SalesQuantity = value
        elif key.lower() =='prod price':
            self.prdPrice =value 
        elif key.lower() == 'price variance':
            self.prdPriceVariance =value
        elif key.lower() == 'contr':
            self.contribution =value
        elif key.lower() == 'account balance':
            self.money = value
        elif key.lower() == 'unit':
            self.unit = value
        else:
            rtn=False
            if type2str(self)=="Seller":comment("Seller",self.name,"does not have", key,value)
        return rtn 



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

    @property
    def product(self):
        return self._product

    @product.setter
    def product(self, value):
        self._product = value
                    
    def print_balance(self):
        r"""
        Print balance
        """
        print("Printing Company %s input stock balance:..." %self.powerSum.upper())
        print("Stock:",self.product, "DemandQuantity:", self.prdPrice,\
             "rmQuantity:", self.prdQuantity)
        print("==========================================================================")
        



    
"""
sheetlist=[]
for sheetname in sheet_names:
    a=xl_workbook.sheet_by_name(sheetname)
    sheetlist.append(a)
    
sheets = sheetlist[-2:]
                        
DEBUG= False
                        
class Wind(Seller):
    #This is the Market buyer class
    def __init__(self,sys,name):
        super().__init__(sys,name) 
        if DEBUG:comment("Loading","Seller",name)
        self.SalesQuantity =0
        self.power = []        
        self.powerSum = []
        self.x=0
        for sheet2 in sheets:
            if sheet2.name == self:
            
                self.cell = sheet2.cell(self.x,5)
                while self.cell.value != "Wind - Mean Speed (mps)":
                    self.x=self.x+1
                    self.cell = sheet2.cell(self.x,5)
                self.x=self.x+1
                self.cell = sheet2.cell(self.x,5)
                '''Finds the first row which will contain wind data just incase other files are 
                not in the exact format. The data needs to be in the 6th column with the title 
                Wind - Mean Speed (mps) in a row above.'''
                
                self.windData = [] 
                for i in range(self.x,sheet2.nrows):
                    self.cell = sheet2.cell(i,5)
                    self.windData.append(self.cell.value)
                '''convert's the wind velocity data (mps) to the windData array'''    
                    
                area = 5026.55 # area of turbine's rotation m^2
                rho = 1.225 # density of air kg/m^3
                

                for i in range(0,len(self.windData)):
                    cP = 0.3 #random.uniform(0,0.4) # turbine efficency randomized between 0 to 0.4
                    p = 0.5*area*rho*cP*self.windData[i]**3
                    self.power.append(p)
                '''converts the wind velocity to power (kj/hr)'''
            
        
        for i in range(0,len(self.power),168):
            self.powerSum.append(sum(self.power[i:i+168])/10**3)
        '''sums up the power in increments of 7 days (kj/week)'''

#%%


 x=0
cell = sheet2.cell(x,5)
while cell.value != "Wind - Mean Speed (mps)":
    x=x+1
    cell = sheet2.cell(x,5)
x=x+1
cell = sheet2.cell(x,5)
'''Finds the first row which will contain wind data just incase other files are 
not in the exact format. The data needs to be in the 6th column with the title 
Wind - Mean Speed (mps) in a row above.'''

windData = [] 
for i in range(x,sheet2.nrows):
    cell = sheet2.cell(i,5)
    windData.append(cell.value)
'''convert's the wind velocity data (mps) to the windData array'''    
    
area = 5026.55 # area of turbine's rotation m^2
rho = 1.225 # density of air kg/m^3

power = []
for i in range(0,len(windData)):
    cP = 0.3 #random.uniform(0,0.4) # turbine efficency randomized between 0 to 0.4
    p = 0.5*area*rho*cP*windData[i]**3
    power.append(p)
'''converts the wind velocity to power (kj/hr)'''


for i in range(0,len(power),168):
    self.powerSum.append(sum(power[i:i+168])/10**3)
'''sums up the power in increments of 7 days (kj/week)'''
"""  


    