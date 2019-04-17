# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 12:56:39 2018

@author: pmgoa
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter

xls = pd.ExcelFile("winddata.xlsx")

def MyFormatter(x,lim):
    if x == 0:
        return 0
    return '{0}e{1}'.format(x/10**np.floor(np.log10(x)),0)

majorFormatter = FuncFormatter(MyFormatter)


def linechart_wind1():
    df1 = pd.read_excel(xls,'wind1')
    df =df1.Date
    df = list(df)
    date_time = pd.to_datetime(df)      
    df2=df1.Power
    df2=list(df2)
    DF=pd.DataFrame()
    DF['df2'] = df2
    DF = DF.set_index(date_time) 
    fig, ax = plt.subplots()
    plt.ylim([0, 7])
    fig.subplots_adjust(bottom=0.3)
    
    plt.xticks(rotation=45)
    plt.plot(DF,color='r')
    #ax.yaxis.set_major_formatter(majorFormatter)
    plt.ylabel('Power Output [MW in 1h time]',fontsize=12)
    plt.xlabel("Year", fontsize=12)
    plt.minorticks_on()
    plt.grid(b=True,which='minor', linestyle=':',  color='black')
    plt.grid(b=True,which='major', linestyle=':',  color='black')
    plt.yscale=('log')
    plt.savefig('Wind_Power_Output1.png',dpi=300)
    plt.show()    
    
    

   

def linechart_wind2():
    df1 = pd.read_excel(xls,'wind2')
    df =df1.Date
    df = list(df)
    date_time = pd.to_datetime(df)    
    df2=df1.Power
    df2=list(df2)
    DF=pd.DataFrame()
    DF['df2'] = df2
    DF = DF.set_index(date_time) 
    fig, ax = plt.subplots()
    plt.ylim([0, 2])
    fig.subplots_adjust(bottom=0.3)
    
    plt.xticks(rotation=45)
    plt.plot(DF,color='r')
    #ax.yaxis.set_major_formatter(majorFormatter)
    plt.ylabel('Power Output [MW in 1h time]',fontsize=12)
    plt.xlabel("Year", fontsize=12)
    plt.minorticks_on()
    plt.grid(b=True,which='minor', linestyle=':',  color='black')
    plt.grid(b=True,which='major', linestyle=':',  color='black')
    plt.yscale=('log')
    plt.savefig('Wind_Power_Output2.png',dpi=300)
    plt.show()    

linechart_wind1()
linechart_wind2()