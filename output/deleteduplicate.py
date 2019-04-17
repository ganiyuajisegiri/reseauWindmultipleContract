# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 20:15:57 2018

@author: Ajisegiri Ganiyu
"""
import xlsxwriter
import xlrd





def remove_duplicates():

    read_file = xlrd.open_workbook("EIP Output v039.xlsx")
    write_file = xlsxwriter.Workbook ('Removed.xlsx')
    
    for sheet in read_file.sheets():
        #if sheet.name=='wind1':
        no_rows = sheet.nrows
        no_cols = sheet.ncols
        name = sheet.name
        gen_sheets = write_file.add_worksheet(name)
        line_list = []
        r = 0
        for col in range(0, no_cols):
            line_sublist = [sheet.cell(row, col).value for row in range(0, no_rows)]
            if line_sublist[0] !='':
               line_list.append(line_sublist) 
               for row in range(0, no_rows):
                   gen_sheets.write(row,r,line_sublist[row])
               r = r + 1
    write_file.close()

remove_duplicates()
"""
#xl_workbook = xlrd.open_workbook("EIP Output v014.xlsx")
#sheet_names = xl_workbook.sheet_names()

remove_duplicates()


for sheet in read_file.sheets():
    if sheet.name=='wind1':
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


for sheet in read_file.sheets():
    if sheet.name=='wind1':
        no_rows = sheet.nrows
        no_cols = sheet.ncols
        name = sheet.name
        gen_sheets = write_file.add_worksheet(name)
        line_list = []
        r = 0
        for col in range(0, no_cols):
            line_sublist = [sheet.cell(row, col).value for row in range(0, no_rows)]
            if line_sublist[0] !='':
               line_list.append(line_sublist) 
               for row in range(0, no_rows):
                   gen_sheets.write(row,r,line_sublist[row])
               r = r + 1
write_file.close()"""