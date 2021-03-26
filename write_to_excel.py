import openpyxl
import getpass

def write_to_excel(values):
    wb = openpyxl.load_workbook('helper_files/Grade Beam Schedule - BLANK.xlsx')
    ws = wb.active
    ws.title = "GBSchedule"

    start_row = 8
    start_col = 3

    for row in range(len(values)):
        for col in range(len(values[0])):
            ws.cell(row=row+start_row, column=col+start_col).value = values[row][col]

    wb.save('/users/'+getpass.getuser()+'/Desktop/GBSchedule.xlsx')