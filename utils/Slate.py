# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 17:25:25 2017

@author: F Muller 
"""


#from utils.Slate import Slatefile, SLatefilenew, Slatefileclose, Slate, scribe, scribeln, comment, \
#                        wordinline, IsNumber, IsText, list2str, type2str

#Slatefile(Filename)
#   Changes the current slatefile to the requested slatefile 
#   If the Filename cant be found its created,

#SLatefilenew(Filename,Sheetname="Slate",Path=".")
#   Creates a new workbook, allows you to specify a path and name
#   if filename already exisits the the reference will be to the exisiting book

#Slatefileclose(Filename="*")
#   Closes the specified file, and generates the physical copy on the harddrive
#   "*" will close all open files, 

#Slate(Sheetname)
#   Sets the slate to the SheetName; 
#   a new sheet will be generatedd if the name does not exist

#all Slate functions return a Tuple (success:boolean,msg:string)
#scribe and scribeln do not return anything

#scribe(arg1,arg2,...)
#   write the arguments to succesive cells
#   if no file has been specified the output will be directed to ./output/Slates.xlsx
#   if no sheet has been specified the output sheet defaults to "Slate"

#scribeln(arg1,arg2,...) 
#   writes the arguments to sucessive cells, 
#   and moves the pointer to the first ecll on the next row
 


#  wordinline
#  checks whether the word appears isolated in the line
#  IsNumber confirms whether a variable is a number (long, int, float)
#  IsText confirms the variable is a string (str)

import xlsxwriter
import datetime ,time

try:
    from TPath import TPath
except:
    from utils.TPath import TPath
    
Debug=False

#handies

def wordinline(word,line,sep=" "):
    txt=sep+line+sep
    return txt.find(sep+word+sep)>-1

def IsNumber(variable):
    r=variable
    try:
        r=float(variable)
    except:
        return
    rtn=wordinline(type2str(r),"int long float"," ")
    return rtn

def IsText(variable):
    return wordinline(type2str(variable),"str"," ")

def list2str(lst,sep=", "):
    return sep.join(map(lambda x:str(x),lst))


def type2str(object):
    return type(object).__name__



    
##the writing classes

class xlssheet(object):
    def __init__(me,Parent,Sheetname):
        me.Parent=Parent
        me.row=0
        me.col=0
        me.sheet=Parent.add_worksheet(Sheetname)
        me.Name=Sheetname
        
    def write(me,  *args):
        for cell in args:
            if IsNumber(cell): 
                me.sheet.write(me.row,me.col,float(cell))
                
            elif type2str(cell)=="list":
                for c in cell : me.write(c)
                return #Dont change the col, you'd get an empty cell!!
            elif type2str(cell)=="tuple":
                for c in list(cell): me.write(c)
            elif type2str(cell)=="dict":
                for c,v in cell: me.write(c,v)
            elif IsText(cell):
                txt=cell
                if txt.strip()=="":
                    me.sheet.write(me.row,me.col,"")  #empties
                elif  len(txt)<2 :
                    me.sheet.write(me.row,me.col,txt) #1 letter str
                elif txt[0]!="=":
                    me.sheet.write(me.row,me.col,txt) # not a formula
                elif txt[1]!="=":
                    me.sheet.write(me.row,me.col,txt) # a formula == causes errors
                else:
                    me.sheet.write(me.row,me.col,"'"+txt) 

            else:
                try:
                   me.write(str(cell))
                except:
                   me.write("#NA") 
                return #again, column is alredy changed
            
                
            me.col=me.col+1

    def writes(me,  *args):
        for cell in args:
            if IsNumber(cell): 
                me.sheet.write_column(me.row,me.col,float(cell))
                
            elif type2str(cell)=="list":
                for c in cell : me.write(c)
                return #Dont change the col, you'd get an empty cell!!
            elif type2str(cell)=="tuple":
                for c in list(cell): me.write(c)
            elif type2str(cell)=="dict":
                for c,v in cell: me.write(c,v)
            elif IsText(cell):
                txt=cell
                if txt.strip()=="":
                    me.sheet.write_column(me.row,me.col,"")  #empties
                elif  len(txt)<2 :
                    me.sheet.write_column(me.row,me.col,txt) #1 letter str
                elif txt[0]!="=":
                    me.sheet.write_column(me.row,me.col,txt) # not a formula
                elif txt[1]!="=":
                    me.sheet.write_column(me.row,me.col,txt) # a formula == causes errors
                else:
                    me.sheet.write_column(me.row,me.col,"'"+txt) 

            else:
                try:
                   me.write(str(cell))
                except:
                   me.write("#NA") 
                return #again, column is alredy changed
            
                
            me.col=me.col-1
    
    def writeln(me,  *args):
        me.write(*args)
        me.row=me.row+1
        me.col=0
    
    def writelns(me,  *args):
        me.write(*args)
        me.row=me.row+1
        me.col=0
    
    def writeit(me,  *args):
        me.write(*args)
        me.col=me.col+1
        me.row=me.row-1
        
       
class xls(xlsxwriter.Workbook):
    def __init__(me,Filename="SLates",ShtName="",Path="./output"):    
        # Create a workbook and add a worksheet.
        me._name=Filename.lower()
        tp=TPath(Filename)
        tp.extension=".xlsx"
        tp.path=Path
        if tp.connect:tp.fullname=tp.nextversion
        
        tp.pathcreate()
        try:
            super().__init__(tp.fullname)
        except:
            super().__init(tp.fullname)
        
        
        me._sht=None
        me.Sheets={}
        if ShtName!="" : me.add_xlsheet(ShtName)
        
    
    @property
    def Name(me):
        return me._name
    
    def add_xlsheet(me,name):
        me._sht= xlssheet(me,name)
        me.Sheets[name.lower()]=me._sht
        print("generating ",name)
        return me._sht
    
        
    
    @property 
    def Activesheet(me):
        if not me._sht :  me.add_xlsheet("Slate")
        return me._sht
    
    @Activesheet.setter
    def Activesheet(me,name):
        if name.lower() in me.Sheets:
            me._sht=me.Sheets[name.lower()]
        else:
            me.add_xlsheet(name)
    
    @property 
    def count(me):
        return len(me.Sheets)

    @property 
    def Cell(me,row,col):    
        try:
           celltuple=me._sht.table[row][col]
           if type(celltuple).__name__ in ['String','Number','Boolean']:
               return celltuple[0]
           elif type(celltuple).__name__ =='Formula':
               return celltuple[2]
           elif type(celltuple).__name__ =='ArrayFormula':
               return celltuple[3]
           else:
               return 0
        finally:
           return None 
        return 
    @Cell.setter
    def Cell(me,row,col,val):    
       me._sht.write(row,col,val)

    @property 
    def Text(me,row,col):    
        try:
           celltuple=me._sht.table[row][col]
           if type(celltuple).__name__ in ['Number','Boolean']:
               return str(celltuple[0])
           elif type(celltuple).__name__ =='String':
               return celltuple[0]
           elif type(celltuple).__name__ =='Formula':
               return celltuple[0]
           elif type(celltuple).__name__ =='ArrayFormula':
               return celltuple[0]
           else:
               return None
        finally:
           return None 
        return 
    
    @Text.setter
    def Text(me,row,col,txt):    
       me._sht.write(row,col,txt)

    
        

#cell_string_tuple = namedtuple('String', 'string, format')
#cell_number_tuple = namedtuple('Number', 'number, format')
#cell_blank_tuple = namedtuple('Blank', 'format')
#cell_boolean_tuple = namedtuple('Boolean', 'boolean, format')
#cell_formula_tuple = namedtuple('Formula', 'formula, format, value')
#cell_arformula_tuple = namedtuple('ArrayFormula',
#                                  'formula, format, value, range')


class _Slates(object):
    def __init__(me):
        me.workbooks={}    
        me._bk=None

    def NewBook(me,Filename="Slates",Sheetname="",Path=".\output"):
        #no checking for path as yet....
        if Filename.lower() in me.workbooks:
            me._bk=me.workbooks[Filename.lower()]
        else:
            print("Generating book "+Filename)
            me._bk=xls(Filename,Sheetname,Path)
            me.workbooks[me._bk.Name]=me._bk
      
    
    @property 
    def ActiveBook(me):
        if not me._bk: me.NewBook("Slates")
        return me._bk
    
    @ActiveBook.setter
    def ActiveBook(me,Filename):
        if Filename.lower() in me.workbooks:
            me._bk=me.workbooks[Filename.lower()]
        else:
            me.NewBook(Filename)
            
    @property 
    def count(me):
        return len(me.workbooks)
    
    def ___call___(me,action,*args):
       if action=="close" : 
           for key, bk in me.workbooks.items():
               bk.close()          
    
    def close(me,name="*"):
        rtn="Closed ("+str(me.count)+"): "
        keys=list(me.workbooks.keys())
        for key in keys:
            if name==key or name=="*" :
                rtn=rtn+"'"+key+"' "
                bk=me.workbooks[key]
                del me.workbooks[key]
                bk.close()
        if "Closed ("+str(me.count)+"): "==rtn: rtn="Cannot find slate: "+name    
        return rtn
                    

    def NewSlate(me,Sheetname="Slate2"):
        me.ActiveBook.add_xlsheet(Sheetname)
                
    def __del__(me):
        try:
            if me.count>0 :  me.close()
        finally:
            pass

Slates=_Slates() 

CommentFilename=""

def Slatefile(Filename):
    try:
        Slates.ActiveBook=Filename
        return True,"Set Slatefile to "+Slates.ActiveBook.Name
    finally:
        pass
    return False,"Slate.cant open "+Filename
    

def SLatefilenew(Filename,Sheetname="",Path="./output"):
    #no checking for path as yet....
    try:
        Slates.NewBook(Filename,Sheetname,Path)
        return True,"Opened "+Slates.ActiveBook.Name
    finally:
        pass
    return False,"Slate.cant open "+name
    

def Slatefileclose(Filename="*"):
    try:
        return True, Slates.close(Filename)
    finally:
        pass
    return False,"error closing file "+name
    
def Slate(Sheetname):
    try:
        Slates.ActiveBook.Activesheet=Sheetname
        return True,"Set slate to "+Slates.ActiveBook.Activesheet.Name
    finally:
        pass
    return False,"error opening sheet "+Sheetname

def scribe(*args):
    Slates.ActiveBook.Activesheet.write(*args)

def scribeln(*args):
    Slates.ActiveBook.Activesheet.writeln(*args)

def scribelns(*args):
    Slates.ActiveBook.Activesheet.writelns(*args)

def scribeit(*args):
    Slates.ActiveBook.Activesheet.writeit(*args)


#for comments 
Lasttime=0


def comment(*args):
    global Lasttime
    global Debug   
    global CommentFilename
    if CommentFilename=="" : CommentFilename=Slates.ActiveBook.Name
    if len(list(args))>0 :
        if IsText(list(args)[0]):
            if list(args)[0].lower()=="debug":
               if len(args)==1 : Debug=not Debug
               if len(list(args))>1 : Debug=list(args)[1]=True
               print("debug",Debug)
    
    #store state, and set slate for comment
    bk=Slates.ActiveBook.Name
    sht=Slates.ActiveBook.Activesheet.Name
    Slatefile(CommentFilename)
    #dont forget to store the state of the comment book!
    sht2=Slates.ActiveBook.Activesheet.Name
    Slate("Comments")
    
    #https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior
    nu=time.time()
    if nu-Lasttime>5 :
        Lasttime=nu
        nu=datetime.datetime.now()
        scribeln(nu.strftime("%Y/%m/%d"),nu.strftime("%H:%M"), *args)
    else:
        scribeln("","", *args)
    
    if Debug:print(*args)
    
    #reset slates
    Slate(sht2)
    Slatefile(bk)
    Slate(sht)   
    
    
def s():
    return Slates


if __name__ == "__main__": #this will only run if this module is run as a script
    print ("Slate.test start")
    print(Slatefile("File1"))
    
    #note comment will be forced to open a Slates file for comments if not asked
    comment(Slate("plop"))
    scribe(1,2,3,4,5)
    scribeln(2,3)
    comment(Slatefile("File2"))
    scribeln(2,3,"wwwwqqq")
    scribeln(2,3)

    comment(Slatefile("File1"))
    scribeln(1,2,3,4,"p1")
    comment(Slate("plop2"))
    scribe(1,2,3,4,"p2")



    comment("test")
    comment("test1")
    comment("DEBUG",True)
    comment("test2")
    comment("test3")
    
    lst =[5,2,1,3,4,"plop"]
    for i in lst:
        scribeln(i)
    
    success,msg=Slatefileclose()
    print(msg)
    print ("done, "+str(Slates.count)+" files left")
    print ("Slate.test ends")

   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    