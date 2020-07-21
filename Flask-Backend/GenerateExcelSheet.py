import xlsxwriter
import win32com.client as win32




# ModelGrades=[10,10,10,10]
# StudentNamesist=["Amin Ghassan","Ismael Hossam","Omar Yousry","Wael Ashraf"]
# StudentGrades =[[9,9,8,9],[10,9,8,7],[8,9,7,10],[7,6,5,9]]


def WriteHeaders(ModelGrades, worksheet, bold):
    Alphabets=["B1","C1","D1","E1","F1","G1","H1","I1","J1","K1","L1","M1","N1","O1","P1","Q1","W1","X1","Y1","Z1"]
    j=0
    worksheet.write('A1', 'Name', bold)
    for i in range(len(ModelGrades)):
        worksheet.write(Alphabets[j], 'Q'+str(i+1)+'('+str(ModelGrades[i])+')', bold)
        worksheet.write(Alphabets[j+1], 'Q'+str(i+1)+' Comment', bold)
        j+=2
    worksheet.write(Alphabets[j], 'Total Grade'+'('+str(sum(ModelGrades))+')', bold)
     
def WriteStudentNames(StudentNamesist, worksheet, bold):
    row=1
    col=0
    for i in range(len(StudentNamesist)):
        worksheet.write(row,col,StudentNamesist[i])
        row+=1
    row+=1    
    worksheet.write(row,col,"Max",bold)
    worksheet.write(row+1,col,"Avg",bold)  
    worksheet.write(row+2,col,"Min",bold)
    worksheet.write(row+3,col,"Count Max",bold)
    worksheet.write(row+4,col,"Count Above Avg",bold)
    worksheet.write(row+5,col,"Count Below Avg",bold)   
    worksheet.write(row+6,col,"Count Min",bold)
    return row
     
def WriteGrades(StudentGrades, RowNUM, worksheet, chart, StudentNamesist):
    Alphabets=["B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","W","X","Y","Z"]
    row = 1
    col = 1
    i=0
    j=0
    for Answer in (StudentGrades):
        row=1
        for grade in (Answer):
            worksheet.write(row, col , grade)
            row += 1
        row+=1    
        worksheet.write(row, col, '=MAX('+Alphabets[i]+'2'+':'+Alphabets[i]+str(RowNUM-1)+')')
        worksheet.write(row+1, col, '=AVERAGE('+Alphabets[i]+'2'+':'+Alphabets[i]+str(RowNUM-1)+')')
        worksheet.write(row+2, col, '=MIN('+Alphabets[i]+'2'+':'+Alphabets[i]+str(RowNUM-1)+')')
        worksheet.write(row+3, col, '=COUNTIF('+Alphabets[i]+'2'+':'+Alphabets[i]+str(RowNUM-1)+',MAX('+Alphabets[i]+'2'+':'+Alphabets[i]+str(RowNUM-1)+'))')
        worksheet.write(row+4, col, '=COUNTIFS('+Alphabets[i]+'2'+':'+Alphabets[i]+str(RowNUM-1)+',">= " &AVERAGE('+Alphabets[i]+'2'+':'+Alphabets[i]+str(RowNUM-1)+'),'+Alphabets[i]+'2'+':'+Alphabets[i]+str(RowNUM-1)+',"< " &MAX('+Alphabets[i]+'2'+':'+Alphabets[i]+str(RowNUM-1)+'))')
        worksheet.write(row+5, col, '=COUNTIFS('+Alphabets[i]+'2'+':'+Alphabets[i]+str(RowNUM-1)+',"< " &AVERAGE('+Alphabets[i]+'2'+':'+Alphabets[i]+str(RowNUM-1)+'),'+Alphabets[i]+'2'+':'+Alphabets[i]+str(RowNUM-1)+',"> " &MIN('+Alphabets[i]+'2'+':'+Alphabets[i]+str(RowNUM-1)+'))')
        worksheet.write(row+6, col, '=COUNTIF('+Alphabets[i]+'2'+':'+Alphabets[i]+str(RowNUM-1)+',MIN('+Alphabets[i]+'2'+':'+Alphabets[i]+str(RowNUM-1)+'))')

        col+=2
        i+=2
        j+=1
    row=1
    k=0
    for w in range(len(StudentNamesist)):
        worksheet.write(row,col,'=SUM('+Alphabets[k]+str(w+2)+':'+Alphabets[k+col-2]+str(w+2)+')')
        row+=1
    row+=1    
    worksheet.write(row, col, '=MAX('+Alphabets[col-1]+'2'+':'+Alphabets[col-1]+str(RowNUM-1)+')')
    worksheet.write(row+1, col, '=AVERAGE('+Alphabets[col-1]+'2'+':'+Alphabets[col-1]+str(RowNUM-1)+')')
    worksheet.write(row+2, col, '=MIN('+Alphabets[col-1]+'2'+':'+Alphabets[col-1]+str(RowNUM-1)+')')
    worksheet.write(row+3, col, '=COUNTIF('+Alphabets[col-1]+'2'+':'+Alphabets[col-1]+str(RowNUM-1)+',MAX('+Alphabets[col-1]+'2'+':'+Alphabets[col-1]+str(RowNUM-1)+'))')
    worksheet.write(row+4, col, '=COUNTIFS('+Alphabets[col-1]+'2'+':'+Alphabets[col-1]+str(RowNUM-1)+',">= " &AVERAGE('+Alphabets[col-1]+'2'+':'+Alphabets[col-1]+str(RowNUM-1)+'),'+Alphabets[col-1]+'2'+':'+Alphabets[col-1]+str(RowNUM-1)+',"< " &MAX('+Alphabets[col-1]+'2'+':'+Alphabets[col-1]+str(RowNUM-1)+'))')
    worksheet.write(row+5, col, '=COUNTIFS('+Alphabets[col-1]+'2'+':'+Alphabets[col-1]+str(RowNUM-1)+',"< " &AVERAGE('+Alphabets[col-1]+'2'+':'+Alphabets[col-1]+str(RowNUM-1)+'),'+Alphabets[col-1]+'2'+':'+Alphabets[col-1]+str(RowNUM-1)+',"> " &MIN('+Alphabets[col-1]+'2'+':'+Alphabets[col-1]+str(RowNUM-1)+'))')
    worksheet.write(row+6, col, '=COUNTIF('+Alphabets[col-1]+'2'+':'+Alphabets[col-1]+str(RowNUM-1)+',MIN('+Alphabets[col-1]+'2'+':'+Alphabets[col-1]+str(RowNUM-1)+'))')
    chart.add_series({
        'categories': '=Sheet1!$A$'+str(RowNUM+4)+':$A$'+str(RowNUM+7),
        'values':     '=Sheet1!$'+Alphabets[col-1]+'$'+str(RowNUM+4)+':$'+Alphabets[col-1]+'$'+str(RowNUM+7),
        'points': [
            {'fill': {'color': 'green'}},
            {'fill': {'color': 'blue'}},
            {'fill': {'color': 'yellow'}},
            {'fill': {'color': 'red'}},
        ],
    })
    worksheet.insert_chart(Alphabets[col+1]+'2',chart)
        
def Autofit(workbook):
    
    workbook.close()
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    wb = excel.Workbooks.Open(r'C:\Users\Wael Ashraf\Documents\GitHub\GP_ESAE\StudentGrades.xlsx')
    ws = wb.Worksheets("Sheet1")
    ws.Columns.AutoFit()
    wb.Save()
    excel.Application.Quit()
    
 # Write a total using a formula.
#worksheet.write(row, 0, 'Total',       bold)
#worksheet.write(row, 1, '=SUM(B2:B5)')

def GenExcel(ModelGrades, StudentNamesist, StudentGrades, ExamTitle):
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(ExamTitle+'.xlsx')
    worksheet = workbook.add_worksheet()
    chart =workbook.add_chart({'type': 'pie'})
    
    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': True})

    WriteHeaders(ModelGrades, worksheet, bold)
    RowNUM=WriteStudentNames(StudentNamesist, worksheet, bold)
    WriteGrades(StudentGrades, RowNUM, worksheet, chart, StudentNamesist)
    Autofit(workbook)
    return 'Finished generating the excel sheet successfully'
