import xlsxwriter
import pythoncom
import win32com.client as win32
import os



# ModelGrades=[10,10,10,10]
# StudentNamesist=["Amin Ghassan","Ismael Hossam","Omar Yousry","Wael Ashraf"]
# StudentGrades =[[9,9,8,9],[10,9,8,7],[8,9,7,10],[7,6,5,9]]


def WriteHeaders(ModelGrades, worksheet, bold,QuesntiosLen):
    Alphabets=["B1","C1","D1","E1","F1","G1","H1","I1","J1","K1","L1","M1","N1","O1","P1","Q1","W1","X1","Y1","Z1","AA1",
    "AB1","AC1","AD1","AE1","AF1","AG1","AH1","AI1","AJ1","AK1","AL1","AM1","AN1","AO1","AP1","AQ1","AR1","AS1","AT1","AU1",
    "AV1","AW1","AX1","AY1","AZ1"]
    Qtype=[]
    EssayCols=[]
    if QuesntiosLen[0]!=0:
        for MCQ in range(QuesntiosLen[0]):
            Qtype.append("MCQ")
    if QuesntiosLen[1]!=0:
        for TF in range(QuesntiosLen[1]):
            Qtype.append("T&F Q")    
    if QuesntiosLen[2]!=0:
        for Comp in range(QuesntiosLen[2]):
            Qtype.append("Complete Q")   
    if QuesntiosLen[3]!=0:
        column=len(Qtype)*2
        for Ess in range(QuesntiosLen[3]):
            column+=2
            EssayCols.append(column)
            Qtype.append("Essay Q")        
    j=0
    worksheet.write('A1', 'Name', bold)
    for i in range(len(ModelGrades)):
        worksheet.write(Alphabets[j], Qtype[i]+str(i+1)+'('+str(ModelGrades[i])+')', bold)
        worksheet.write(Alphabets[j+1], Qtype[i]+str(i+1)+' Comment', bold)
        j+=2
    worksheet.write(Alphabets[j], 'Total Grade'+'('+str(sum(ModelGrades))+')', bold)
    return EssayCols

def WriteStudentNames(StudentNamesist, worksheet, bold,ILOFeedback):
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
    worksheet.write(row+8,col,"Questions Comments",bold)
    
    row_ilo=row+10
    worksheet.write(row_ilo,col,"ILO(s)",bold)
    worksheet.write(row_ilo,col+1,"Description",bold)
    worksheet.write(row_ilo,col+2,"Coverage (%)",bold)
    row_ilo+=1
    i=1
    for key in ILOFeedback:
        worksheet.write(row_ilo,col,"ILO_"+str(i))
        worksheet.write(row_ilo,col+1,key)
        worksheet.write(row_ilo,col+2,ILOFeedback[key])
        i+=1
        row_ilo+=1
    return row
     
def WriteGrades(StudentGrades, RowNUM, worksheet, chart, StudentNamesist,QuestionsComments,EssayComments,EssayCols):
    Alphabets=["B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","W","X","Y","Z","AA",
    "AB","AC","AD","AE","AF","AG","AH","AI","AJ","AK","AL","AM","AN","AO","AP","AQ","AR","AS","AT","AU",
    "AV","AW","AX","AY","AZ"]
    row = 1
    col = 1
    col_comm=2
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
        worksheet.write(row+8, col_comm, QuestionsComments[j])
        col+=2
        col_comm+=2
        i+=2
        j+=1
    row_ess=1
    for essay,col_ess in zip(EssayComments,EssayCols):
        for comment in essay:
            worksheet.write(row_ess,col_ess,comment)
            row_ess+=1    
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
        
def Autofit(ExamTitle):
    pythoncom.CoInitialize()
    fileDir = os.path.dirname(os.path.realpath('__file__'));
    filename = os.path.join(fileDir,ExamTitle+'.xlsx')
    print(filename)
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    wb = excel.Workbooks.Open(filename)
    ws = wb.Worksheets("Sheet1")
    ws.Columns.AutoFit()
    wb.Save()
    excel.Application.Quit()
    
    
 # Write a total using a formula.
#worksheet.write(row, 0, 'Total',       bold)
#worksheet.write(row, 1, '=SUM(B2:B5)')

def GenExcel(ModelGrades, StudentNamesist, StudentGrades, ExamTitle,QuesntiosLen,QuestionsComments,ILOFeedback,EssayComments):
    # Create a workbook and add a worksheet.
    #path = "C:\\Users\\Wael Ashraf\\Documents\\GitHub\\GP_ESAE\\" 
    fileDir = os.path.dirname(os.path.realpath('__file__'));
    filename = os.path.join(fileDir,ExamTitle+'.xlsx')
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    chart =workbook.add_chart({'type': 'pie'})
    
    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': True})

    EssayCols=WriteHeaders(ModelGrades, worksheet, bold,QuesntiosLen)
    RowNUM=WriteStudentNames(StudentNamesist, worksheet, bold,ILOFeedback)
    WriteGrades(StudentGrades, RowNUM, worksheet, chart, StudentNamesist,QuestionsComments,EssayComments,EssayCols)
    workbook.close()
    Autofit(ExamTitle)
    return 'Finished generating the excel sheet successfully'

# ModelGrades=[10,10,10,10]
# StudentNamesist=["Amin Ghassan","Ismael Hossam","Omar Youssry","Wael Ashraf"]
# StudentGrades =[[9,9,8,9],[10,9,8,7],[8,9,7,10],[10,8,8,9]]
# ExamTitle="Midterm Data Structures 2016"
# QuesntiosLen=[1,1,1,1]
# QuestionsComments=["Q1 Comment","Q2 Comment","Q3 Comment","Q4 Comment"]
# ILOFeedback={'ILO1 Desc': 'ILO1 80%', 'ILO2 Desc': 'ILO2 70%'}
# EssayComments=[["Gamed ya Amin","Gamed ya Ismael","Gamed ya Omar","Gamed ya Wael"]]

# ModelGrades=[1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 2, 1, 1, 1, 2, 2, 1, 1, 2, 2, 2, 2, 2, 4, 4, 2, 3, 5, 4, 5]
# StudentNamesist=['omar']
# StudentGrades = [[1], [1], [0], [1], [1], [2], [1], [1], [0], [0], [2], [0], [0], [1], [0], [2], [1], [0], [0], [2], [0], [0], [0], [2.4], [2.4], [1.2], [1.7999999999999998], [3.0], [2.4], [3.0]]
# ExamTitle='Programming Techniques final S2019'
# QuesntiosLen=[10,8,5,7]
# QuestionsComments=
# ILOFeedback=
# EssayComments=
# GenExcel(ModelGrades, StudentNamesist, StudentGrades, ExamTitle,QuesntiosLen,QuestionsComments,ILOFeedback,EssayComments)
#Autofit("Midterm Data Structures 2016")