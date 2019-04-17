# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 00:06:14 2017

@author: Frans
"""
from os import path as osp
from os import makedirs
from glob import glob
import errno

#look here for string manipulation
#http://www.pythonforbeginners.com/basics/string-manipulation-in-python
def wordinline(word,line,sep=" "):
    txt=sep+line+sep
    return txt.find(sep+word+sep)>-1

    
class TPath(str):
    def __init__(me,fullname):
        super().__init__()
        me.clear()
        me.fullname=fullname
        
    def clear(me):
        me._path=""
        me._name=""
        me.extension=""
        me.__disconnect()
    
    
    def __disconnect(me):
        me._connected=False
        me._folders=[]
        me._files=[]
    
    @property
    def path(me):
        return me._path #dispalay without the \\
    @path.setter
    def path(me,Path):
        me._path=Path.replace("/","\\") 
        if not wordinline(me._path[-1],"/ \\"): me._path =me._path+"\\"  #store with the \\
        me.__disconnect()
    
    @property
    def name(me):
        return me._name
    @name.setter
    def name(me,Name):
        lst=Name.split(".")
        if len(lst)>1:
            me.extension=lst[1]
            me._name=lst[0]
        else:
            me._name=lst[0]
        me.__disconnect()

    @property
    def extension(me):
        return me._extension #display without the .
    @extension.setter
    def extension(me,extension):
        if extension=="" :
            me._extension=""
        elif extension[0]!=".":
           me._extension="."+extension
        else:
            me._extension=extension
        me.__disconnect()
        
    @property
    def fullname(me):
        return me.path+me.name+me.extension
    @fullname.setter
    def fullname(me, fullname):
        me.clear()
        fullname=fullname.replace("/","\\")
        if fullname[-1]=="\\" :fullname=fullname[:-1]
        lst=osp.split(fullname)
        me.path=".\\"
        if lst[0]:me.path=lst[0]
        me.name=""
        if lst[1]: me.name=lst[1]



    def __str__(me):
       return me.name+me.extension
    def __repr__(me):
       return me.fullname
   
    @property    
    def nextversion(me) :
        files= glob(me._path+me._name+"*"+me._extension)
        version=-1
        if not files: 
            if me.connect :
                return (me._path+me._name+" v%03d"+me._extension ) % (2,)
            else:
                return me.fullname
        for f in files:
            txt=osp.basename(files[-1])[len(me._name)+2:-len(me._extension)]
            if txt=="" : 
                version=max(version,2)
            else:
                version=max(int(txt),version)
            version=version+1
        print("VERSION of file: ",version)
        txt= (me._path+me._name+" v%03d"+me._extension ) % version
        return txt
    
    @property
    def connect(me)->bool:
        if not me._connected :
            me._connected=osp.exists(me.fullname)
        return me.connected
    
    @property 
    def connected(me)->bool:
        return me._connected

    
    @property
    def isfile(me):
        return osp.isfile(me.fullname)

    @property
    def isfolder(me):
        return osp.isdir(me.fullname)
    
    @property
    def folders(me)->list:
        if me.connect and me.isfolder:
            contents= glob(me.path+me.name+me.extension+"\\*" )
            me._folders=[]
            for f in contents:
                f=TPath(f)
                if f.isfolder:me._folders.append(f)
            return me._folders

    @property
    def files(me)->list:
        if me.connect and me.isfolder:
            contents= glob(me.path+me.name+me.extension+"\\*" )
            me._files=[]
            for f in contents:
                f=TPath(f)
                if f.isfile:me._files.append(f)
            return sorted(me._files)
        
    def pathcreate(me):
        try:
            makedirs(me.path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

if __name__ == "__main__": #this will only run if this module is run as a script
  
    tp=TPath("c:\\users\\frans\\fractal\\sharebox\\output\\EIP output.xlsx")    
    print("helloo")
    print(tp.path,tp.name,tp.extension)    
    print(tp.nextversion)
        
    tp=TPath(".\\..\\output\\EIP output.xlsx")    
    print("2")
    print(tp)
    print (osp.abspath(tp.fullname))
    print(tp.nextversion)
    
    tp.fullname=tp.path
    print(tp.files)
    tp.fullname=tp.path
    print(tp)
    print(tp.folders)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
