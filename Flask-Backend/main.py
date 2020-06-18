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

word2index = pickle.load(open("D:\\University\\Semester 10 Spring 2020\\GP\\Testing the 3 models\\1. word2vec\\word2index","rb"))
index2word = pickle.load(open("D:\\University\\Semester 10 Spring 2020\\GP\\Testing the 3 models\\1. word2vec\\index2word","rb"))
char2index = pickle.load(open("D:\\University\\Semester 10 Spring 2020\\GP\\Testing the 3 models\\1. word2vec\\index2word",'rb'))

embeddings = pickle.load(open("D:\\University\\Semester 10 Spring 2020\\GP\\Testing the 3 models\\1. word2vec\\embeddings.pk",'rb'))


def InputPreprocess(questions,contexts):
    questionList=[]
    contextList=[]
    for question in questions:
        for word in question.split():
            questionList.append(word.strip(string.punctuation).lower())

    for context in contexts:
        for word in context.split():
            contextList.append(word.strip(string.punctuation).lower())

    userQuestionEmbedded, userContextEmbedded, _,userQuestionCharEmbedded,userContextCharEmbedded = Embed([questionList],[contextList],["-"])

    for i in range(len(userQuestionCharEmbedded)):
        userQuestionCharEmbedded= tf.keras.preprocessing.sequence.pad_sequences(userQuestionCharEmbedded[i],padding='post',maxlen=16,value=len(char2index))
    userQuestionCharEmbedded = be.expand_dims(userQuestionCharEmbedded,axis=0)

    for i in range(len(userContextCharEmbedded)):
        userContextCharEmbedded= tf.keras.preprocessing.sequence.pad_sequences(userContextCharEmbedded[i],padding='post',maxlen=16,value=len(char2index))
    userContextCharEmbedded = be.expand_dims(userContextCharEmbedded,axis=0)

    # print("Before Padding")
    userQuestionEmbedded = tf.keras.preprocessing.sequence.pad_sequences(userQuestionEmbedded,padding='post',truncating="post",dtype='float32',maxlen=50)
    userContextEmbedded = tf.keras.preprocessing.sequence.pad_sequences(userContextEmbedded,padding='post',truncating="post",dtype='float32',maxlen=660)
    userQuestionCharEmbedded = tf.keras.preprocessing.sequence.pad_sequences(userQuestionCharEmbedded,padding='post',truncating="post",maxlen=50,value=len(char2index))
    userContextCharEmbedded = tf.keras.preprocessing.sequence.pad_sequences(userContextCharEmbedded,padding='post',truncating="post",maxlen=660,value=len(char2index))

    return userQuestionEmbedded,userContextEmbedded,userQuestionCharEmbedded,userContextCharEmbedded


def OutputProcess(p,context):
    start = np.argmax(p[0])
    end = np.argmax(p[1])

    contextList = context.split()
    answer =""
    if start<=end:
        answer=" ".join(contextList[start:end+1])

    else:
        maxPos=0
        for i in range(len(contextList)):
            for j in range(i,len(contextList)):
                if p[0][0][i]*p[1][0][j] >maxPos:
                    maxPos = p[0][0][i]*p[1][0][j]
                    answer = " ".join(contextList[i:j+1])

    return answer

def Embed(questions,contexts,answers):
    e_q=[]      #embedded question
    e_qC=[]     #embedded question Characters
    e_c=[]      #embedded context
    e_cC=[]      #embedded context Characters

    e_a=[]      #embedded answer

    for i in range(len(questions)):
        question=[]
        questionChars=[]
        for word in questions[i]:
            if word in word2index:
                question.append(embeddings[word2index[word]])
            else:
                question.append(embeddings[word2index["UNK"]])

        chars=[]
        for char in word:
            if char in char2index:
                chars.append(char2index[char])
        questionChars.append(np.array(chars))

        context=[]
        contextChars=[]
        for word in contexts[i]:
            if word in word2index:
                context.append(embeddings[word2index[word]])
            else:
                context.append(embeddings[word2index["UNK"]])

        chars=[]
        for char in word:
            if char in char2index:
                chars.append(char2index[char])
        contextChars.append(np.array(chars))


        answer=[]
        for word in answers[i]:
            if word in word2index:
                answer.append(embeddings[word2index[word]])
            else:
                answer.append(embeddings[word2index["UNK"]])



    e_q.append(question)
    e_qC.append(questionChars)
        
    e_c.append(context)
    e_cC.append(contextChars)

    e_a.append(answer)

    return np.array(e_q), np.array(e_c), np.array(e_a),np.array(e_qC),np.array(e_cC)

 

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
        question = database.AddMCQ(Question, Answers, CorrectAns, Grade, ILO, ExamTitle)
        if (question == 'MCQ question is added successfully'):
            MCQReturn = question
        elif (question == 'There was an issue adding mcq'):
            MCQReturn = question
        elif (question=='Question already exists in the exam'):
            MCQReturn = question
    elif (Exam=='There was an issue creating the exam'):
        MCQReturn = Exam
    return {'MCQReturn':MCQReturn}

@app.route("/UpdateMCQ/<OldQuestion>/<NewQuestion>/<NewAnswers>/<NewCorrectAns>/<ExamTitle>")
def UpdateMCQ(OldQuestion,NewQuestion, NewAnswers, NewCorrectAns, ExamTitle):
    updated = database.UpdateMCQ(OldQuestion,NewQuestion, NewAnswers, NewCorrectAns, ExamTitle)
    if (updated=='There was an issue Updating mcq question'):
        pass
    elif (updated=='There was an issue Updating mcq options'):
        pass
    elif (updated=='There was an issue Updating mcq options'):
        pass
    elif (updated=='Mcq is updated successfully'):
        pass
    return 

@app.route("/AddComplete/<string:ExamTitle>/<int:InstructorID>/<Question1>/<Question2>/<CorrectAns>/<Grade>/<ILO>")
def AddComplete(ExamTitle,InstructorID,Question1,Question2,CorrectAns,Grade,ILO):
    IloReturn = database.AddILOIfNotExist(ILO, InstructorID)
    #print(IloReturn)
    Question = str(Question1) + '/' + str(Question2)
    Exam = database.CreateExamIfNotExist(ExamTitle,InstructorID)
    CompleteReturn=1
    if (Exam=='ExamFound' or Exam=='Exam is added successfully'):
        question = database.AddComplete(Question, CorrectAns, Grade, ILO, ExamTitle)
        if (question == 'Complete question is added successfully'):
            CompleteReturn = question
        elif (question == 'There was an issue adding complete question'):
            CompleteReturn = question
        elif (question=='Question already exists in the exam'):
            CompleteReturn = question
    elif (Exam=='There was an issue creating the exam'):
        CompleteReturn = Exam
    return {'CompleteReturn':CompleteReturn}

@app.route("/UpdateComplete/<OldQuestion>/<NewQuestion>/<NewCorrectAns>/<ExamTitle>")
def UpdateComplete(OldQuestion,NewQuestion, NewCorrectAns, ExamTitle):
    updated = database.UpdateComplete(OldQuestion,NewQuestion, NewCorrectAns, ExamTitle)
    if (updated=='There was an issue Updating complete question'):
        pass
    elif (updated=='There was an issue Updating complete correct answer'):
        pass
    elif (updated=='Complete question is updated successfully'):
        pass
    return 

@app.route("/AddTrueFalse/<string:ExamTitle>/<int:InstructorID>/<string:Question>/<string:CorrectAns>/<int:Grade>/<string:ILO>")
def AddTrueFalse(ExamTitle,InstructorID,Question,CorrectAns,Grade,ILO):
    IloReturn = database.AddILOIfNotExist(ILO, InstructorID)
    #print(IloReturn)
    Exam = database.CreateExamIfNotExist(ExamTitle,InstructorID)
    TFReturn=1
    #print(TFReturn)
    if (Exam=='ExamFound' or Exam=='Exam is added successfully'):
        question = database.AddTrueFalse(Question, CorrectAns, Grade, ILO, ExamTitle)
        if (question == 'T&F question is added successfully'):
            TFReturn = question
        elif (question == 'There was an issue adding T&F question'):
            TFReturn = question
        elif (question=='Question already exists in the exam'):
            TFReturn = question
    elif (question=='There was an issue creating the exam'):
        TFReturn = question
    return {'TFReturn':TFReturn}

@app.route("/UpdateTrueFalse/<OldQuestion>/<NewQuestion>/<NewCorrectAns>/<ExamTitle>")
def UpdateTrueFalse(OldQuestion,NewQuestion, NewCorrectAns, ExamTitle):
    updated = database.UpdateTrueFalse(OldQuestion,NewQuestion, NewCorrectAns, ExamTitle)
    if (updated=='There was an issue Updating True False question'):
        pass
    elif (updated=='There was an issue Updating True False correct answer'):
        pass
    elif (updated=='TF question is updated successfully'):
        pass
    return 

@app.route("/AddEssay/<string:ExamTitle>/<int:InstructorID>/<string:Question>/<string:CorrectAns>/<Grade>/<ILO>")
def AddEssay(ExamTitle,InstructorID,Question,CorrectAns,Grade,ILO):
    IloReturn = database.AddILOIfNotExist(ILO, InstructorID)
    #print(IloReturn)
    Exam = database.CreateExamIfNotExist(ExamTitle,InstructorID)
    EssayReturn=1
    if (Exam=='ExamFound' or Exam=='Exam is added successfully'):
        question = database.AddEssay(Question, CorrectAns, Grade, ILO, ExamTitle)
        if (question == 'Essay question is added successfully'):
            EssayReturn = question
        elif (question == 'There was an issue adding essay question'):
            EssayReturn = question
        elif (question=='Question already exists in the exam'):
            EssayReturn = question
    elif (Exam=='There was an issue creating the exam'):
        EssayReturn = Exam
    return {'EssayReturn':EssayReturn}

@app.route("/UpdateEssay/<OldQuestion>/<NewQuestion>/<NewCorrectAns>/<ExamTitle>")
def UpdateEssay(OldQuestion,NewQuestion, NewCorrectAns, ExamTitle):
    updated = database.UpdateEssay(OldQuestion,NewQuestion, NewCorrectAns, ExamTitle)
    if (updated=='There was an issue Updating essay question'):
        pass
    elif (updated=='There was an issue Updating essay correct answer'):
        pass
    elif (updated=='Essay question is updated successfully'):
        pass
    return 

# # ALREADY ADDED
# database.db.drop_all()
# database.db.create_all()
# ins1=database.Instructor(InstructorID='1',InstructorUserName='ins1name',InstructorPassword='ins1pw')
# database.db.session.add(ins1)
# database.db.session.commit()
# print(database.Instructor.query.all())
# print(database.Instructor.query.get(1).InstructorID) #ID = 1
# exam1=database.Exam(ExamTitle='exam1', instructor_id='1')
# exam2=database.Exam(ExamTitle='exam2', instructor_id='1')
# database.db.session.add(exam1)
# database.db.session.add(exam2)
# database.db.session.commit()

print(AddMCQ('exam1',1,'mcq23','asdsad','sadasd',10,'ilo5'))
print(AddMCQ('exam5',1,'mcq24','asdsad','sadasd',10,'ilo2'))
# print(AddComplete('exam1',1,'comp4','adssa','asdyuagsf',10,'ilo1'))
# print(AddComplete('exam6',1,'comp','asdasd','asdyuagsf',10,'ilo1'))
# print(AddTrueFalse('exam1',1,'TF25','asdyuagsf',10,'ilo1'))
# print(AddTrueFalse('exam7',1,'TF','asdyuagsf',10,'ilo1'))
# print(AddEssay('exam1',1,'essay5','asdyuagsf',10,'ilo1'))
# print(AddEssay('exam8',1,'essay','asdyuagsf',10,'ilo1'))
# print(database.MCQ.query.all())
# print(database.Complete.query.all())
# print(database.Essay.query.all())
# print(database.TrueAndFalse.query.all())

print(database.MCQ.query.filter_by(ILO='exam5').all())
print(database.MCQ.query.filter_by(ILO='ilo1').all())
print(database.MCQ.query.filter_by(ILO='ilo2').all())



app.run(debug=True)