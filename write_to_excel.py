import openpyxl
import getpass

def write_to_excel(schedule_entries):
    wb = openpyxl.load_workbook('helper_files/Grade Beam Schedule - BLANK.xlsx')
    ws = wb.active
    ws.title = "GBSchedule"

    start_row = 7
    start_col = 3

    for row, entry in schedule_entries.items():
        # this 6 needs to be replaced with a 10 when all stirrup info is being added to the sched
        for col in range(0,6):
            ws.cell(row=row+start_row, column=col+start_col).value = entry[col]

    wb.save('/users/'+getpass.getuser()+'/Desktop/GBSchedule.xlsx')