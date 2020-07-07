import flask
import tensorflow as tf
from tensorflow.keras.models import load_model
import tensorflow.keras.backend as be
import string
import numpy as np
import pickle
import json
from Evaluator_Integrated import EvaluateAns
import Database as database

#app=flask.Flask("__main__")
app=database.app

# word2index = pickle.load(open("D:\\University\\Semester 10 Spring 2020\\GP\\Testing the 3 models\\1. word2vec\\word2index","rb"))
# index2word = pickle.load(open("D:\\University\\Semester 10 Spring 2020\\GP\\Testing the 3 models\\1. word2vec\\index2word","rb"))
# char2index = pickle.load(open("D:\\University\\Semester 10 Spring 2020\\GP\\Testing the 3 models\\1. word2vec\\index2word",'rb'))

# embeddings = pickle.load(open("D:\\University\\Semester 10 Spring 2020\\GP\\Testing the 3 models\\1. word2vec\\embeddings.pk",'rb'))


# def InputPreprocess(questions,contexts):
#     questionList=[]
#     contextList=[]
#     for question in questions:
#         for word in question.split():
#             questionList.append(word.strip(string.punctuation).lower())

#     for context in contexts:
#         for word in context.split():
#             contextList.append(word.strip(string.punctuation).lower())

#     userQuestionEmbedded, userContextEmbedded, _,userQuestionCharEmbedded,userContextCharEmbedded = Embed([questionList],[contextList],["-"])

#     for i in range(len(userQuestionCharEmbedded)):
#         userQuestionCharEmbedded= tf.keras.preprocessing.sequence.pad_sequences(userQuestionCharEmbedded[i],padding='post',maxlen=16,value=len(char2index))
#     userQuestionCharEmbedded = be.expand_dims(userQuestionCharEmbedded,axis=0)

#     for i in range(len(userContextCharEmbedded)):
#         userContextCharEmbedded= tf.keras.preprocessing.sequence.pad_sequences(userContextCharEmbedded[i],padding='post',maxlen=16,value=len(char2index))
#     userContextCharEmbedded = be.expand_dims(userContextCharEmbedded,axis=0)

#     # print("Before Padding")
#     userQuestionEmbedded = tf.keras.preprocessing.sequence.pad_sequences(userQuestionEmbedded,padding='post',truncating="post",dtype='float32',maxlen=50)
#     userContextEmbedded = tf.keras.preprocessing.sequence.pad_sequences(userContextEmbedded,padding='post',truncating="post",dtype='float32',maxlen=660)
#     userQuestionCharEmbedded = tf.keras.preprocessing.sequence.pad_sequences(userQuestionCharEmbedded,padding='post',truncating="post",maxlen=50,value=len(char2index))
#     userContextCharEmbedded = tf.keras.preprocessing.sequence.pad_sequences(userContextCharEmbedded,padding='post',truncating="post",maxlen=660,value=len(char2index))

#     return userQuestionEmbedded,userContextEmbedded,userQuestionCharEmbedded,userContextCharEmbedded


# def OutputProcess(p,context):
#     start = np.argmax(p[0])
#     end = np.argmax(p[1])

#     contextList = context.split()
#     answer =""
#     if start<=end:
#         answer=" ".join(contextList[start:end+1])

#     else:
#         maxPos=0
#         for i in range(len(contextList)):
#             for j in range(i,len(contextList)):
#                 if p[0][0][i]*p[1][0][j] >maxPos:
#                     maxPos = p[0][0][i]*p[1][0][j]
#                     answer = " ".join(contextList[i:j+1])

#     return answer

# def Embed(questions,contexts,answers):
#     e_q=[]      #embedded question
#     e_qC=[]     #embedded question Characters
#     e_c=[]      #embedded context
#     e_cC=[]      #embedded context Characters

#     e_a=[]      #embedded answer

#     for i in range(len(questions)):
#         question=[]
#         questionChars=[]
#         for word in questions[i]:
#             if word in word2index:
#                 question.append(embeddings[word2index[word]])
#             else:
#                 question.append(embeddings[word2index["UNK"]])

#         chars=[]
#         for char in word:
#             if char in char2index:
#                 chars.append(char2index[char])
#         questionChars.append(np.array(chars))

#         context=[]
#         contextChars=[]
#         for word in contexts[i]:
#             if word in word2index:
#                 context.append(embeddings[word2index[word]])
#             else:
#                 context.append(embeddings[word2index["UNK"]])

#         chars=[]
#         for char in word:
#             if char in char2index:
#                 chars.append(char2index[char])
#         contextChars.append(np.array(chars))


#         answer=[]
#         for word in answers[i]:
#             if word in word2index:
#                 answer.append(embeddings[word2index[word]])
#             else:
#                 answer.append(embeddings[word2index["UNK"]])



#     e_q.append(question)
#     e_qC.append(questionChars)
        
#     e_c.append(context)
#     e_cC.append(contextChars)

#     e_a.append(answer)

#     return np.array(e_q), np.array(e_c), np.array(e_a),np.array(e_qC),np.array(e_cC)

 

# QWE,CWE,QCE,CCE = InputPreprocess(userQuestion,userContext)

# p=model.predict([QWE,CWE,QCE,CCE ])
# answer = OutputProcess(p,userContext[0])
# print(p)
# print("Context:\n",userContext[0],"\nQuestion:\n",userQuestion[0],"\nAnswer:\n",answer)
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

    Grade = 0
    return {'Grade':Grade}

app.run(debug=True)