# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 14:10:48 2017

@author: Frans
"""
if __name__ == "__main__": #this will only run if this module is run as a script
    from Slate import Slatefile, SLatefilenew, Slatefileclose, Slate, scribe, scribeln,scribelns,scribeit, comment, \
                      wordinline, IsNumber, IsText
else:
    from utils.Slate import Slatefile, SLatefilenew, Slatefileclose, Slate, scribe, scribeln,scribelns,scribeit, comment, \
                            wordinline, IsNumber, IsText


#from reporter import Reporter
#use:
#   self.Reporter=Reporter(self)

#to save all properties named with an underscore (self._property)
#
#   self.reporter.Writeval()   
#
#the data is saved to a slate with the name from the a name or _name property
#note that name and _name are therefor not recorded!
    
#   self._exclude=["prop1", "prop2"]
#   if a property _exclude exists, it must be a list containing items not to be included
#   do not include the "_" in the names of the items to be excluded

class Reporter(object):
    def __init__(me,obj=None,Slatename=""):
        
        me._obj=None
        if obj==None : return
        me._obj=obj
        me.name="Unk" #will be redefined in properties
        me._properties=[]
        me._hasheader=False
        if Slatename!="":me.name=Slatename
        
    def __proplist(me):
        #', '.join(i for i in dir(a) if not i.startswith('__'))
        #try:
            lst=list(filter(lambda x:not x.startswith('__'), list(dir(me._obj)))) 
            if  me.name=="Unk":
                if "name" in lst: 
                    me.name=me._obj.__getattribute__("name")
                    lst.remove("name") #dont print the name
                    if "_name" in lst:lst.remove("_name")
                elif "_name" in lst:     
                    me.name=me._obj.__getattribute__("_name")
                    lst.remove("_name") #dont print the name
                
            #lst_=list(filter(lambda x:x.startswith('_'), lst))
            #lstno_=list(filter(lambda x:not x.startswith('_'), lst))

            if "_include" in lst:     
                ilst=me._obj.__getattribute__("_include")
                lst.remove("_include")
                if len(ilst)>0 :
                    lst2=[]  #fill this with items included
                    for txt in ilst:       #include list retrieved from _include property
                        if txt[0]!="_" and txt in lst: #allow inclusing of properties withouth an underscore,
                            lst2.append(txt)           #the have priority over their underscore equivalent (tend to be properties)
                        elif "_"+txt in lst:
                            lst2.append("_"+txt)  #shortcuts to underscored properties are allowed

                    for txt in ilst:       #include underscoreed properties 
                        if txt[0]=="_" and txt in lst and not txt[1:] in lst2: #not if already included as properties withouth an underscore,
                            lst2.append(txt)                  
                else:  #import all single underscored properties
                    lst2=list(filter(lambda x:x[0]=="_",lst))
            
            if "_exclude" in lst:     
                elst=me._obj.__getattribute__("_exclude")
                for txt in elst: 
                    if txt in lst2 :
                        lst2.remove(txt)
                    elif ( "_"+txt in lst2 ):
                        lst2.remove("_"+txt)
                        


            return lst2
        #except:
        #    return []
    

    @property
    def properties(me):
        if len(me._properties)==0 :
            return me.__proplist()
        else:
            #print('aAA', me._properties)
            return me._properties
    
    #this should only be called once, jjust before the first time we report values
    #only then will we collect all the _properties
    #note, we will not see any _properties defined after that!
    def Writeheader(me,slatename=""):    
        if me._hasheader : return #only do this once!
        
        me._hasheader=True
        me._properties=me.__proplist()
        
        if slatename=="" : 
            Slate(me.name)
        else: 
            ok,me.name =Slate(slatename)

        lst2=me.properties
        lists=[]
        listnames=[]
        for txt in lst2:
            a= me._obj.__getattribute__((txt))
            if isinstance(a,list):
                listnames.append(txt)
                #print('sss',txt,a)
                lists.append(a)
                    #scribe(me._obj.__getattribute__((txt))[i])
            else:
                if len(txt)>1:
                    if txt[0]=="_" :txt=txt[1:]
                scribe(txt)
        txt=""  
        maxlen=0
        for a in lists:
            maxlen=max(maxlen,len(a))
            
        if len(lists)>0 :
            for i in range(0,maxlen):
                for j in range(0,len(lists)):
                    if len(lists[j])>i:
                        if IsText(lists[j][i]):
                            txt=lists[j][i]
                            
                            scribe(listnames[j]+"-"+txt)
                            #print('aaa',listnames[j]+"-"+txt)
                        else:
                            if txt!="":
                                scribe(txt+"-"+listnames[j])
                                #print('bbb',txt+"-"+listnames[j])
                            else:
                                scribe(listnames[j])
                                #print('ccc',listnames[j])
                                
                                
        #print(listnames)    
        #print(lists)

    """def Writeheader(me,slatename=""):    
        if me._hasheader : return #only do this once!
        
        me._hasheader=True
        me._properties=me.__proplist()
        
        if slatename=="" : 
            Slate(me.name)
        else: 
            ok,me.name =Slate(slatename)

        lst2=me.properties
        for txt in lst2:
            if len(txt)>1:
                if txt[0]=="_" :txt=txt[1:]
            scribe(txt)"""
    
    def write(me):
        text =[]
        values=[]
        for txt in me.properties:
            if isinstance((me._obj.__getattribute__((txt))),(list,)):
                text.append(txt)
                values.append(me._obj.__getattribute__((txt)))
            

    def scribe(me,value):
        Slate(me.name)
        scribe(value) 
    
    def scribeln(me,value):
        Slate(me.name)
        scribeln(value) 


    def Writeval(me):        
        me.Writeheader()

        Slate(me.name)
        scribeln()
        lists=[]
        listnames=[]
        for txt in me.properties:
            try:
                a= me._obj.__getattribute__((txt))
                if isinstance(a,list):
                    listnames.append(txt)
                    lists.append(a)
                else:
                    scribe(abs(a))
                    
            except:
                scribe("#NA") 
                    
        maxlen=0
        for a in lists:
            maxlen=max(maxlen,len(a))
            
        if len(lists)>0 :
            for i in range(0,maxlen):
                for j in range(0,len(lists)):
                    if len(lists[j])>i:
                        if IsText(lists[j][i]):
                            scribe("")
                        else:
                            scribe(abs(lists[j][i]))
                            
    #for repeated printing of the _properties of a class    
    """def Writeval(me):        
        me.Writeheader()

        Slate(me.name)
        scribeln()
        for txt in me.properties:
            try:
                #scribe(me._obj.__getattribute__((txt)))
                if isinstance((me._obj.__getattribute__((txt))),(list,)):
                    a= me._obj.__getattribute__((txt))
                    for i in a:
                        scribelns(i)      
                    scribeit()
                        #scribe(me._obj.__getattribute__((txt))[i])
                        #pass
                else:
                    scribe(me._obj.__getattribute__((txt)))
            except:
                scribe("#NV")""" 
    #for repeated printing of differnt instances of the same class:
    def Writeinstance(me,obj):     
        if me._hasheader : me._obj=obj
        me.Writeheader()
        Slate(me.name)
        scribeln()
        for txt in me.properties:
            try:
                scribe(obj.__getattribute__((txt)))
            except:
                scribe("#NV") 
        
        
        
    
if __name__ == "__main__": #this will only run if this module is run as a script
    
    class plop(object):
        def __init__(me):
            me._elf=4
            me._name="plop2"
            me.elf3=[42,43,41,45]
            me.elf1=[1,2,4,5]
            me.elf4=[12,21,14,25]
            me.elf5=[22,23,17,27]
            me._exclude=["elf2"]
            me._include=["elf4","elf3","elf1","elf5"]
        
        @property
        def elf(me):
           me._elf=3
           return 1
       
        
    
    s1=plop()
    s=Reporter(s1,"test")    
    print(s.properties)
    s1._www="wert"
    s.Writeval()
    s=Reporter(s1,"test")  
    print(s.properties)
    Slatefileclose()