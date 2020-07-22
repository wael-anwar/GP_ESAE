import flask
import tensorflow as tf
from tensorflow.keras.models import load_model
import tensorflow.keras.backend as be
import string
import numpy as np
import pickle
import json
#import Evaluator_Integrated as Evaluate
import Database as database
import Evaluator_Integrated as Evaluate
import GenerateExcelSheet as genX
import collections

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

@app.route("/SignUpStudentInstructor/<Identity>/<UserName>/<Name>/<Password>")
def SignUpStudentInstructor(Identity,UserName, Name, Password): 
    SignUp = 0
    if (Identity == "student"):
        SignUp = database.StudentSignUp(UserName, Name, Password)
    elif (Identity == "instructor"):
        SignUp = database.InstructorSignUp(UserName, Name, Password)

    return { 'SignUp':SignUp }

@app.route("/SignInStudentInstructor/<Identity>/<UserName>/<Password>")
def SignInStudentInstructor(Identity, UserName, Password): 
    SignIn = 0
    ID=0
    if (Identity == "student"):
        SignIn,ID = database.StudentSignIn(UserName,Password)
        return {'SignIn':SignIn}
    elif (Identity == "instructor"):
        SignIn,ID = database.InstructorSignIn(UserName,Password)
        return {'SignIn':SignIn, 'ID':ID}

@app.route("/ViewExams/<int:InstructorID>")
def ViewExams(InstructorID): 
    ExamList = database.GetExamByInstructorID(InstructorID)
    return { 'ans':ExamList }

@app.route("/ViewAllExams/<int:StudentID>")
def ViewAllExams(StudentID): 
    ExamList = database.GetAllExams(StudentID)
    return { 'ans':ExamList }

@app.route("/AddMCQ/<ExamTitle>/<int:InstructorID>/<Question>/<Answers>/<CorrectAns>/<Grade>/<ILO>")
def AddMCQ(ExamTitle,InstructorID,Question,Answers,CorrectAns,Grade,ILO):
    IloReturn = database.AddILOIfNotExist(ILO, InstructorID)
    #print(IloReturn)
    Exam = database.CreateExamIfNotExist(ExamTitle,InstructorID)
    MCQReturn=1
    if (Exam=='ExamFound' or Exam=='Exam is added successfully'):
        question = database.AddMCQ(Question, Answers, CorrectAns, Grade, ILO, ExamTitle, InstructorID)
        if (question == 'MCQ question is added successfully'):
            MCQReturn = 'Question is added successfully'
        elif (question == 'There was an issue adding mcq'):
            MCQReturn = 'There was an issue adding question'
        elif (question=='Question already exists in the exam'):
            MCQReturn = question
    elif (Exam=='There was an issue creating the exam'):
        MCQReturn = Exam
    return {'MCQReturn':MCQReturn}

@app.route("/UpdateMCQ/<OldQuestion>/<NewQuestion>/<NewAnswers>/<NewCorrectAns>/<ExamTitle>/<NewILO>/<NewGrade>/<int:InstructorID>")
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
            CompleteReturn = 'Question is added successfully'
        elif (question == 'There was an issue adding complete question'):
            CompleteReturn = 'There was an issue adding question'
        elif (question=='Question already exists in the exam'):
            CompleteReturn = question
    elif (Exam=='There was an issue creating the exam'):
        CompleteReturn = Exam
    return {'CompleteReturn':CompleteReturn}

@app.route("/UpdateComplete/<OldQuestion>/<NewQuestion1>/<NewQuestion2>/<NewCorrectAns>/<ExamTitle>/<NewILO>/<NewGrade>/<int:InstructorID>")
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
            TFReturn = 'Question is added successfully'
        elif (question == 'There was an issue adding T&F question'):
            TFReturn = 'There was an issue adding question'
        elif (question=='Question already exists in the exam'):
            TFReturn = question
    elif (question=='There was an issue creating the exam'):
        TFReturn = question
    return {'TFReturn':TFReturn}

@app.route("/UpdateTrueFalse/<OldQuestion>/<NewQuestion>/<NewCorrectAns>/<ExamTitle>/<NewILO>/<NewGrade>/<int:InstructorID>")
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
            EssayReturn = 'Question is added successfully'
        elif (question == 'There was an issue adding essay question'):
            EssayReturn = 'There was an issue adding question'
        elif (question=='Question already exists in the exam'):
            EssayReturn = question
    elif (Exam=='There was an issue creating the exam'):
        EssayReturn = Exam
    return {'EssayReturn':EssayReturn}

@app.route("/UpdateEssay/<OldQuestion>/<NewQuestion>/<NewCorrectAns>/<ExamTitle>/<NewILO>/<NewGrade>/<int:InstructorID>")
def UpdateEssay(OldQuestion,NewQuestion, NewCorrectAns, ExamTitle, NewILO, NewGrade, InstructorID):
    ISupdated = database.UpdateEssay(OldQuestion,NewQuestion, NewCorrectAns, ExamTitle, NewILO, NewGrade, InstructorID)
    return {'Updated':ISupdated} 

@app.route("/MixQuestion/<ExamTitle>/<int:InstructorID>/<QuestionType>/<ILO>/<int:Number>")
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

@app.route("/GetILO/<int:InstructorID>")
def GetILO(InstructorID):
    ILOs = database.GetILO(InstructorID)
    #print(ILOs)
    return {'ILO_List':ILOs}

@app.route("/GetMCQ/<ExamTitle>/<int:InstructorID>")
def GetMCQ(ExamTitle, InstructorID): #Get All MCQ Questions
    QuestionList, CounterList, AnswerList, CorrectAnswerList, ILOList, GradeList = database.GetMCQ(ExamTitle, InstructorID)
    return {'QuestionList':QuestionList, 'CounterList':CounterList, 'AnswerList':AnswerList,
    'CorrectAnswerList':CorrectAnswerList, 'ILOList':ILOList, 'GradeList':GradeList}

@app.route("/GetComplete/<ExamTitle>/<int:InstructorID>")
def GetComplete(ExamTitle, InstructorID): 
    QuestionList, CorrectAnswerList, ILOList, GradeList = database.GetComplete(ExamTitle, InstructorID)
    return {'QuestionList':QuestionList, 'CorrectAnswerList':CorrectAnswerList,
    'ILOList':ILOList, 'GradeList':GradeList}

@app.route("/GetTF/<ExamTitle>/<int:InstructorID>")
def GetTF(ExamTitle, InstructorID):
    QuestionList, CorrectAnswerList, ILOList, GradeList = database.GetTF(ExamTitle, InstructorID)
    return {'QuestionList':QuestionList, 'CorrectAnswerList':CorrectAnswerList, 'ILOList':ILOList, 'GradeList':GradeList}

@app.route("/GetEssay/<ExamTitle>/<int:InstructorID>")
def GetEssay(ExamTitle, InstructorID):
    QuestionList, CorrectAnswerList, ILOList, GradeList = database.GetEssay(ExamTitle, InstructorID)
    return {'QuestionList':QuestionList, 'CorrectAnswerList':CorrectAnswerList, 'ILOList':ILOList, 'GradeList':GradeList}

@app.route("/GetMCQStud/<ExamTitle>")
def GetMCQStud(ExamTitle): #Get All MCQ Questions
    QuestionList, CounterList, AnswerList, CorrectAnswerList, ILOList, GradeList = database.GetMCQ(ExamTitle,0)
    return {'QuestionList':QuestionList, 'CounterList':CounterList, 'AnswerList':AnswerList,
    'CorrectAnswerList':CorrectAnswerList, 'ILOList':ILOList, 'GradeList':GradeList}

@app.route("/GetCompleteStud/<ExamTitle>")
def GetCompleteStud(ExamTitle): 
    QuestionList, CorrectAnswerList, ILOList, GradeList = database.GetComplete(ExamTitle,0)
    return {'QuestionList':QuestionList, 'CorrectAnswerList':CorrectAnswerList,
    'ILOList':ILOList, 'GradeList':GradeList}

@app.route("/GetTFStud/<ExamTitle>")
def GetTFStud(ExamTitle):
    QuestionList, CorrectAnswerList, ILOList, GradeList = database.GetTF(ExamTitle,0)
    return {'QuestionList':QuestionList, 'CorrectAnswerList':CorrectAnswerList, 'ILOList':ILOList, 'GradeList':GradeList}

@app.route("/GetEssayStud/<ExamTitle>")
def GetEssayStud(ExamTitle):
    QuestionList, CorrectAnswerList, ILOList, GradeList = database.GetEssay(ExamTitle,0)
    return {'QuestionList':QuestionList, 'CorrectAnswerList':CorrectAnswerList, 'ILOList':ILOList, 'GradeList':GradeList}

@app.route("/GetAMCQ/<ExamTitle>/<int:InstructorID>/<Question>")
def GetAMCQ(ExamTitle, InstructorID, Question):
    Question, AnswerList, CorrectAnswer, ILO,  Grade = database.GetAMCQ(ExamTitle, InstructorID, Question)
    return {'Question':Question, 'AnswerList':AnswerList, 'CorrectAnswer':CorrectAnswer, 'ILO':ILO, 'Grade':Grade}

@app.route("/GetACompleteQues/<ExamTitle>/<int:InstructorID>/<Question>")
def GetACompleteQues(ExamTitle, InstructorID, Question):
    Question1, Question2, CorrectAnswer, ILO,  Grade = database.GetACompleteQues(ExamTitle, InstructorID, Question)
    return {'Question1':Question1, 'Question2':Question2, 'CorrectAnswer':CorrectAnswer,
    'ILO':ILO, 'Grade':Grade}

@app.route("/GetATrueFalseQues/<ExamTitle>/<int:InstructorID>/<Question>")
def GetATrueFalseQues(ExamTitle, InstructorID, Question):
    Question, CorrectAnswer, ILO,  Grade = database.GetATrueFalseQues(ExamTitle, InstructorID, Question)
    return {'Question':Question, 'CorrectAnswer':CorrectAnswer, 'ILO':ILO, 'Grade':Grade}

@app.route("/GetAEssQues/<ExamTitle>/<int:InstructorID>/<string:Question>")
def GetAEssQues(ExamTitle, InstructorID, Question):
    Question, CorrectAnswer, ILO,  Grade = database.GetAEssQues(ExamTitle, InstructorID, str(Question))
    return {'Question':Question, 'CorrectAnswer':CorrectAnswer, 'ILO':ILO, 'Grade':Grade}

@app.route("/SubmitStudentExam/<ExamTitle>/<int:StudentID>/<MCQList>/<MCQAnswers>/<CompleteList>/<CompleteAnswers>/<TFList>/<TFAnswers>/<EssayList>/<EssayAnswers>")
def SubmitStudentExam(ExamTitle, StudentID, MCQList, MCQAnswers, 
        CompleteList, CompleteAnswers, TFList, TFAnswers, EssayList, EssayAnswers):
    Is_successfull = 0
    # if (CompleteList!='empty'):
    #     print(1)
    #     print(CompleteList.split(','))
    if (MCQList!='empty'):
        MCQList1=MCQList.split(',')
        MCQAnswers1=MCQAnswers.split(',')
        for question,answer in zip(MCQList1, MCQAnswers1):
            Is_successfull = database.StudentSubmitMCQ(ExamTitle, StudentID, question, answer)
            #print(Is_successfull)
            if (Is_successfull == 'There was an issue adding mcq answer'):
                return {'successful':Is_successfull}
    
    if (CompleteList!='empty'):
        CompleteList1=CompleteList.split(',')
        CompleteAnswers1=CompleteAnswers.split(',')
        for question,answer in zip(CompleteList1, CompleteAnswers1):
            ques = question.split("......")
            MyQuestion = ques[0]+'/'+ques[1]
            Is_successfull = database.StudentSubmitComplete(ExamTitle, StudentID, MyQuestion, answer)
            #print(Is_successfull)
            if (Is_successfull == 'There was an issue adding Complete answer'):
                return {'successful':Is_successfull}
    
    if (TFList!='empty'):
        TFList1=TFList.split(',')
        TFAnswers1=TFAnswers.split(',')
        for question,answer in zip(TFList1, TFAnswers1):
            Is_successfull = database.StudentSubmitTF(ExamTitle, StudentID, question, answer)
            #print(Is_successfull)
            if (Is_successfull == 'There was an issue adding TF answer'):
                return {'successful':Is_successfull}
    
    if (EssayList!='empty'):
        EssayList1=EssayList.split(',')
        EssayAnswers1=EssayAnswers.split(',')
        for question,answer in zip(EssayList1, EssayAnswers1):
            Is_successfull = database.StudentSubmitEssay(ExamTitle, StudentID, question, answer)
            #print(Is_successfull)
            if (Is_successfull == 'There was an issue adding Essay answer'):
                return {'successful':Is_successfull}
    
    Is_successfull = 'Exam is submitted'
    #print(Is_successfull)
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

#MCQ, True and false, Complete .. input shall be binary
def GenerateQuestionFeedback(QuestionListAnswer): #list of list
    FeedbackList = []
    for OneQuesList in QuestionListAnswer:
        ListLength = len(OneQuesList)
        CorrectAnswersCount = OneQuesList.count(1)
        Percentage = float(CorrectAnswersCount) / float(ListLength) * 100
        Percentage = round(Percentage)
        FeedbackList.append(str(Percentage) + ' % of the students were able to answer this question correctly')
    return FeedbackList

def GenerateEssayQuestionsFeedback(QuestionListAnswer): #input is not approximated and it is between 0 and 1
    FeedbackList = []
    for OneQuesList in QuestionListAnswer:
        ListLength = len(OneQuesList)
        # CountPlagiarism = sum(i>=0.95 for i in OneQuesList)
        # if (CountPlagiarism):
        #     FeedbackList.append('Alert, there may be plagiarized answers in this question')
        #     continue
        
        # CountWeakAnswers = sum(i<=0.2 for i in OneQuesList)
        # if (round(CountWeakAnswers/ListLength,2) <= 0.25):
        #     FeedbackList.append('Alert, this question has a lot of humble grades and it may not be explained well.')
        #     continue

        Avg = sum(OneQuesList)/ListLength *100
        Avg = round(Avg)
        FeedbackList.append(str(Avg) + ' % of the students were able to answer this question correctly')

    return FeedbackList

def GenerateEssayAnswerFeedback(QuestionListAnswer):
    FeedbackList = []
    for OneQuesList in QuestionListAnswer:
        OneQuesFeedbackList = []
        for ans1 in OneQuesList:
            ans = round(ans1,2)
            if (ans >= 0.95):
                OneQuesFeedbackList.append('This student has a very high score and may have plagiarized')
            elif (ans >= 0.7):
                OneQuesFeedbackList.append('This student has a high score')
            elif (ans >= 0.3):
                OneQuesFeedbackList.append('This student has a normal score')
            else:
                OneQuesFeedbackList.append('This student has a low score')
        FeedbackList.append(OneQuesFeedbackList)
    return FeedbackList

def AverageListofList(ListofList):
    List1 = []  
    for lst in ListofList:
        List1.append(sum(lst)/len(lst))
    avg = round(sum(List1)/len(List1),2)
    return avg

def GenerateILOFeedback(MCQILO, MCQGradeList, CompILO, CompGradeList, TFILO, TFGradeList, EssILO, EssGradeList):
    ILOGrades = collections.defaultdict(list)
    ILOAvg    = collections.defaultdict(list)
    for key in MCQILO.keys():
        for val in MCQILO[key]:
            ILOGrades[key].append(MCQGradeList[val])
    
    for key in CompILO.keys():
        for val in CompILO[key]:
            ILOGrades[key].append(CompGradeList[val])
    
    for key in TFILO.keys():
        for val in TFILO[key]:
            ILOGrades[key].append(TFGradeList[val])
    
    for key in EssILO.keys():
        for val in EssILO[key]:
            ILOGrades[key].append(EssGradeList[val])
    
    for key in ILOGrades.keys():
        avg = AverageListofList(ILOGrades[key]) * 100
        avg=round(avg,1)
        ILOAvg[key] = "This ilo's questions were answered correctly by " + str(avg) +" %."
    
    return ILOAvg
    
# GenerateILOFeedback({'ilo1':[0],'ilo2':[1]}, [[1,1],[0,0]], {'ilo2':[0]}, [[0.6,0.5,0.7]], 
#         {'ilo3':[0]}, [[0,0]], {'ilo1':[0], 'ilo3':[1,2]}, [[1],[0.4,0.4],[0.5,0.7]])

#CHECK IF I NEED THE INSTRUCTOR ID LATER
@app.route("/GradeExam/<ExamTitle>")
def GradeExam(ExamTitle):
    A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X = database.GetExamToEvaluate(ExamTitle)

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

    MCQILO            = U
    CompILO           = V
    TFILO             = W
    EssILO            = X

    #*******
    QuestionsLen      = [] #mcq, tf, comp, essay
    QuestionsLen.append(len(MCQQuestionList))
    QuestionsLen.append(len(TFQuestionList))
    QuestionsLen.append(len(CompQuestionList))
    QuestionsLen.append(len(EssQuestionList))

    StudentGrades     = []
    ModelGrades       = []

    #Call here the function from evaluator.py to grade the exam
    MCQGradeEvaluated  = 0
    CompGradeEvaluated = 0
    TFGradeEvaluated   = 0
    EssGradeEvaluated  = 0
    StudentNamesist    = []
    EssStudentFeedback = []
    QuestionsFeedbackList = []

    print("Starting Evaluation proces ... ")

    if (MCQAnswerList):
        MCQGradeEvaluated  = Evaluate.Evaluator("MCQ",MCQStudentIDList,MCQAnswerList,MCQModelAnswer,MCQGrade)
        QuestionsFeedbackList.append(GenerateQuestionFeedback(MCQGradeEvaluated))
        StudentNamesist    = database.GetStudentsNamesByID(MCQStudentIDList[0])
        StudentGrades.append(MCQGradeEvaluated)
        ModelGrades.append(MCQGrade)

    if (TFAnswerList):
        TFGradeEvaluated   = Evaluate.Evaluator("TF",TFStudentIDList,TFAnswerList,TFModelAnswer,TFGrade)
        QuestionsFeedbackList.append(GenerateQuestionFeedback(TFGradeEvaluated))
        StudentNamesist    = database.GetStudentsNamesByID(TFStudentIDList[0])
        StudentGrades.append(TFGradeEvaluated)
        ModelGrades.append(TFGrade)

    if (CompAnswerList):
        CompGradeEvaluated = Evaluate.Evaluator("Complete",CompStudentIDList,CompAnswerList,CompModelAnswer,CompGrade)
        QuestionsFeedbackList.append(GenerateQuestionFeedback(CompGradeEvaluated))
        StudentNamesist    = database.GetStudentsNamesByID(CompStudentIDList[0])
        StudentGrades.append(CompGradeEvaluated)
        ModelGrades.append(CompGrade)

    if (EssAnswerList):
        EssGradeEvaluated  = Evaluate.Evaluator("Essay",EssStudentIDList,EssAnswerList,EssModelAnswer,EssGrade)
        #print(EssGradeEvaluated)
        QuestionsFeedbackList.append(GenerateEssayQuestionsFeedback(EssGradeEvaluated)) #list
        EssStudentFeedback = GenerateEssayAnswerFeedback(EssGradeEvaluated) #list of list
        EssGradeEvaluated1 = np.array(EssGradeEvaluated)
        for lst in EssGradeEvaluated1:
            lst[lst>0.80] = 1
            mask1 = ((lst<=0.80) & (lst>0.6))
            lst[mask1] = 0.8
            mask2 = ((lst<=0.6) & (lst>0.4))
            lst[mask2] = 0.6
            mask3 = ((lst<=0.4) & (lst>0.2))
            lst[mask3] = 0.4
            mask4 = ((lst<=0.2) & (lst>0))
            lst[mask4] = 0.2
        EssGradeEvaluated=EssGradeEvaluated1.tolist()
        #print(EssGradeEvaluated)
        StudentNamesist    = database.GetStudentsNamesByID(EssStudentIDList[0])
        StudentGrades.append(EssGradeEvaluated)
        ModelGrades.append(EssGrade)
    
    ILOFeedbackDict = GenerateILOFeedback(MCQILO, MCQGradeEvaluated, CompILO, CompGradeEvaluated, TFILO, TFGradeEvaluated, EssILO, EssGradeEvaluated)

    # MCQQuestionList   = ['MCQ 1', 'MCQ2', 'MCQ3']
    # MCQModelAnswer    = ['Model Ans 1', 'Model Ans 2', 'Model Ans 3']
    # MCQGrade          = [3, 4, 2]
    # MCQAnswerList     = [['Student 1 ans MCQ1', 'Student 2 ans MCQ1', 'Student 3 ans MCQ1'],
    #                      ['Student 1 ans MCQ2', 'Student 2 ans MCQ2', 'Student 3 ans MCQ2'],
    #                      ['Student 1 ans MCQ3', 'Student 2 ans MCQ3', 'Student 3 ans MCQ3']] #assuming for example 3 students
    # MCQStudentIDList  = [[1,2,3],[1,2,3],[1,2,3]] #assuming for example 3 students
    flat_ModelGrades = []
    for sublist in ModelGrades:
        for item in sublist:
            flat_ModelGrades.append(item)
    
    StudentGradesFlattened     = [e for sl in StudentGrades for e in sl]
    QuestionsFeedbackFlattened = [e for sl in QuestionsFeedbackList for e in sl]
    #print(StudentGradesFlattened)
    newlist=[]
    Multiplied_Grades=[]
    for q,model in zip(StudentGradesFlattened,flat_ModelGrades):
        newlist=[]
        for grade in q:
            grade=model*grade
            newlist.append(grade)   
        Multiplied_Grades.append(newlist) 
    print('Finished evaluation and starting excel sheet generation')

    print(flat_ModelGrades)
    print(StudentNamesist)
    print(Multiplied_Grades)
    print(ExamTitle)
    print(QuestionsLen)
    print(QuestionsFeedbackFlattened)
    print(ILOFeedbackDict)
    print(EssStudentFeedback)

    excel = genX.GenExcel(flat_ModelGrades, StudentNamesist, Multiplied_Grades, ExamTitle, QuestionsLen, QuestionsFeedbackFlattened, ILOFeedbackDict, EssStudentFeedback)
    #print('Finished generating excel sheet successfully')
    if (excel == 'Finished generating the excel sheet successfully'):
        return {'Grades':excel}
    else: 
        excel = 'Unfortunately, an error occured'
        return {'Grades':excel}  

# GradeExam('try exam')
#GradeExam('Midterm Data Structures 2016')

@app.route("/GetInstName/<username>")
def GetInstName(username):
    name,id = database.GetInstName(username)
    return {'name':name, 'id':id}

@app.route("/GetStudName/<username>")
def GetStudName(username):
    name,id = database.GetStudName(username)
    return {'name':name, 'id':id}

@app.route("/GetStudNamebyID/<int:id>")
def GetStudNamebyID(id): #get username
    name = database.GetStudNamebyID(id)
    return {'name':name}

@app.route("/GetInstUsername/<int:id>")
def GetInstUsername(id):
    username = database.GetInstUsername(id)
    return {'username':username}

# lst=[[[0, 1]], [[1, 0]], [[1, 0.685845]], [[1.0, 0.0]]]
# print([e for sl in lst for e in sl])
#output : [[0, 1], [1, 0], [1, 0.685845], [1.0, 0.0]]
# x=1

app.run(debug=True)