import flask
import tensorflow as tf
from tensorflow.keras.models import load_model
import tensorflow.keras.backend as be
import string
import numpy as np
import pickle
import json
import Evaluator_Integrated as Evaluate
import Database as database

#app=flask.Flask("__main__")
app=database.app


conte=""
start=0
model=""

@app.route("/")
def my_index():
    return flask.render_template("index.html",token="Hello Flask+React (GP ESAE)")

@app.route("/model/<string:question>")
def answerModel(question):
    global start
    global model
    global conte
    print("question:",question," context:",conte)
    if start==0:
        model = load_model("D:\\Anime\\Faculty Of Engineering\\GP\\Project\\DModel15")
        start=1
    # print("loaded")
    userQuestion=[question]
    userContext = [conte]

    QWE,CWE,QCE,CCE = InputPreprocess(userQuestion,userContext)
    p=model.predict([QWE,CWE,QCE,CCE ])
    answer = OutputProcess(p,userContext[0])
    return {'ans': answer}  


@app.route("/context/<string:cont>")
def getContext(cont):
    print(cont)
    global conte
    conte = cont
    return {'context':conte}

# @app.route("/complete/<string:question1>/<string:question2>")
# def answerModelcomplete(question1,question2):
#     answer=EvaluateAns(question1,question2)#student ans, model ans
#     return {'ans': answer}

@app.route("/habal/<string:cont1>/<string:cont2>/<string:cont3>/<string:cont4>")
def getContext1(cont1,cont2,cont3,cont4):
    return {'TFReturn':cont3}

@app.route("/ViewExams/<InstructorID>")
def ViewExams(InstructorID): 
    ExamList = database.GetExamByInstructorID(InstructorID)
    return { 'ans':ExamList }

@app.route("/AddMCQ/<ExamTitle>/<InstructorID>/<Question>/<Answers>/<CorrectAns>/<Grade>/<ILO>")
def AddMCQ(ExamTitle,InstructorID,Question,Answers,CorrectAns,Grade,ILO):
    IloReturn = database.AddILOIfNotExist(ILO, InstructorID)
    #print(IloReturn)
    Exam = database.CreateExamIfNotExist(ExamTitle,InstructorID)
    MCQReturn=1
    if (Exam=='ExamFound' or Exam=='Exam is added successfully'):
        question = database.AddMCQ(Question, Answers, CorrectAns, Grade, ILO, ExamTitle, InstructorID)
        if (question == 'MCQ question is added successfully'):
            MCQReturn = question
        elif (question == 'There was an issue adding mcq'):
            MCQReturn = question
        elif (question=='Question already exists in the exam'):
            MCQReturn = question
    elif (Exam=='There was an issue creating the exam'):
        MCQReturn = Exam
    return {'MCQReturn':MCQReturn}

@app.route("/UpdateMCQ/<OldQuestion>/<NewQuestion>/<NewAnswers>/<NewCorrectAns>/<ExamTitle>/<NewILO>/<NewGrade>/<InstructorID>")
def UpdateMCQ(OldQuestion,NewQuestion, NewAnswers, NewCorrectAns, ExamTitle, NewILO, NewGrade, InstructorID):
    ISupdated = database.UpdateMCQ(OldQuestion,NewQuestion, NewAnswers, NewCorrectAns, ExamTitle, NewILO, NewGrade, InstructorID)
    return {'Updated':ISupdated} 

@app.route("/AddComplete/<string:ExamTitle>/<int:InstructorID>/<Question1>/<Question2>/<CorrectAns>/<Grade>/<ILO>")
def AddComplete(ExamTitle,InstructorID,Question1,Question2,CorrectAns,Grade,ILO):
    IloReturn = database.AddILOIfNotExist(ILO, InstructorID)
    #print(IloReturn)
    Question = str(Question1) + '/' + str(Question2)
    Exam = database.CreateExamIfNotExist(ExamTitle,InstructorID)
    CompleteReturn=1
    if (Exam=='ExamFound' or Exam=='Exam is added successfully'):
        question = database.AddComplete(Question, CorrectAns, Grade, ILO, ExamTitle, InstructorID)
        if (question == 'Complete question is added successfully'):
            CompleteReturn = question
        elif (question == 'There was an issue adding complete question'):
            CompleteReturn = question
        elif (question=='Question already exists in the exam'):
            CompleteReturn = question
    elif (Exam=='There was an issue creating the exam'):
        CompleteReturn = Exam
    return {'CompleteReturn':CompleteReturn}

@app.route("/UpdateComplete/<OldQuestion>/<NewQuestion1>/<NewQuestion2>/<NewCorrectAns>/<ExamTitle>/<NewILO>/<NewGrade>/<InstructorID>")
def UpdateComplete(OldQuestion,NewQuestion1, NewQuestion2, NewCorrectAns, ExamTitle, NewILO, NewGrade, InstructorID):
    ques = OldQuestion.split("......")
    MyQuestion = ques[0]+'/'+ques[1]
    ISupdated = database.UpdateComplete(MyQuestion,NewQuestion1+'/'+NewQuestion2, 
    NewCorrectAns, ExamTitle, NewILO, NewGrade, InstructorID)
    return {'Updated':ISupdated}

@app.route("/AddTrueFalse/<string:ExamTitle>/<int:InstructorID>/<string:Question>/<string:CorrectAns>/<int:Grade>/<string:ILO>")
def AddTrueFalse(ExamTitle,InstructorID,Question,CorrectAns,Grade,ILO):
    IloReturn = database.AddILOIfNotExist(ILO, InstructorID)
    #print(IloReturn)
    Exam = database.CreateExamIfNotExist(ExamTitle,InstructorID)
    TFReturn=1
    #print(TFReturn)
    if (Exam=='ExamFound' or Exam=='Exam is added successfully'):
        question = database.AddTrueFalse(Question, CorrectAns, Grade, ILO, ExamTitle, InstructorID)
        if (question == 'T&F question is added successfully'):
            TFReturn = question
        elif (question == 'There was an issue adding T&F question'):
            TFReturn = question
        elif (question=='Question already exists in the exam'):
            TFReturn = question
    elif (question=='There was an issue creating the exam'):
        TFReturn = question
    return {'TFReturn':TFReturn}

@app.route("/UpdateTrueFalse/<OldQuestion>/<NewQuestion>/<NewCorrectAns>/<ExamTitle>/<NewILO>/<NewGrade>/<InstructorID>")
def UpdateTrueFalse(OldQuestion,NewQuestion, NewCorrectAns, ExamTitle, NewILO, NewGrade, InstructorID):
    ISupdated = database.UpdateTrueFalse(OldQuestion,NewQuestion, NewCorrectAns, ExamTitle, NewILO, NewGrade, InstructorID)
    return {'Updated':ISupdated} 

@app.route("/AddEssay/<string:ExamTitle>/<int:InstructorID>/<string:Question>/<string:CorrectAns>/<Grade>/<ILO>")
def AddEssay(ExamTitle,InstructorID,Question,CorrectAns,Grade,ILO):
    IloReturn = database.AddILOIfNotExist(ILO, InstructorID)
    #print(IloReturn)
    Exam = database.CreateExamIfNotExist(ExamTitle,InstructorID)
    EssayReturn=1
    if (Exam=='ExamFound' or Exam=='Exam is added successfully'):
        question = database.AddEssay(Question, CorrectAns, Grade, ILO, ExamTitle, InstructorID)
        if (question == 'Essay question is added successfully'):
            EssayReturn = question
        elif (question == 'There was an issue adding essay question'):
            EssayReturn = question
        elif (question=='Question already exists in the exam'):
            EssayReturn = question
    elif (Exam=='There was an issue creating the exam'):
        EssayReturn = Exam
    return {'EssayReturn':EssayReturn}

#AddEssay('OOP',1,'What is OOPS?','OOPS is abbreviated as Object Oriented Programming system',3,'OOP concepts')

@app.route("/UpdateEssay/<OldQuestion>/<NewQuestion>/<NewCorrectAns>/<ExamTitle>/<NewILO>/<NewGrade>/<InstructorID>")
def UpdateEssay(OldQuestion,NewQuestion, NewCorrectAns, ExamTitle, NewILO, NewGrade, InstructorID):
    ISupdated = database.UpdateEssay(OldQuestion,NewQuestion, NewCorrectAns, ExamTitle, NewILO, NewGrade, InstructorID)
    return {'Updated':ISupdated} 

@app.route("/MixQuestion/<ExamTitle>/<InstructorID>/<QuestionType>/<ILO>/<int:Number>")
def MixQuestion(ExamTitle, InstructorID, QuestionType, ILO, Number):
    Mixed = 0
    if (QuestionType == 'MCQ'):
        Mixed = database.MixMCQ(ExamTitle, InstructorID, ILO, Number)

    elif (QuestionType == 'Complete'):
        Mixed = database.MixComplete(ExamTitle, InstructorID, ILO, Number)

    elif (QuestionType == 'T and F'):
        Mixed = database.MixTF(ExamTitle, InstructorID, ILO, Number)

    elif (QuestionType == 'Essay'):
        Mixed = database.MixEssay(ExamTitle, InstructorID, ILO, Number)

    return {'MixQues':Mixed}

@app.route("/GetILO/<InstructorID>")
def GetILO(InstructorID):
    ILOs = database.GetILO(InstructorID)
    #print(ILOs)
    return {'ILO_List':ILOs}

@app.route("/GetMCQ/<ExamTitle>/<InstructorID>")
def GetMCQ(ExamTitle, InstructorID): #Get All MCQ Questions
    QuestionList, CounterList, AnswerList, CorrectAnswerList, ILOList, GradeList = database.GetMCQ(ExamTitle, InstructorID)
    return {'QuestionList':QuestionList, 'CounterList':CounterList, 'AnswerList':AnswerList,
    'CorrectAnswerList':CorrectAnswerList, 'ILOList':ILOList, 'GradeList':GradeList}

@app.route("/GetComplete/<ExamTitle>/<InstructorID>")
def GetComplete(ExamTitle, InstructorID): 
    QuestionList, CorrectAnswerList, ILOList, GradeList = database.GetComplete(ExamTitle, InstructorID)
    return {'QuestionList':QuestionList, 'CorrectAnswerList':CorrectAnswerList,
    'ILOList':ILOList, 'GradeList':GradeList}

@app.route("/GetTF/<ExamTitle>/<InstructorID>")
def GetTF(ExamTitle, InstructorID):
    QuestionList, CorrectAnswerList, ILOList, GradeList = database.GetTF(ExamTitle, InstructorID)
    return {'QuestionList':QuestionList, 'CorrectAnswerList':CorrectAnswerList, 'ILOList':ILOList, 'GradeList':GradeList}

@app.route("/GetEssay/<ExamTitle>/<InstructorID>")
def GetEssay(ExamTitle, InstructorID):
    QuestionList, CorrectAnswerList, ILOList, GradeList = database.GetEssay(ExamTitle, InstructorID)
    return {'QuestionList':QuestionList, 'CorrectAnswerList':CorrectAnswerList, 'ILOList':ILOList, 'GradeList':GradeList}

@app.route("/GetAMCQ/<ExamTitle>/<InstructorID>/<Question>")
def GetAMCQ(ExamTitle, InstructorID, Question):
    Question, AnswerList, CorrectAnswer, ILO,  Grade = database.GetAMCQ(ExamTitle, InstructorID, Question)
    return {'Question':Question, 'OneAnswerList':AnswerList, 'CorrectAnswer':CorrectAnswer, 'ILO':ILO, 'Grade':Grade}

@app.route("/GetACompleteQues/<ExamTitle>/<InstructorID>/<Question>")
def GetACompleteQues(ExamTitle, InstructorID, Question):
    Question1, Question2, CorrectAnswer, ILO,  Grade = database.GetACompleteQues(ExamTitle, InstructorID, Question)
    return {'Question1':Question1, 'Question2':Question2, 'CorrectAnswer':CorrectAnswer,
    'ILO':ILO, 'Grade':Grade}

@app.route("/GetATrueFalseQues/<ExamTitle>/<InstructorID>/<Question>")
def GetATrueFalseQues(ExamTitle, InstructorID, Question):
    Question, CorrectAnswer, ILO,  Grade = database.GetATrueFalseQues(ExamTitle, InstructorID, Question)
    return {'Question':Question, 'CorrectAnswer':CorrectAnswer, 'ILO':ILO, 'Grade':Grade}

@app.route("/GetAEssQues/<ExamTitle>/<InstructorID>/<string:Question>")
def GetAEssQues(ExamTitle, InstructorID, Question):
    Question, CorrectAnswer, ILO,  Grade = database.GetAEssQues(ExamTitle, InstructorID, str(Question))
    return {'Question':Question, 'CorrectAnswer':CorrectAnswer, 'ILO':ILO, 'Grade':Grade}

@app.route("/SubmitStudentExam/<ExamTitle>/<StudentID>/<MCQList>/<MCQAnswers>/<CompleteList>/<CompleteAnswers>/<TFList>/<TFAnswers>/<EssayList>/<EssayAnswers>")
def SubmitStudentExam(ExamTitle, StudentID, MCQList, MCQAnswers, 
        CompleteList, CompleteAnswers, TFList, TFAnswers, EssayList, EssayAnswers):
    Is_successfull = 0

    MCQList1=MCQList.split(',')
    MCQAnswers1=MCQAnswers.split(',')
    if (MCQList1):
        for question,answer in zip(MCQList1, MCQAnswers1):
            Is_successfull = database.StudentSubmitMCQ(ExamTitle, StudentID, question, answer)
            #print(Is_successfull)
            if (Is_successfull == 'There was an issue adding mcq answer'):
                return {'successful':Is_successfull}
    
    CompleteList1=CompleteList.split(',')
    CompleteAnswers1=CompleteAnswers.split(',')
    if (CompleteList1):
        for question,answer in zip(CompleteList1, CompleteAnswers1):
            ques = question.split("......")
            MyQuestion = ques[0]+'/'+ques[1]
            Is_successfull = database.StudentSubmitComplete(ExamTitle, StudentID, MyQuestion, answer)
            #print(Is_successfull)
            if (Is_successfull == 'There was an issue adding Complete answer'):
                return {'successful':Is_successfull}
    
    TFList1=TFList.split(',')
    TFAnswers1=TFAnswers.split(',')
    if (TFList1):
        for question,answer in zip(TFList1, TFAnswers1):
            Is_successfull = database.StudentSubmitTF(ExamTitle, StudentID, question, answer)
            #print(Is_successfull)
            if (Is_successfull == 'There was an issue adding TF answer'):
                return {'successful':Is_successfull}
    
    EssayList1=EssayList.split(',')
    EssayAnswers1=EssayAnswers.split(',')
    if (EssayList1):
        for question,answer in zip(EssayList1, EssayAnswers1):
            Is_successfull = database.StudentSubmitEssay(ExamTitle, StudentID, question, answer)
            #print(Is_successfull)
            if (Is_successfull == 'There was an issue adding Essay answer'):
                return {'successful':Is_successfull}
    
    Is_successfull = 'Exam is submitted'
    print(Is_successfull)
    return {'successful':Is_successfull}
        
@app.route("/DeleteExam/<ExamTitle>")
def DeleteExam(ExamTitle):
    Deleted = database.DeleteExam(ExamTitle)
    return {'Deleted':Deleted}

@app.route("/DeleteMCQ/<ExamTitle>/<Question>")
def DeleteMCQ(ExamTitle, Question):
    Deleted = database.DeleteMCQ(ExamTitle, Question)
    print(Deleted)
    return {'Deleted':Deleted}

@app.route("/DeleteComplete/<ExamTitle>/<Question>")
def DeleteComplete(ExamTitle, Question):
    ques = Question.split("......")
    MyQuestion = ques[0]+'/'+ques[1]
    Deleted = database.DeleteComplete(ExamTitle, MyQuestion)
    print(Deleted)
    return {'Deleted':Deleted}

@app.route("/DeleteTF/<ExamTitle>/<Question>")
def DeleteTF(ExamTitle, Question):
    Deleted = database.DeleteTF(ExamTitle, Question)
    print(Deleted)
    return {'Deleted':Deleted}

@app.route("/DeleteEssay/<ExamTitle>/<Question>")
def DeleteEssay(ExamTitle, Question):
    Deleted = database.DeleteEssay(ExamTitle, Question)
    print(Deleted)
    return {'Deleted':Deleted}

#CHECK IF I NEED THE INSTRUCTOR ID LATER
@app.route("/GradeExam/<ExamTitle>")
def GradeExam(ExamTitle):
    A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T = database.GetExamToEvaluate(ExamTitle)
    MCQQuestionList   = A
    MCQModelAnswer    = B
    MCQGrade          = C
    MCQAnswerList     = D
    MCQStudentIDList  = E

    CompQuestionList  = F
    CompModelAnswer   = G
    CompGrade         = H
    CompAnswerList    = I
    CompStudentIDList = J

    TFQuestionList    = K
    TFModelAnswer     = L
    TFGrade           = M
    TFAnswerList      = N
    TFStudentIDList   = O

    EssQuestionList   = P
    EssModelAnswer    = Q
    EssGrade          = R
    EssAnswerList     = S
    EssStudentIDList  = T
    
    #Call here the function from evaluator.py to grade the exam
    MCQGradeEvaluated = 0
    CompGradeEvaluated = 0
    TFGradeEvaluated = 0
    EssGradeEvaluated = 0
    if (MCQAnswerList):
        MCQGradeEvaluated  = Evaluate.Evaluator("MCQ",MCQStudentIDList,MCQAnswerList,MCQModelAnswer,MCQGrade)
    if (CompAnswerList):
        CompGradeEvaluated = Evaluate.Evaluator("Complete",CompStudentIDList,CompAnswerList,CompModelAnswer,CompGrade)
    if (TFAnswerList):
        TFGradeEvaluated   = Evaluate.Evaluator("TF",TFStudentIDList,TFAnswerList,TFModelAnswer,TFGrade)
    if (EssAnswerList):
        EssGradeEvaluated  = Evaluate.Evaluator("Essay",EssStudentIDList,EssAnswerList,EssModelAnswer,EssGrade)

    MCQQuestionList   = ['MCQ 1', 'MCQ2', 'MCQ3']
    MCQModelAnswer    = ['Model Ans 1', 'Model Ans 2', 'Model Ans 3']
    MCQGrade          = [3, 4, 2]
    MCQAnswerList     = [['Student 1 ans MCQ1', 'Student 2 ans MCQ1', 'Student 3 ans MCQ1'],
                         ['Student 1 ans MCQ2', 'Student 2 ans MCQ2', 'Student 3 ans MCQ2'],
                         ['Student 1 ans MCQ3', 'Student 2 ans MCQ3', 'Student 3 ans MCQ3']] #assuming for example 3 students
    MCQStudentIDList  = [[1,2,3],[1,2,3],[1,2,3]] #assuming for example 3 students

    Grade = 0
    return {'Grade':Grade}


app.run(debug=True)