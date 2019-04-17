# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 20:15:57 2018

@author: Ajisegiri Ganiyu
"""
import os
import xlsxwriter
import xlrd



#newpath =r'C:\/Users\/pmgoa\/OneDrive - University of Leeds\/reseau multiple\/randomrandom\/newpath'
#if not os.path.exists(newpath):
#   os.makedirs(newpath)

def remove_duplicates():
    #book = xlwt.Workbook()  #  this is to open a workbook
    #sheet1 = book.add_sheet(name) # add sheet to the workbook
    
    #path = os.getcwd()          #  get the path
    #files= os.listdir(path)     # get all the files in that directroy in a list
    #file=[]
    #for f in files:
    #   if f.endswith('.xlsx'):
    #       file.append(f)             #  get only the .xlsx
    

    read_file = xlrd.open_workbook("EIP Output v003.xlsx")
    write_file = xlsxwriter.Workbook ('EIP Output v003deleted.xlsx')
    for sheet in read_file.sheets():
            no_rows = sheet.nrows
            no_cols = sheet.ncols
            name = sheet.name
            gen_sheets = write_file.add_worksheet(name)
            line_list = []
            r = 0
            for row in range(0, no_rows):
                line_sublist = [sheet.cell(row, col).value for col in range(0, no_cols)]
                if line_sublist not in line_list:
                    line_list.append(line_sublist)
                    for col in range(0, no_cols):
                        gen_sheets.write(r,col,line_sublist[col])
                    r = r + 1
    write_file.close()

#xl_workbook = xlrd.open_workbook("EIP Output v014.xlsx")
#sheet_names = xl_workbook.sheet_names()

remove_duplicates()
