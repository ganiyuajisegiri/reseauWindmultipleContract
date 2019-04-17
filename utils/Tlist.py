# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 18:02:32 2017

@author: Frans
"""

#from utils.FLMUtil import wordinline, isnumber, istext, list2str, type2str, , ,

import utils.FLMSort 


#Mulutil elements copied here to minimise dependencies
#find a whole word in a line (actually looks for " word " in " line ")
def wordinline(word,line,sep=" "):
    txt=sep+line+sep
    return txt.find(sep+word+sep)>-1

def isnumber(variable):
    try:
        r=float(variable)
        r=wordinline(type(r).__name__,"int long float"," ")
        return r
    except:
        return False
    
def istext(variable):
    return wordinline(type2str(variable),"str"," ")

def type2str(object):
    return type(object).__name__

import re
# when sorting plop12 appears before plop2 as 1<2
#this routine changes plop2 into plop000002 and plop12 into plop000012
#so that when sorting the plop000012 >plop000002 
def sortcast(val):
    if not istext(val):return val
    txt=""
    for elm in re.split('(\d+)',str(val)):
        if isnumber(elm):
            txt=txt+"{:6d}".format(int(elm))
        else:
            txt=txt+elm
    return txt
    

vbtab="\t"
vbcr="\n"

from math import log10
def vformat(aVal, AsPct = False,acc=3,mag=3 ):
  #Dim dy, nf, Pct
      if aVal is None: return ""
        
      if not isnumber(aVal) :
         return   "{}".format(aVal)
      aVal=float(aVal)
      dy = abs(aVal)
      if AsPct : 
          dy = dy * 100
          endstr="%}"
      else:
          endstr="f}"

      acc=int(acc)
      
      lv=log10(dy)
      base=int(lv)
      if base>=acc:
          dum=10**(base-acc+1)
          aVal=int(aVal/dum)*dum
      
      if dy>10**mag or dy<10**(-mag):
          mod=10**(lv-base)
          n3=int(base/3)
          if n3<0:n3=n3-1
          n3=n3*3
          mod=10**(lv-n3)
          #print ("w ",mod,n3,base)
          if n3==0:
              nf ="{:."+str(max(0,acc-base-1))+endstr
              return nf.format(aVal)  
          else:
              return vformat(mod,acc=acc,mag=mag)+"x10^"+str(n3)
      else:
         if dy<1 :acc=acc+1
         nf ="{:."+str(max(0,acc-base-1))+endstr
         return nf.format(aVal)  

 




# baseclass for a two way linked list
class Tlist(utils.FLMSort.FLMSort):
    _first1=None
    _last1=None
    _prev1=None
    _next1=None
    _count=0
    __separators=" \t"
    parent=None
    allowduplicates=True
    def __init__(me,parent=None,name="",value=None, units=" - "):
        if isinstance(value,list):
           super().__init__(name=name)
           for elm in value:
               rtn=Tlist(parent=me,value=elm)
               me.add (rtn)
        else:
           super().__init__(name=name,value=value)
            
        #me.parent=FLMLISt()
        if parent:
            parent.add(me)

    def remove(me,index=None):

        if index: #remove the elm at the requested index
            rtn=me.items(index)
            if rtn:rtn.remove()
            return
        elif me.parent is None: # not in list
            return
        
        #now remove elm from list
        if me._prev1 is not None:
            me._prev1._next1=me._next1
        else:
            me.parent._first1=me._next1
            
        if me._next1 is not None: 
            me._next1._prev1=me._prev1
        else:
            me.parent._last1=me._prev1
        #update parent
        me.parent._count-=1
        #remove sibling links
        me._next1=None
        me._prev1=None
        me.parent=None

    @property
    def count(me):
        c=me._first1 
        i=0
        while c:
            i+=1
            c=c._next1
        me._count=i
        return i
       
    def __len__(me):
        return me.count
    
    @property
    def paramcount(me):
        i=0
        c=me._first1
        while c :
            if not c._first1:i+=1
            c=c._next1
        return i

    @property
    def paramlist(me):
        lst=[]
        for c in me:
            if not c._first1:lst.append(c)
        return lst

    @property
    def listscount(me):
        i=0
        c=me._first1
        while c :
            if c._first1:i+=1
            c=c._next1
        return i

    @property
    def lists(me):
        lst=[]
        for c in me:
            if c._first1:lst.append(c)
        return lst

    @property
    def islist(me)->bool:
        return me._first1 is not None
    

    @property
    def ismatrix(me):
        return me.paramcount==0  and me.listscount>0
    @property
    def islinear(me):
        return me.listscount==0
    @property
    def istree(me):
        return me.paramcount>0  and me.listscount>0
    

    def clearlist(me):
        me._first1=None
        me._last1=None
        me._prev1=None
        me._next1=None
        me._count=0
        me.__separators=" \t,;:"
    

       

    @property
    def index(me):
        if me.parent :
            return me.parent.indexof(me)
        else:
            return -1
    
    #retrieve the first time a value or a name occurs
    def indexof(me,obj):
        if me._first1 is None: return -1
        if not isinstance(obj,Tlist):
            obj=me.items(element=obj)
            if obj is None: return -1
        c=me._first1 
        i=0
        while not c is None and not c is obj:
            i+=1
            c=c._next1
        if c:
            return i
        else:
            return-1
    
    #convert any object into an element
    def __elm2object(me,value=None,name=None,units=" -"):
        if not isinstance(value,Tlist):
            if name is None:
                if callable(value):
                    try:
                        name=me.item2str(value)
                    except:
                        name=str(value)
                else:
                    name=type2str(value)
            elm=Tlist(me,name=name,value=value,units=units)
        else:elm=value
        
        return elm
        
    #add a base from one series to another
    #converts items to Tlist objects
    def add(me,param1=None,param2=None,units=" -"):
        
        if isinstance(param1,Tlist):
            if param1 is me : return me#can add yourelf...
            elm=param1
        else:
            if isinstance(param1,str) and isnumber(param2):
                name=param1
                value=param2
            elif isinstance(param2,str) and isnumber(param1):
                name=param2
                value=param1
            elif isinstance(param1,str) and isinstance(param2,str):
                name=param1
                value=param2
            elif isinstance(param1,str) and isinstance(param2,list):
                name=param1
                rtn=Tlist(me,param1)
                for elm in param2:
                    rtn.add(elm,units=units)
                return rtn
            elif param1 is not None and param2 is None:
                name=None
                value=param1
            else:
                value=param1
                name=param2
            #create element    
            elm=me.__elm2object(value=value,name=name,units=units)  
        
        return me.insert(elm,me.count)

    
    
    def insert(me,element,index=-11111):
        if not isinstance(element,Tlist) :return #can only deal with elements
        if element is me : return me #can add yourelf...
        if  element.parent is me and index>element.index:
            index=index-1

        if not me.allowduplicates:
            if element._name: 
                if me.indexof(element._name)>-1:return me.items(element=element._name)
            elif element._value:
                if me.indexof(element._value)>-1:return me.items(element=element._value)
        
        element.remove()
        #uinvert for neg numbers
        if index<0 : index=me.count+index+1
        
        i=0
        elm=me._first1
        if index>me._count:elm=None #add to the end...
        
        while elm is not None and not i==index:
            i+=1
            elm=elm._next1
        
        if elm is None:
            #we ran out of elements add to the end
            if  me._first1 is None:
                me._first1=element
            else:
                me._last1._next1=element
    
            me._count+=1
            element._next1=None
            element._prev1=me._last1
            me._last1=element
            element.parent = me  
            return element
        else:
            if elm._prev1 is None:
                elm._prev1=element
                element._next1=elm
                element._prev1=None
                me._count+=1
            else:
                elm._prev1._next1=element
                element._prev1=elm._prev1
                elm._prev1=element
                element._next1=elm
                me._count+=1
            if element._prev1 is None :me._first1=element
            if element._next1 is None :me._last1=element
            element.parent = me  
            return element
                
    
    #generate itteration behaviour e.g. for elm in Tlist:
    def __iter__(me):
        me._currentobj=me._first1
        return me

    def __next__(me):
        if me._currentobj  :
            rtn=me._currentobj 
            me._currentobj=me._currentobj._next1
            return rtn
        else:
            raise StopIteration

    def findname(me,name=""): #returns an object from a "path" string e.g. book1.sheet3.A1
        lst=name.split(".")
        if len(lst)==0 or lst[0]=="":
            return (False,me)
        else:
            found,obj= me.find(lst.pop(0))
            if not found:
                return (False,None)
            else:
                return (True,obj.findname(".".join(lst)))
 
    def find(me,name=""): #returns a tuple (found bool,list)
        s=me.items(name)
        return (not s is None,s) 

    def search(me,search="search text"): #returns a tuple (found bool,list) if text is part of a name
        s=me.items(search=search)
        return (len( s)>0,s) 
    
            
    def item2str(me,item):
        return item.name.lower()
            

    def values(me,index=None,col=None,element=None,search="",separator=""):
        rtn=me.items(index=index,element=element, search=search,separator=separator)
        if isinstance(rtn,list):
            rtn=list(map(lambda x:x.value,me))
        elif rtn:
            return rtn.value
        
    def names(me,index=None,search="",separator=""):
        rtn=me.items(index=index, search=search,separator=separator)
        if isinstance(rtn,list):
            rtn=list(map(lambda x:str(x),me))
        elif rtn:
            return me.str(rtn)
        
    def items(me,row=None,col=None,element=None,search="",separator=""):
        if me._first1 is None: return None
        elm=None
        if row is None and search=="" and element==None:
            return list(map(lambda x:x,me))
        elif row is None and search!="" :
            return list(filter(lambda x:wordinline(search,me.item2str(x),separator),me))
        elif element:
            elm=me._first1 
            while not elm is None and elm._name.lower()!=str(element).lower():
                if type2str(elm._value)==type2str(element):
                   if isinstance(element,object) and isinstance(elm._value,object):
                       if elm._value is not None and element is elm._value : break
                   else:
                       if elm._value is not None and element==elm._value: break
                elm=elm._next1
        
        #index is either a key/name or an integer with the ny=umber of the item
        elif isnumber(row) and isinstance(row,int):
            if row<0: row=me.count+row
            elm=me._first1 
            i=0
            while not elm is None and not i==row:
                #check only lists if col is given
                if col is None or elm.islist : i+=1
                elm=elm._next1
        elif istext(row) :
            names=me.itemnames
            if str(row).lower() in names:
                elm=me.items(names.index(str(row).lower()))
        else:
            elm=None 
        
        if col is not None and isinstance(elm,Tlist): 
            return elm.items(row=col)
        else:
            return elm
    
    def __getitem__(me, key):
        #Returns a (worksheet,Success) by its name and index
        if isinstance(key,tuple):
            row=key[0]
            col=key[1]
        else:
            row=key
            col=None
        elm = me.items(row=row,col=col)
        if elm is None: elm=me.items(element=row)
        if elm is None: elm=me.defaultvalue
        return elm
    
    def __delitem__(me, key):
        elm = me.items(row=key)
        if elm is None: elm=me.items(element=key)
        if elm:
            elm.remove()
            del elm
        

    @property
    def copy(me):
        rtn=Tlist()
        #retrieve the attributes
        #this copies all attributes of an instance that heve been set since the generation in  __init__ and onwards
        for k,v in me.__dict__.items():
            if not callable(v) : 
                rtn.__setattr__(k,v)
        #now copy all the other elements in this list    
        elm=me._first1
        while elm:
            rtn.add(elm.copy)
            elm=elm._next1
            
        return rtn
    

    
    @property
    def itemnames(me):
        return list(map(lambda x:me.item2str(x).lower(),me))
    
    def sort(me,attr="name"):
        if me.count<1:return
        lst=me.items()
        lst=me.__Qsort(lst,attr)
        for elm in lst:
            me.add(elm)

    def __Qsort(me,lst, attr="name"):
        if len(lst)<=1:
            return lst
        else:
            lower =[]
            higher =[]
            pivlst =[]
            pivvalue=sortcast(lst[len(lst)//2].__getattribute__(attr))
            for elm in lst:
                elmvalue=sortcast(elm.__getattribute__(attr) )
                if elmvalue < pivvalue:
                    lower.append(elm)
                elif elmvalue > pivvalue:
                    higher.append(elm)
                else:
                    pivlst.append(elm)
            lower = me.__Qsort(lower,attr)
            higher = me.__Qsort(higher,attr)
            return lower + pivlst + higher
            
    def __add__(me,lst2,copy=False): #leaves list2 empty
        for elm in lst2:
            if copy:
                me.add(elm.copy)
            else:
                me.add(elm)

    #
    # String Functions
    #
    #
    
    @property
    def listseparators(me) ->str:
       return me.__separators
    

    @listseparators.setter
    def listseparators(me,separators):
       if separators == me.__separators :return
       txt=""
       if me.count > 0 : txt = me.list2string(me.__separators)
       if separators == "" :
          if me.__separators == "" : me.__separators = "\t"
       else:
          me.__separators = separators
       if txt != "" : me.string2list(txt,me.__separators)
       #Raise_Change
    
    def __isseparator(me,char):
       return  char != "" and wordinline(char[0],me.__separators,"") 
    
    def list2string(me,separators=" ",shape="text",indent=0,indentstr="\t",withname=False,withvalue=True) ->str:
       #Checks
       if separators is None : separators = me.listseparators[0]
       if separators == "none" : separators = ""

       indstr=indentstr*max(0,indent)
       
       #print me
       txt=""
       #if shape!="list":txt=indstr
       if shape=="list":
           txt=txt+me.fullname
           if withvalue and me._value is not None:txt=txt+indentstr+vformat(me._value)
           txt=txt+vbcr
       elif shape=="tree":
           if withname:txt=txt+me.name
           if withname and withvalue and me._value is not None :txt=txt+indentstr
           if withvalue and me._value is not None:txt=txt+vformat(me._value)
           txt=txt+vbcr
       else :#text is default
           if withname:txt=txt+me.name
           if withname and withvalue and me.value is not None :txt=txt+" = "
           if withvalue and me.value is not None:txt=txt+vformat(me._value)
           if me.ismatrix:
               txt=txt+vbcr
               indent=indent-1
       
       if not (me.islinear or me.ismatrix) : 
           shape="tree"
           txt=txt+vbcr
       
       if me._count==0 : return txt
       
       indent=indent+1
       indstr=indentstr*max(0,indent)
       shape=shape.lower()
       
       for elm in me:
           if len(txt)>0 and txt[-1]!=vbcr: 
               txt = txt + separators 

           dtxt=elm.list2string(separators=separators,shape=shape,indent=indent, 
                                   indentstr=indentstr,withname=withname,withvalue=withvalue)
           if shape=="tree":
               txt=txt+indstr+dtxt
           else:
               txt=txt+dtxt
           
           if elm.islist :txt=txt+vbcr

       if shape=="list":txt=txt+vbcr
       if len(txt)>0 and txt[-1]=="\n":txt=txt[:-1]    
       return  txt

    def string2list(me,txt, separators=None, includeseparators = False, formatValues = True):
        #Dim i As Long, Iold, elm As TList
        me.clearlist()
        if separators  == "" : 
            me.value=txt
        else:
            if separators:me.listseparators = separators
            lst=txt.split(vbcr)
            li=0
            if len(lst)>1:
                for txt in lst:
                   Rtn = Tlist()
                   li=li+1
                   Rtn.name="line {:.0f}".format(li)
                   Rtn.__separators = me.__separators
                   elm = ""
                   for i in range(0 , len(txt)):
                      achar = txt[i]
                      if me.__isseparator(achar) :
                         #new word
                         Rtn.add (elm.strip(" \t"))
                         if includeseparators : Rtn.add (achar)
                         elm = ""
                      elif (achar == vbtab) or achar >= " " :
                         elm = elm + achar
                      #end if
                   # next
                   Rtn.add(elm.strip())
                   if Rtn.count == 0 : Rtn.add ("")
                   me.add(Rtn)
            else:
               elm = ""
               for i in range(0 , len(txt)): #!! range stops before the last number
                  achar = txt[i]
                  if me.__isseparator(achar) :
                     #new word
                     me.add (elm.strip(" \t"))
                     if includeseparators : me.add (achar)
                     elm = ""
                  elif (achar == vbtab) or achar >= " " :#strip char w asci<32
                     elm = elm + achar
               me.add(elm.strip())
               if me.count == 0 : me.add ("")
               me.count
        #me._Sorted = False
        #Raise_Change
        return me   
    

if __name__ == "__main__": #this will only run if this module is run as a script
    
    
    print ("this is a double linked list that supports a trees")
    #generation of a list element
    lst=Tlist(name="Opa",value="the toplevel element")
    
    #add 6 elements to the list by creating new instances, passing lst as the parent
    y=Tlist(lst,"elm0",3.3)
    y1=Tlist(lst,"elm3",6)
    y2=Tlist(lst,"elm7",3.3)
    y3=Tlist(lst,"elm1",12)
    y4=Tlist(lst,"elm12",13.3)
    y5=Tlist(lst,"elm7",5.3)
    
    #add new data directly via add
    lst.add("elm3",6.7)
    
    #convert the list to a string ans a liniear list with tthe fullname of the element
    print("Print the list using list2string\n",lst.list2string(shape="list",withname=True))

    #create a new element and add it later
    w=Tlist(lst,"pllop",33)
    lst.add(w)
    
    #or create it and insert it somewhere in the list
    w=Tlist(None,"plop22",22)
    lst.insert(w,3)
    
    #convert the list to a string ans a liniear list with tthe fullname of the element
    print("Print the list using list2string\n",lst.list2string(shape="list",withname=True))
    
    #move elements by just inserting them in a different position
    #negtative locations move it relative the the end of the list
    lst.insert(w,-2)

    print("after insertion\n",lst.list2string(shape="list",withname=True))
    #retrieve items by name (first one found), get the index of the element with 
    #indexof(elm) or elm.index 
    elm=lst["elm0"]
    print("retrieve by name",[elm.name,elm.index,elm,elm.value])
    
    #or by number
    elm=lst[2]
    print("by number",[lst.indexof(elm),elm,elm.value])
    
    #or by the value
    elm=lst[3.3]
    print("\nor even by the value (first occurance off...)\n",[lst.indexof(elm),elm,elm.value])
    
    #the list is zero based and -1 returns the last element
    elm=[lst[0],lst[-1]]
    print("\nthe list is zero based and -1 returns the last element\n",elm)

    
    #search for elemnts with by name
    print("\nsearch for all elements with 'elm7'\n",lst.items(search="elm7"))
 
    #sort the list, default attirbute is the name
    lst.sort()
    print("\nsort by name\n",lst.list2string(shape="list",withname=True))
    
    lst.sort("value")
    print("\nsort by value (or any attribute)\n",lst.list2string(shape="list",withname=True))
    
    lst2=lst.copy
    print("copy the list copies all children as well")
    print("\ncopied list\n",lst.list2string(shape="list",withname=True))
    
    #add elements from an other list removes the items from the donating list
    lst2.add(lst[0])
    lst2.add(lst[0])
    lst2.add(lst[0])
    print("\nold list lost elm 1,2,3\n",lst.list2string(shape="list",withname=True))
    print("\nlist2 now stores these elements at the end\n",lst2.list2string(shape="list"))

    #optimised for text analysis
    #generate lists from strings, this deletes the old list...
    #split on a collection of characters (e.g here space "," and tab "\t"), 
    #cariage returns "\n" are automatically converts the list from a single list to a list of lists

    lst.string2list("this is a test,plop,1\nand here we\t start again"," ,\t")
    #note how the liststring can be used to print the list as text
    print("\nnew list from text \n",lst.list2string(shape="text",withname=False,separators=", "))
    
    #generation of a list element
    #with allowduplicates False, you prevent the same name of value appear twice in a list
    lst=Tlist(name="Opa",value="the toplevel element")
    lst.allowduplicates=False
    
    #add 6 elements to the list by creating new instances, passing lst as the parent
    y=Tlist(lst,"elm0",3.3)
    y1=Tlist(lst,"elm3",6)
    y2=Tlist(lst,"elm7",3.3)
    y3=Tlist(lst,"elm1",12)
    y4=Tlist(lst,"elm12",13.3)
    y5=Tlist(lst,"elm7",5.3)

    print("Allow duplicates set to False stops two 3 and 7 in the list\n",
          lst.list2string(shape="list",withname=True))

    #list dont have to be linear, list of list of lists are fine!
    #build complex trees 
    lst=Tlist(name="tree list")
    #convert a list into a list called line that is addded the the lst
    a=lst.add("line1",[1,2,3,4,5])
    b=lst.add("line2",[12,22,23,42,25])
    c=lst.add("line3",[12,22,23,42,25])
    lst2=Tlist(lst[0],"elm22",[2,3,4,5])
    lst2=Tlist(lst[0],"elm32",[22,32,24,25])
    lst2.add(b)
    lst2=Tlist(lst[0],"elm42",[23,33,34,35])
    print("\nnew list from [] \n",lst.list2string(shape="tree",withname=True))
    
    
    #retrieve values from trees, or matrixes using row and col. row is the index, 
    #col tries and find it in the lists
    print("\n just testing...",repr(lst[1,12]))
    
    l=Tlist()