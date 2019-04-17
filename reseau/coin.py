# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 12:09:47 2017

@author: pmgoa
"""

import random

import matplotlib
import matplotlib.pyplot as plt

total_heads = 0
total_tails = 0
upper_limit =0.66
lower_limit = 0.35
count = 0

change=0
nochange=0



while count < 10:

    coin = random.random()
    #print(coin)
    if coin < lower_limit or coin > upper_limit:
        #print("Heads!\n")
        nochange += 1
        count += 1

    elif coin > lower_limit and coin <= upper_limit:
        #print("Tails!\n")
        change += 1
        count += 1

#print("\nOkay, you flipped heads", total_heads, "times ")
#print("\nand you flipped tails", total_tails, "times ")
#print("probability of head occuring is", change/count)


class Coin:
    def __init__(self,n):
        self.sideup ='Heads'
        self.n = n
        self.total_heads=0
        self.total_tails=0
        self.count=0
        
    
    def toss(self):
        while self.count <self.n:
            coin = random.randint(0, 1)
            if coin == 0:
                self.sideup = 'Heads'
                self.total_heads += 1
                self.count += 1            
            else:
                self.sideup ='Tails'
                self.total_tails += 1
                self.count += 1 
        
    def probHead(self):
        print("\nOkay, you flipped heads", self.total_heads, "times ")
        print("\nand you flipped tails", self.total_tails, "times ")
        print()
        print ("probability of head occuring is", self.total_heads/self.count)
        print ("probability of tail occuring is", self.total_tails/self.count)

        
#c=Coin(100)
#c.toss()
#c.probHead()


def PredictRequirements():
    count=0
    prdPrice=1.2
    prdPriceVariance = 0.17
    #work out the toal amount of product to be generated in the this period 

    while count < 10:
        prdPrice=round(random.gauss(prdPrice,prdPriceVariance),3)
        print(count, prdPrice)
        coin = random.random()
        # print(coin)
        if coin < lower_limit or coin > upper_limit:
            prdPrice =prdPrice
            print('rrrr',coin, prdPrice)
            count += 1 
        elif coin > lower_limit and coin <= upper_limit:
            prdPrice =prdPrice *0.8
            print('ssss',prdPrice)
            count += 1 
    print(coin, prdPrice)

#PredictRequirements()

import random

def rollDice():
    roll = random.randint(1,100)
    return roll

# Now, just to test our dice, let's roll the dice 100 times. 

x = 0
while x < 100:
    result = rollDice()
    x+=1


import random


# let us go ahead and change this to return a simple win/loss
def rollDice():
    roll = random.randint(1,100)

    if roll == 100:
        print(roll,'roll was 100, you lose. What are the odds?! Play again!')
        return False
    elif roll <= 50:
        print(roll,'roll was 1-50, you lose.')
        return False
    elif 100 > roll >= 50:
        print (roll,'roll was 51-99, you win! *pretty lights flash* (play more!)')
        return True


'''
Simple bettor, betting the same amount each time.
'''
def simple_bettor(funds,initial_wager,wager_count):
    value = funds
    wager = initial_wager

    currentWager = 0

    while currentWager < wager_count:
        if rollDice():
            value += wager
        else:
            value -= wager

        currentWager += 1
        print ('Funds:', value)



#simple_bettor(10000,100,100)



def rollDice():
    roll = random.randint(1,100)

    if roll == 100:
        return False
    elif roll <= 50:
        return False
    elif 100 > roll >= 50:
        return True


'''
Simple bettor, betting the same amount each time.
'''
def simplebettor(funds,initial_wager,wager_count):
    value = funds
    wager = initial_wager

    # wager X
    wX = []

    #value Y
    vY = []

    # change to 1, to avoid confusion so we start @ wager 1
    # instead of wager 0 and end at 100. 
    currentWager = 1

    #           change this to, less or equal.
    while currentWager <= wager_count:
        if rollDice():
            value += wager
            # append #
            wX.append(currentWager)
            vY.append(value)
            
        else:
            value -= wager
            # append #
            wX.append(currentWager)
            vY.append(value)

        currentWager += 1
        
    #print 'Funds:', value

    plt.plot(wX,vY)
    


x = 0

# start this off @ 1, then add, and increase 50 to 500, then 1000
while x < 100:
    simplebettor(10000,100,1000)
    x += 1


plt.ylabel('Account Value')
plt.xlabel('Wager Count')
plt.show()