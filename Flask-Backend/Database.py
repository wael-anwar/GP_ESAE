from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import collections

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ease.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Student(db.Model):
    StudentID       = db.Column(db.Integer,    primary_key=True)
    StudentUserName = db.Column(db.String(50), unique=True, nullable=False)
    StudentName     = db.Column(db.String(50), nullable=False)
    StudentPassword = db.Column(db.String(60), nullable=False)
    #email = db.Column(db.String(120), unique=True, nullable=False)
    #posts = db.relationship('Post', backref='author', lazy=True)
    def __repr__(self):
        return f"('{self.StudentUserName})"

class Instructor(db.Model):
    InstructorID       = db.Column(db.Integer,    primary_key=True)
    InstructorUserName = db.Column(db.String(50), unique=True, nullable=False)
    InstructorName     = db.Column(db.String(50), nullable=False)
    InstructorPassword = db.Column(db.String(60), nullable=False)
    Exams              = db.relationship('Exam', backref='put', lazy=True) #Instructor 1:many exams
    MCQS               = db.relationship('MCQ', backref='put', lazy=True) #Instructor 1:many MCQs
    Completes          = db.relationship('Complete', backref='put', lazy=True) #Instructor 1:many Complete
    TFS                = db.relationship('Truefalse', backref='put', lazy=True) #Instructor 1:many TF
    Essays             = db.relationship('Essay', backref='put', lazy=True) #Instructor 1:many Essay
    ILOs               = db.relationship('Ilo', backref='assign', lazy=True) #Instructor 1:many ILOs
    def __repr__(self):
        return f"('{self.InstructorUserName})"

class Exam(db.Model):
    ExamID        = db.Column(db.Integer,     primary_key=True)
    ExamTitle     = db.Column(db.String(100), nullable=False, unique=True)
    date_posted   = db.Column(db.DateTime,    nullable=False, default=datetime.utcnow)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.InstructorID'), nullable=False)
    mcq           = db.relationship('MCQ',          backref='has', lazy=True) #Exam 1:many  MCQ
    complete      = db.relationship('Complete',     backref='has', lazy=True) #Exam 1:many  
    truefalse  = db.relationship('Truefalse', backref='has', lazy=True) #Exam 1:many  
    essay         = db.relationship('Essay',        backref='has', lazy=True) #Exam 1:many  
    def __repr__(self):
        return f"('{self.ExamID}','{self.ExamTitle}', '{self.instructor_id}')"

class MCQ(db.Model):
    QuestionID    = db.Column(db.Integer, primary_key=True)
    Question      = db.Column(db.Text,    nullable=False)
    Answers       = db.Column(db.Text,    nullable=False) #will be separated by a slash or comma for example
    CorrectAnswer = db.Column(db.Text,    nullable=False)
    Grade         = db.Column(db.Integer, nullable=False)
    ILO           = db.Column(db.Text, db.ForeignKey('ilo.ILOContent'), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.InstructorID'), nullable=False)
    exam_id       = db.Column(db.Integer, db.ForeignKey('exam.ExamID'), nullable=False)
    #ilo_id        = db.Column(db.Integer, db.ForeignKey('iLO_.ILO_ID'), nullable=False)
    def __repr__(self):
        return f"('{self.Question}', '{self.Answers}', '{self.CorrectAnswer}', '{self.ILO}', '{self.exam_id}')"

class Complete(db.Model):
    QuestionID    = db.Column(db.Integer, primary_key=True)
    Question      = db.Column(db.Text,    nullable=False) #2 texts will be separated by a slash for example
    CorrectAnswer = db.Column(db.Text,    nullable=False)
    Grade         = db.Column(db.Integer, nullable=False)
    ILO           = db.Column(db.Text, db.ForeignKey('ilo.ILOContent'), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.InstructorID'), nullable=False)
    exam_id       = db.Column(db.Integer, db.ForeignKey('exam.ExamID'), nullable=False)
    #ilo_id        = db.Column(db.Integer, db.ForeignKey('iLO_.ILO_ID'), nullable=False)
    def __repr__(self):
        return f"('{self.Question}', '{self.CorrectAnswer}', '{self.ILO}', '{self.instructor_id}', '{self.exam_id}')"

class Truefalse(db.Model):
    QuestionID    = db.Column(db.Integer, primary_key=True)
    Question      = db.Column(db.Text,    nullable=False) 
    CorrectAnswer = db.Column(db.Text,    nullable=False)
    Grade         = db.Column(db.Integer, nullable=False)
    ILO           = db.Column(db.Text, db.ForeignKey('ilo.ILOContent'), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.InstructorID'), nullable=False)
    exam_id       = db.Column(db.Integer, db.ForeignKey('exam.ExamID'), nullable=False)
    #ilo_id        = db.Column(db.Integer, db.ForeignKey('iLO_.ILO_ID'), nullable=False)
    def __repr__(self):
        return f"('{self.Question}', '{self.CorrectAnswer}', '{self.ILO}', '{self.exam_id})"

class Essay(db.Model):
    QuestionID    = db.Column(db.Integer, primary_key=True)
    Question      = db.Column(db.Text,    nullable=False)
    CorrectAnswer = db.Column(db.Text,    nullable=False)
    Grade         = db.Column(db.Integer, nullable=False)
    ILO           = db.Column(db.Text, db.ForeignKey('ilo.ILOContent'), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.InstructorID'), nullable=False)
    exam_id       = db.Column(db.Integer, db.ForeignKey('exam.ExamID'), nullable=False)
    #ilo_id        = db.Column(db.Integer, db.ForeignKey('iLO_.ILO_ID'), nullable=False)
    def __repr__(self):
        return f"('{self.Question}', '{self.CorrectAnswer}', '{self.ILO}', '{self.exam_id})"

class Ilo (db.Model):
    ILO_ID        = db.Column(db.Integer, primary_key=True)
    ILOContent    = db.Column(db.Text,    nullable=False, unique=True)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.InstructorID'), nullable=False)  
    def __repr__(self):
        return f"('{self.ILO_ID}', '{self.ILOContent}','{self.instructor_id}')"

class StudentTakeExam(db.Model):
    student_id = db.Column(db.Integer, db.ForeignKey('student.StudentID'), primary_key=True)
    exam_id    = db.Column(db.Integer, db.ForeignKey('exam.ExamID'), primary_key=True)
    Grade      = db.Column(db.Integer)
    def __repr__(self):
        return f"('{self.student_id}', '{self.exam_id}','{self.Grade}')"

class StudentMCQ(db.Model):
    ID         = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.StudentID'))
    exam_id    = db.Column(db.Integer, db.ForeignKey('exam.ExamID'), nullable=False)
    mcq_id     = db.Column(db.Integer, db.ForeignKey('MCQ.QuestionID'), nullable=False)
    Answer = db.Column(db.Text)
    def __repr__(self):
        return f"('{self.student_id}', '{self.exam_id}','{self.mcq_id}','{self.Answer}')"

class StudentComplete(db.Model):
    ID         = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.StudentID'))
    exam_id    = db.Column(db.Integer, db.ForeignKey('exam.ExamID'), nullable=False)
    complete_id     = db.Column(db.Integer, db.ForeignKey('complete.QuestionID'), nullable=False)
    Answer = db.Column(db.Text)
    def __repr__(self):
        return f"('{self.student_id}', '{self.exam_id}','{self.complete_id}','{self.Answer}')"

class StudentTF(db.Model):
    ID         = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.StudentID'))
    exam_id    = db.Column(db.Integer, db.ForeignKey('exam.ExamID'), nullable=False)
    tf_id     = db.Column(db.Integer, db.ForeignKey('truefalse.QuestionID'), nullable=False)
    Answer = db.Column(db.Text)
    def __repr__(self):
        return f"('{self.student_id}', '{self.exam_id}','{self.tf_id}','{self.Answer}')"

class StudentEssay(db.Model):
    ID         = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.StudentID'))
    exam_id    = db.Column(db.Integer, db.ForeignKey('exam.ExamID'), nullable=False)
    essay_id     = db.Column(db.Integer, db.ForeignKey('essay.QuestionID'), nullable=False)
    Answer = db.Column(db.Text)
    def __repr__(self):
        return f"('{self.student_id}', '{self.exam_id}','{self.essay_id}','{self.Answer}')"



def InstructorSignUp(username, name, pw):
    try:
        Inst = Instructor(InstructorUserName = username, InstructorName = name, InstructorPassword=pw)
        db.session.add(Inst)
        db.session.commit()
        return 'Added successfully'
    except:
        return 'Error'

def StudentSignUp(username, name, pw):
    try:
        Stud = Student(StudentUserName = username, StudentName = name, StudentPassword=pw)
        db.session.add(Stud)
        db.session.commit()
        return 'Added successfully'
    except:
        return 'Error'

def InstructorSignIn(username, pw):
    Inst = Instructor.query.filter_by(InstructorUserName = username, InstructorPassword=pw).all()
    if (not Inst):
        return 'Error',0
    elif (Inst[0]):
        return 'Found',Inst[0].InstructorID

def StudentSignIn(username, pw):
    Stud = Student.query.filter_by(StudentUserName = username, StudentPassword=pw).all()
    if (not Stud):
        return 'Error',0
    elif (Stud[0]):
        return 'Found',Stud[0].StudentID

def GetExamByInstructorID(InstructorID):
    ExamList=[]
    Exams = Exam.query.filter_by(instructor_id = InstructorID).all()
    for exam in Exams:
        ExamList.append(exam.ExamTitle)
    return ExamList

def GetAllExams(StudentID):
    SubmittedExamList=[]
    check1 = StudentComplete.query.filter_by(student_id=StudentID).all()
    check2 = StudentEssay.query.filter_by(student_id=StudentID).all()
    check3 = StudentMCQ.query.filter_by(student_id=StudentID).all()
    check4 = StudentTF.query.filter_by(student_id=StudentID).all()
    for check in check1:
        if (check.exam_id not in SubmittedExamList):
            SubmittedExamList.append(check.exam_id)
    
    for check in check2:
        if (check.exam_id not in SubmittedExamList):
            SubmittedExamList.append(check.exam_id)
    
    for check in check3:
        if (check.exam_id not in SubmittedExamList):
            SubmittedExamList.append(check.exam_id)
    
    for check in check4:
        if (check.exam_id not in SubmittedExamList):
            SubmittedExamList.append(check.exam_id)

    ExamList=[]
    Exams = Exam.query.all()
    for exam in Exams:
        if (exam.ExamID not in SubmittedExamList):
            ExamList.append(exam.ExamTitle)
    return ExamList

def CreateExamIfNotExist(Examtitle,InstructorId):
    Exams = Exam.query.filter_by(ExamTitle = Examtitle).all()
    if (not Exams): #if it does not exist in the database
        try:
            NewExam = Exam(ExamTitle=Examtitle, instructor_id=InstructorId)
            db.session.add(NewExam)
            db.session.commit()
            return 'Exam is added successfully'
        except:
            return 'There was an issue creating the exam'
    else:
        return 'ExamFound'

def AddILOIfNotExist(ILOContent,instructor_id):
    ilo = Ilo.query.filter_by(ILOContent = ILOContent, instructor_id=instructor_id).all()
    if (not ilo): #if it does not exist in the database
        try:
            NewILO = Ilo(ILOContent = ILOContent, instructor_id=instructor_id)
            db.session.add(NewILO)
            db.session.commit()
            return 'ILO is added successfully'
        except:
            return 'There was an issue adding the ILO'
    else:
        return 'ILO Found'

def AddMCQ(Question, Answers, CorrectAns, Grade,ILO, ExamTitle, InstructorID):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle).all()
    ExamID = 0
    for ex in exam:
        ExamID = ex.ExamID
    QuestionExist = MCQ.query.filter_by(Question=Question, exam_id=ExamID).all()
    if (QuestionExist):
        return 'Question already exists in the exam'
    try:
        question = MCQ(Question=Question, Answers=Answers, CorrectAnswer=CorrectAns,Grade=Grade, ILO=ILO, exam_id=ExamID, instructor_id=InstructorID)
        db.session.add(question)
        db.session.commit()
        return 'MCQ question is added successfully'
    except:
        return 'There was an issue adding mcq'

def UpdateMCQ(OldQuestion,NewQuestion, NewAnswers, NewCorrectAns, ExamTitle, NewILO, NewGrade, InstructorID):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle).all()
    ExamID = 0
    for ex in exam:
        ExamID = ex.ExamID
    question = MCQ.query.filter_by(Question=OldQuestion, exam_id=ExamID).all()
    for ex in question:
        ex.Question=NewQuestion
        ex.Answers=NewAnswers
        ex.CorrectAnswer=NewCorrectAns
        ex.Grade=NewGrade
        AddILOIfNotExist(NewILO,InstructorID)
        ex.ILO = NewILO
        try:
            db.session.commit()
        except:
            return 'MCQ could not be updated'
    
    return "Successfully updated"

def AddComplete(Question, CorrectAns,Grade, ILO, ExamTitle, InstructorID):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle).all()
    ExamID = 0
    for ex in exam:
        ExamID = ex.ExamID
    QuestionExist = Complete.query.filter_by(Question=Question, exam_id=ExamID).all()
    if (QuestionExist):
        return 'Question already exists in the exam'
    try:
        question = Complete(Question=Question, CorrectAnswer=CorrectAns,Grade=Grade, ILO=ILO, exam_id=ExamID, instructor_id=InstructorID)
        db.session.add(question)
        db.session.commit()
        return 'Complete question is added successfully'
    except:
        return 'There was an issue adding complete question'
                    
def UpdateComplete(OldQuestion,NewQuestion, NewCorrectAns, ExamTitle, NewILO, NewGrade, InstructorID):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle).all()
    ExamID = 0
    for ex in exam:
        ExamID = ex.ExamID
    question = Complete.query.filter_by(Question=OldQuestion, exam_id=ExamID).all()
    for ex in question:
        ex.Question=NewQuestion
        ex.CorrectAnswer=NewCorrectAns
        ex.Grade=NewGrade
        AddILOIfNotExist(NewILO,InstructorID)
        ex.ILO = NewILO
        try:
            db.session.commit()
        except:
            return 'Complete question could not be updated'
    
    return "Successfully updated"

def AddTrueFalse(Question, CorrectAns, Grade, ILO, ExamTitle, InstructorID):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle).all()
    ExamID = 0
    for ex in exam:
        ExamID = ex.ExamID
    QuestionExist = Truefalse.query.filter_by(Question=Question, exam_id=ExamID).all()
    if (QuestionExist):
        return 'Question already exists in the exam'
    try:
        question = Truefalse(Question=Question, CorrectAnswer=CorrectAns,Grade=Grade, ILO=ILO, exam_id=ExamID, instructor_id=InstructorID)
        db.session.add(question)
        db.session.commit()
        return 'T&F question is added successfully'
    except:
        return 'There was an issue adding T&F question'

def UpdateTrueFalse(OldQuestion,NewQuestion, NewCorrectAns, ExamTitle,NewILO, NewGrade, InstructorID):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle).all()
    ExamID = 0
    for ex in exam:
        ExamID = ex.ExamID
    question = Truefalse.query.filter_by(Question=OldQuestion, exam_id=ExamID).all()
    for ex in question:
        ex.Question=NewQuestion
        ex.CorrectAnswer=NewCorrectAns
        ex.Grade=NewGrade
        AddILOIfNotExist(NewILO,InstructorID)
        ex.ILO = NewILO
        try:
            db.session.commit()
        except:
            return 'TF question could not be updated'
    
    return "Successfully updated"

def AddEssay(Question, CorrectAns, Grade, ILO, ExamTitle, InstructorID):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle).all()
    ExamID = 0
    for ex in exam:
        ExamID = ex.ExamID
    QuestionExist = Essay.query.filter_by(Question=Question, exam_id=ExamID).all()
    if (QuestionExist):
        return 'Question already exists in the exam'
    try:
        question = Essay(Question=Question, CorrectAnswer=CorrectAns,Grade=Grade, ILO=ILO, exam_id=ExamID, instructor_id=InstructorID)
        db.session.add(question)
        db.session.commit()
        return 'Essay question is added successfully'
    except:
        return 'There was an issue adding essay question'

def UpdateEssay(OldQuestion,NewQuestion, NewCorrectAns, ExamTitle,NewILO, NewGrade, InstructorID):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle).all()
    ExamID = 0
    for ex in exam:
        ExamID = ex.ExamID
    question = Essay.query.filter_by(Question=OldQuestion, exam_id=ExamID).all()
    for ex in question:
        ex.Question=NewQuestion
        ex.CorrectAnswer=NewCorrectAns
        ex.Grade=NewGrade
        AddILOIfNotExist(NewILO,InstructorID)
        ex.ILO = NewILO
        try:
            db.session.commit()
        except:
            return 'Essay question could not be updated'
    
    return "Successfully updated"

def MixMCQ(ExamTitle, InstructorID, ILO, Number):
    Count=0
    Questions = MCQ.query.filter_by(ILO=ILO, instructor_id=InstructorID).all()
    for ques in Questions:
        Count+=1
    if (Count < Number):
        return "The existing questions with this ILO are less than the required number, available number is " + str(Count)
    else:
        exam = CreateExamIfNotExist(ExamTitle,InstructorID)
        exam = Exam.query.filter_by(ExamTitle=ExamTitle).all()
        ExamID = 0
        for ex in exam:
            ExamID = ex.ExamID
        Count = Number
        for ques in Questions:
            if (Count == 0):
                break
            else:
                try:
                    Question   = ques.Question
                    Answers    = ques.Answers
                    CorrectAns = ques.CorrectAnswer
                    Grade      = ques.Grade   
                    question   = MCQ(Question=Question, Answers=Answers, CorrectAnswer=CorrectAns,Grade=Grade, ILO=ILO, exam_id=ExamID, instructor_id=InstructorID)

                    db.session.add(question)
                    db.session.commit()
                    Count-=1
                except:
                    return 'There was an issue, please try again'
        return "Question is added successfully"

def MixComplete(ExamTitle, InstructorID, ILO, Number):
    Count=0
    Questions = Complete.query.filter_by(ILO=ILO, instructor_id=InstructorID).all()
    for ques in Questions:
        Count+=1
    if (Count < Number):
        return "The existing questions with this ILO are less than the required number, available number is " + str(Count)
    else:
        exam = CreateExamIfNotExist(ExamTitle,InstructorID)
        exam = Exam.query.filter_by(ExamTitle=ExamTitle).all()
        ExamID = 0
        for ex in exam:
            ExamID = ex.ExamID
        Count = Number
        for ques in Questions:
            if (Count == 0):
                break
            else:
                try:
                    Question   = ques.Question
                    CorrectAns = ques.CorrectAnswer
                    Grade      = ques.Grade   
                    question   = Complete(Question=Question, CorrectAnswer=CorrectAns,Grade=Grade, ILO=ILO, exam_id=ExamID, instructor_id=InstructorID)
                    db.session.add(question)
                    db.session.commit()
                    Count-=1
                except:
                    return 'There was an issue, please try again'
        return "Question is added successfully"

def MixTF(ExamTitle, InstructorID, ILO, Number):
    Count=0
    Questions = Truefalse.query.filter_by(ILO=ILO, instructor_id=InstructorID).all()
    for ques in Questions:
        Count+=1
    if (Count < Number):
        return "The existing questions with this ILO are less than the required number, available number is " + str(Count)
    else:
        exam = CreateExamIfNotExist(ExamTitle,InstructorID)
        exam = Exam.query.filter_by(ExamTitle=ExamTitle).all()
        ExamID = 0
        for ex in exam:
            ExamID = ex.ExamID
        Count = Number
        for ques in Questions:
            if (Count == 0):
                break
            else:
                try:
                    Question   = ques.Question
                    CorrectAns = ques.CorrectAnswer
                    Grade      = ques.Grade   
                    question   = Truefalse(Question=Question, CorrectAnswer=CorrectAns,Grade=Grade, ILO=ILO, exam_id=ExamID, instructor_id=InstructorID)
                    db.session.add(question)
                    db.session.commit()
                    Count-=1
                except:
                    return 'There was an issue, please try again'
        return "Question is added successfully"

def MixEssay(ExamTitle, InstructorID, ILO, Number):
    Count=0
    Questions = Essay.query.filter_by(ILO=ILO, instructor_id=InstructorID).all()
    for ques in Questions:
        Count+=1
    if (Count < Number):
        return "The existing questions with this ILO are less than the required number, available number is " + str(Count)
    else:
        exam = CreateExamIfNotExist(ExamTitle,InstructorID)
        exam = Exam.query.filter_by(ExamTitle=ExamTitle).all()
        ExamID = 0
        for ex in exam:
            ExamID = ex.ExamID
        Count = Number
        for ques in Questions:
            if (Count == 0):
                break
            else:
                try:
                    Question   = ques.Question
                    CorrectAns = ques.CorrectAnswer
                    Grade      = ques.Grade   
                    question   = Essay(Question=Question, CorrectAnswer=CorrectAns,Grade=Grade, ILO=ILO, exam_id=ExamID, instructor_id=InstructorID)
                    db.session.add(question)
                    db.session.commit()
                    Count-=1
                except:
                    return 'There was an issue, please try again'
        return "Question is added successfully"

def GetILO(InstructorID):
    ILO_List = []
    ILOs = Ilo.query.filter_by(instructor_id = InstructorID).all()
    for ilo in ILOs:
        ILO_List.append(ilo.ILOContent)
    return ILO_List

def GetMCQ(ExamTitle, InstructorID):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle).all()
    ExamID = 0
    for ex in exam:
        ExamID = ex.ExamID
    Questions=0
    if (InstructorID==0):
        Questions = MCQ.query.filter_by(exam_id=ExamID).all()
    else:
        Questions = MCQ.query.filter_by(exam_id=ExamID, instructor_id=InstructorID).all()
    QuestionList      = []
    CounterList       = []
    AnswerList        = []
    CorrectAnswerList = []
    ILOList           = []
    GradeList         = []

    for question in Questions:
        QuestionList.append(question.Question)
        AnswerList.append(question.Answers)
        CounterList.append(len(question.Answers.split(",")))
        CorrectAnswerList.append(question.CorrectAnswer)
        ILOList.append(question.ILO)
        GradeList.append(question.Grade)
    return QuestionList, CounterList, AnswerList, CorrectAnswerList, ILOList, GradeList

def GetComplete(ExamTitle, InstructorID):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle).all()
    ExamID = 0
    for ex in exam:
        ExamID = ex.ExamID
    Questions=0
    if (InstructorID==0):
        Questions = Complete.query.filter_by(exam_id=ExamID).all()
    else:
        Questions = Complete.query.filter_by(exam_id=ExamID, instructor_id=InstructorID).all()
    QuestionList = []
    CorrectAnswerList = []
    ILOList           = []
    GradeList         = []
    for question in Questions:
        ques = question.Question.split("/")
        QuestionList.append(ques[0] + "......" + ques[1])
        CorrectAnswerList.append(question.CorrectAnswer)
        ILOList.append(question.ILO)
        GradeList.append(question.Grade)
    return QuestionList, CorrectAnswerList, ILOList, GradeList

def GetTF(ExamTitle, InstructorID):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle).all()
    ExamID = 0
    for ex in exam:
        ExamID = ex.ExamID
    Questions=0
    if (InstructorID==0):
        Questions = Truefalse.query.filter_by(exam_id=ExamID).all()
    else:
        Questions = Truefalse.query.filter_by(exam_id=ExamID, instructor_id=InstructorID).all()
    QuestionList      = []
    CorrectAnswerList = []
    ILOList           = []
    GradeList         = []
    for question in Questions:
        QuestionList.append(question.Question)
        CorrectAnswerList.append(question.CorrectAnswer)
        ILOList.append(question.ILO)
        GradeList.append(question.Grade)
    return QuestionList, CorrectAnswerList, ILOList, GradeList

def GetEssay(ExamTitle, InstructorID):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle).all()
    ExamID = 0
    for ex in exam:
        ExamID = ex.ExamID
    Questions=0
    if (InstructorID==0):
        Questions = Essay.query.filter_by(exam_id=ExamID).all()
    else:
        Questions = Essay.query.filter_by(exam_id=ExamID, instructor_id=InstructorID).all()
    QuestionList      = []
    CorrectAnswerList = []
    ILOList           = []
    GradeList         = []
    for question in Questions:
        QuestionList.append(question.Question)
        CorrectAnswerList.append(question.CorrectAnswer)
        ILOList.append(question.ILO)
        GradeList.append(question.Grade)
    return QuestionList, CorrectAnswerList, ILOList, GradeList

def GetAMCQ(ExamTitle, InstructorID, Question_):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle).all()
    ExamID = 0
    for ex in exam:
        ExamID = ex.ExamID
    Question = MCQ.query.filter_by(exam_id=ExamID, instructor_id=InstructorID, Question=Question_).all()
    question=0
    AnswerList=0
    CorrectAnswer=0
    ILO=0
    Grade=0
    for ques in Question:
        question=ques.Question
        AnswerList = ques.Answers.split(",")
        CorrectAnswer=ques.CorrectAnswer
        ILO=ques.ILO
        Grade=ques.Grade
    return question, AnswerList, CorrectAnswer, ILO,  Grade
    
def GetACompleteQues(ExamTitle, InstructorID, Question_):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle).all()
    ExamID = 0
    for ex in exam:
        ExamID = ex.ExamID
    ques = Question_.split("......")
    MyQuestion = ques[0]+'/'+ques[1]
    Question = Complete.query.filter_by(exam_id=ExamID, instructor_id=InstructorID, Question=MyQuestion).all()
    Question1=0
    Question2=0
    CorrectAnswer=0
    ILO=0
    Grade=0
    for ques in Question:
        quest = ques.Question.split("/")
        Question1=quest[0]
        Question2=quest[1]
        CorrectAnswer=ques.CorrectAnswer
        ILO=ques.ILO
        Grade=ques.Grade
    return Question1, Question2, CorrectAnswer, ILO,  Grade

def GetATrueFalseQues(ExamTitle, InstructorID, Question_):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle).all()
    ExamID = 0
    for ex in exam:
        ExamID = ex.ExamID
    Question = Truefalse.query.filter_by(exam_id=ExamID, instructor_id=InstructorID, Question=Question_).all()
    question=0
    CorrectAnswer=0
    ILO=0
    Grade=0
    for ques in Question:
        question=ques.Question
        CorrectAnswer=ques.CorrectAnswer
        ILO=ques.ILO
        Grade=ques.Grade
    return question, CorrectAnswer, ILO,  Grade

def GetAEssQues(ExamTitle, InstructorID, Question_):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle).all()
    ExamID = 0
    for ex in exam:
        ExamID = ex.ExamID
    Question = Essay.query.filter_by(exam_id=ExamID, instructor_id=InstructorID, Question=Question_).all()
    question=0
    CorrectAnswer=0
    ILO=0
    Grade=0
    for ques in Question:
        question=ques.Question
        CorrectAnswer=ques.CorrectAnswer
        ILO=ques.ILO
        Grade=ques.Grade
    return question, CorrectAnswer, ILO,  Grade
 
def StudentSubmitMCQ(ExamTitle, StudentID, mcq_question, Answer):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle).all()
    ExamID = 0
    for ex in exam:
        ExamID = ex.ExamID
    mcq = MCQ.query.filter_by(Question=mcq_question, exam_id=ExamID).all()
    mcq_id = 0
    for mcq_ in mcq:
        mcq_id = mcq_.QuestionID
    try:
        StudentAnswer = StudentMCQ(student_id=StudentID, exam_id=ExamID, mcq_id=mcq_id, Answer=Answer)
        db.session.add(StudentAnswer)
        db.session.commit()
        return 'MCQ answer is added successfully'
    except:
        return 'There was an issue adding mcq answer'

def StudentSubmitComplete(ExamTitle, StudentID, CompleteQuestion, Answer):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle).all()
    ExamID = 0
    for ex in exam:
        ExamID = ex.ExamID
    complete = Complete.query.filter_by(Question=CompleteQuestion, exam_id=ExamID).all()
    complete_id = 0
    for comp in complete:
        complete_id = comp.QuestionID
    try:
        StudentAnswer = StudentComplete(student_id=StudentID, exam_id=ExamID, complete_id=complete_id, Answer=Answer)
        db.session.add(StudentAnswer)
        db.session.commit()
        return 'Complete answer is added successfully'
    except:
        return 'There was an issue adding Complete answer'

def StudentSubmitTF(ExamTitle, StudentID, TFQuestion, Answer):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle).all()
    ExamID = 0
    for ex in exam:
        ExamID = ex.ExamID
    tf = Truefalse.query.filter_by(Question=TFQuestion, exam_id=ExamID).all()
    tf_id = 0
    for tf_ in tf:
        tf_id = tf_.QuestionID
    try:
        StudentAnswer = StudentTF(student_id=StudentID, exam_id=ExamID, tf_id=tf_id, Answer=Answer)
        db.session.add(StudentAnswer)
        db.session.commit()
        return 'TF answer is added successfully'
    except:
        return 'There was an issue adding TF answer'

def StudentSubmitEssay(ExamTitle, StudentID, EssQuestion, Answer):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle).all()
    ExamID = 0
    for ex in exam:
        ExamID = ex.ExamID
    essay = Essay.query.filter_by(Question=EssQuestion, exam_id=ExamID).all()
    essay_id = 0
    for ess in essay:
        essay_id = ess.QuestionID
    try:
        StudentAnswer = StudentEssay(student_id=StudentID, exam_id=ExamID, essay_id=essay_id, Answer=Answer)
        db.session.add(StudentAnswer)
        db.session.commit()
        return 'Essay answer is added successfully'
    except:
        return 'There was an issue adding Essay answer'

def DeleteExam(ExamTitle):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle).all()
    ExamID = exam[0].ExamID
    ques = MCQ.query.filter_by(exam_id = ExamID).all()
    for q in ques:
        try:
            db.session.delete(q)
            db.session.commit()
        except:
            'Error'
        try:
            DeleteILO = q.ILO
            DelILO = Ilo.query.filter_by(ILOContent = DeleteILO).all()
            db.session.delete(DelILO[0])
            db.session.commit()
        except:
            'Error'
    ques = Truefalse.query.filter_by(exam_id = ExamID).all()
    for q in ques:
        try:
            db.session.delete(q)
            db.session.commit()
        except:
            'Error'
        try:
            DeleteILO = q.ILO
            DelILO = Ilo.query.filter_by(ILOContent = DeleteILO).all()
            db.session.delete(DelILO[0])
            db.session.commit()
        except:
            'Error'
    ques = Complete.query.filter_by(exam_id = ExamID).all()
    for q in ques:
        try:
            db.session.delete(q)
            db.session.commit()
        except:
            'Error'
        try:
            DeleteILO = q.ILO
            DelILO = Ilo.query.filter_by(ILOContent = DeleteILO).all()
            db.session.delete(DelILO[0])
            db.session.commit()
        except:
            'Error'
    ques = Essay.query.filter_by(exam_id = ExamID).all()
    for q in ques:
        try:
            db.session.delete(q)
            db.session.commit()
        except:
            'Error'
        try:
            DeleteILO = q.ILO
            DelILO = Ilo.query.filter_by(ILOContent = DeleteILO).all()
            db.session.delete(DelILO[0])
            db.session.commit()
        except:
            'Error'
    
    ques = StudentTakeExam.query.filter_by(exam_id = ExamID).all()
    for q in ques:
        try:
            db.session.delete(q)
            db.session.commit()
        except:
            'Error'
    ques = StudentMCQ.query.filter_by(exam_id = ExamID).all()
    for q in ques:
        try:
            db.session.delete(q)
            db.session.commit()
        except:
            'Error'
    ques = StudentComplete.query.filter_by(exam_id = ExamID).all()
    for q in ques:
        try:
            db.session.delete(q)
            db.session.commit()
        except:
            'Error'
    ques = StudentTF.query.filter_by(exam_id = ExamID).all()
    for q in ques:
        try:
            db.session.delete(q)
            db.session.commit()
        except:
            'Error'
    ques = StudentEssay.query.filter_by(exam_id = ExamID).all()
    for q in ques:
        try:
            db.session.delete(q)
            db.session.commit()
        except:
            'Error'
    try:
        db.session.delete(exam[0])
        db.session.commit()
        return 'Deleted Successfully'
    except:
        return 'Please try again'

def DeleteMCQ(ExamTitle, Question):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle).all()
    ExamID = 0
    ExamID = exam[0].ExamID
    Question_ = MCQ.query.filter_by(exam_id=ExamID, Question=Question).all()
    try:
        db.session.delete(Question_[0])
        db.session.commit()
        try:
            DeleteILO = Question_[0].ILO
            DelILO = Ilo.query.filter_by(ILOContent = DeleteILO).all()
            db.session.delete(DelILO[0])
            db.session.commit()
        except:
            'Error'
        return 'Deleted Successfully'
    except:
        return 'Please try again'

def DeleteComplete(ExamTitle, Question):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle).all()
    ExamID = 0
    ExamID = exam[0].ExamID
    Question_ = Complete.query.filter_by(exam_id=ExamID, Question=Question).all()
    try:
        db.session.delete(Question_[0])
        db.session.commit()
        try:
            DeleteILO = Question_[0].ILO
            DelILO = Ilo.query.filter_by(ILOContent = DeleteILO).all()
            db.session.delete(DelILO[0])
            db.session.commit()
        except:
            'Error'
        return 'Deleted Successfully'
    except:
        return 'Please try again'

def DeleteTF(ExamTitle, Question):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle).all()
    ExamID = 0
    ExamID = exam[0].ExamID
    Question_ = Truefalse.query.filter_by(exam_id=ExamID, Question=Question).all()
    try:
        db.session.delete(Question_[0])
        db.session.commit()
        try:
            DeleteILO = Question_[0].ILO
            DelILO = Ilo.query.filter_by(ILOContent = DeleteILO).all()
            db.session.delete(DelILO[0])
            db.session.commit()
        except:
            'Error'
        return 'Deleted Successfully'
    except:
        return 'Please try again'

def DeleteEssay(ExamTitle, Question):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle).all()
    ExamID = 0
    ExamID = exam[0].ExamID
    Question_ = Essay.query.filter_by(exam_id=ExamID, Question=Question).all()
    try:
        db.session.delete(Question_[0])
        db.session.commit()
        try:
            DeleteILO = Question_[0].ILO
            DelILO = Ilo.query.filter_by(ILOContent = DeleteILO).all()
            db.session.delete(DelILO[0])
            db.session.commit()
        except:
            'Error'
        return 'Deleted Successfully'
    except:
        return 'Please try again'

def GetStudentsMCQ(ExamTitle):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle).all()
    ExamID = 0
    ExamID = exam[0].ExamID
    ExamQuestions = MCQ.query.filter_by(exam_id=ExamID).all()
    IDList = []
    QuestionList = []
    AnswerList = [] #List of list
    ModelAnswer = []
    Grade = []
    StudentIDList = [] #List of list
    MCQDict = collections.defaultdict(list)
    Counter = 0
    for ques in ExamQuestions:
        IDList.append(ques.QuestionID)
        QuestionList.append(ques.Question)
        ModelAnswer.append(ques.CorrectAnswer)
        Grade.append(ques.Grade)
        MCQDict[ques.ILO].append(Counter)
        Counter+=1
    for id in IDList:
        question = StudentMCQ.query.filter_by(mcq_id=id).all()
        OneQuestionAnswerList = []
        StudLocalIdList=[]
        for ques in question:
            StudLocalIdList.append(ques.student_id)
            OneQuestionAnswerList.append(ques.Answer)
        StudentIDList.append(StudLocalIdList)
        AnswerList.append(OneQuestionAnswerList)
    return QuestionList, ModelAnswer, Grade, AnswerList, StudentIDList, MCQDict

def GetStudentsComplete(ExamTitle):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle).all()
    ExamID = 0
    ExamID = exam[0].ExamID
    ExamQuestions = Complete.query.filter_by(exam_id=ExamID).all()
    IDList = []
    QuestionList = []
    AnswerList = [] #List of list
    ModelAnswer = []
    Grade = []
    StudentIDList = [] #List of list
    CompDict = collections.defaultdict(list)
    Counter = 0
    for ques in ExamQuestions:
        IDList.append(ques.QuestionID)
        QuestionList.append(ques.Question)
        ModelAnswer.append(ques.CorrectAnswer)
        Grade.append(ques.Grade)
        CompDict[ques.ILO].append(Counter)
        Counter+=1
    for id in IDList:
        question = StudentComplete.query.filter_by(complete_id=id).all()
        OneQuestionAnswerList = []
        StudLocalIdList=[]
        for ques in question:
            StudLocalIdList.append(ques.student_id)
            OneQuestionAnswerList.append(ques.Answer)
        StudentIDList.append(StudLocalIdList)
        AnswerList.append(OneQuestionAnswerList)
    return QuestionList, ModelAnswer, Grade, AnswerList, StudentIDList, CompDict

def GetStudentsTF(ExamTitle):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle).all()
    ExamID = 0
    ExamID = exam[0].ExamID
    ExamQuestions = Truefalse.query.filter_by(exam_id=ExamID).all()
    IDList = []
    QuestionList = []
    AnswerList = [] #List of list
    ModelAnswer = []
    Grade = []
    StudentIDList = [] #List of list
    TFDict = collections.defaultdict(list)
    Counter = 0
    for ques in ExamQuestions:
        IDList.append(ques.QuestionID)
        QuestionList.append(ques.Question)
        ModelAnswer.append(ques.CorrectAnswer)
        Grade.append(ques.Grade)
        TFDict[ques.ILO].append(Counter)
        Counter+=1
    for id in IDList:
        question = StudentTF.query.filter_by(tf_id=id).all()
        OneQuestionAnswerList = []
        StudLocalIdList=[]
        for ques in question:
            StudLocalIdList.append(ques.student_id)
            OneQuestionAnswerList.append(ques.Answer)
        StudentIDList.append(StudLocalIdList)
        AnswerList.append(OneQuestionAnswerList)
    return QuestionList, ModelAnswer, Grade, AnswerList, StudentIDList, TFDict

def GetStudentsEssay(ExamTitle):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle).all()
    ExamID = 0
    ExamID = exam[0].ExamID
    ExamQuestions = Essay.query.filter_by(exam_id=ExamID).all()
    IDList = []
    QuestionList = []
    AnswerList = [] #List of list
    ModelAnswer = []
    Grade = []
    StudentIDList = [] #List of list
    EssayDict = collections.defaultdict(list)
    Counter = 0
    for ques in ExamQuestions:
        IDList.append(ques.QuestionID)
        QuestionList.append(ques.Question)
        ModelAnswer.append(ques.CorrectAnswer)
        Grade.append(ques.Grade)
        EssayDict[ques.ILO].append(Counter)
        Counter+=1
    for id in IDList:
        question = StudentEssay.query.filter_by(essay_id=id).all()
        OneQuestionAnswerList = []
        StudLocalIdList=[]
        for ques in question:
            StudLocalIdList.append(ques.student_id)
            OneQuestionAnswerList.append(ques.Answer)
        StudentIDList.append(StudLocalIdList)
        AnswerList.append(OneQuestionAnswerList)
    return QuestionList, ModelAnswer, Grade, AnswerList, StudentIDList, EssayDict

def GetExamToEvaluate(ExamTitle):
    MCQQuestionList, MCQModelAnswer, MCQGrade, MCQAnswerList, MCQStudentIDList, MCQILO       = GetStudentsMCQ(ExamTitle)
    CompQuestionList, CompModelAnswer, CompGrade, CompAnswerList, CompStudentIDList, CompILO = GetStudentsComplete(ExamTitle)
    TFQuestionList, TFModelAnswer, TFGrade, TFAnswerList, TFStudentIDList, TFILO             = GetStudentsTF(ExamTitle)
    EssQuestionList, EssModelAnswer, EssGrade, EssAnswerList, EssStudentIDList, EssILO       = GetStudentsEssay(ExamTitle)
    return MCQQuestionList, MCQModelAnswer, MCQGrade, MCQAnswerList, MCQStudentIDList, CompQuestionList, CompModelAnswer, CompGrade, CompAnswerList, CompStudentIDList, TFQuestionList, TFModelAnswer, TFGrade, TFAnswerList, TFStudentIDList, EssQuestionList, EssModelAnswer, EssGrade, EssAnswerList, EssStudentIDList, MCQILO, CompILO, TFILO, EssILO

def GetInstName(username):
    name = Instructor.query.filter_by(InstructorUserName=username).all()
    return name[0].InstructorName, name[0].InstructorID

def GetInstUsername(id):
    username = Instructor.query.filter_by(InstructorID = id).all()
    return username[0].InstructorUserName
    
def GetStudName(username):
    name = Student.query.filter_by(StudentUserName=username).all()
    return name[0].StudentName, name[0].StudentID

def GetStudentsNamesByID(IdList):
    NameList=[]
    for id in IdList:
        stud = Student.query.filter_by(StudentID = id).all()
        if (stud):
            NameList.append(stud[0].StudentName)
    return NameList

def GetStudNamebyID(id):
    name = Student.query.filter_by(StudentID=id).all()
    return name[0].StudentUserName


#GetExamToEvaluate('ex')

# ess = Truefalse.query.filter_by(Question='tf1').all()
# print (Truefalse.query.filter_by(Question='tf1').all())
# db.session.delete(ess[0])
# db.session.commit()
# print (Truefalse.query.filter_by(Question='tf1').all())
# x=1

# db.drop_all()
# # #Database is already created, do not uncomment the next line
# db.create_all()

# db.drop_all()
# ins1=Instructor(InstructorID='1',InstructorUserName='ins1name',InstructorPassword='ins1pw')
# std1 = Student(StudentUserName='student1',StudentPassword='std1pw')
# ilo1 = Ilo(ILOContent='ILO1',instructor_id=1)
# exam1=Exam(ExamID='1', ExamTitle='exam1', instructor_id='1')
# comp1=Complete(Question='this is comp1', CorrectAnswer='1', Grade=10, ILO='ilo 1 ins 1', instructor_id=1, exam_id='1')
# mcq1 = MCQ(QuestionID=1, Question='first mcq', Answers='ajaja', CorrectAnswer='ILO1', Grade=10, ILO='adoad',instructor_id=1, exam_id=1 )
#tf1 = Truefalse( Question='first tf', CorrectAnswer='ILO1', Grade=10, ILO='adoad',instructor_id=1, exam_id=1)
#ess1=Essay( Question='first essay', CorrectAnswer='ILO1', Grade=10, ILO='adoad',instructor_id=1, exam_id=1)
# mcqques1 = StudentMCQ(student_id=1,exam_id=1,mcq_id=1, Answer='myans')
# ques2 = StudentComplete(student_id=1,exam_id=1,complete_id=1, Answer='myans')
# ques3 = StudentTF(student_id=1,exam_id=1,tf_id=1, Answer='myans')
# ques4 = StudentEssay(student_id=1,exam_id=1,essay_id=1, Answer='myans')


# db.create_all()

# db.session.add(ins1)
# db.session.add(std1)
# db.session.add(ilo1)
# db.session.add(exam1)
# db.session.add(comp1)
# db.session.add(mcq1)
# db.session.add(mcqques1)
# db.session.add(ques2)
# db.session.add(ques3)
# db.session.add(ques4)
# db.session.add(tf1)
# db.session.add(ess1)

# db.session.commit()
# print(StudentMCQ.query.all())
# print(StudentComplete.query.all())
# print(StudentEssay.query.all())
# print(StudentTF.query.all())

# GetComplete('exam1',1)
# GetEssay('exam1',1)
# GetTF('exam1',1)
# GetComplete('exam1',1)



x=1

# print(Ilo.query.all())
# print(MCQ.query.filter_by(ILO = 'ilo 1 ins 3').all())

# x=1
# print(StudentTakeExam.query.all())
# stud = StudentTakeExam.query.all()
# g=20
# for s in stud:
#     s.Grade=g
#     g+=10
#     db.session.commit()
#     print(StudentTakeExam.query.all())   

# print(Student.query.all()) #Display all the table
# print(Instructor.query.all()) #Display all the table
# print(Exam.query.all()) #Display all the table
# print(MCQ.query.all()) #Display all the table
# print(Complete.query.all()) #Display all the table
# print(Truefalse.query.all()) #Display all the table
# print(Essay.query.all()) #Display all the table

# print(ins1.Exams)
# print(ins2.Exams)

# print(exam1.mcq)
# print(exam1.complete)
# print(exam1.Truefalse)
# print(exam1.essay)

# print(exam2.mcq)
# print(exam2.complete)
# print(exam2.Truefalse)
# print(exam2.essay)

# print(exam3.mcq)
# print(exam3.complete)
# print(exam3.Truefalse)
# print(exam3.essay)

# exam = Exam.query.filter_by(ExamTitle='exam5')
# ExamID = 0
# for ex in exam:
#     ExamID = ex.ExamID
# print(MCQ.query.filter_by(exam_id=ExamID).all())

# exam = Exam.query.filter_by(ExamTitle='exam6')
# ExamID = 0
# for ex in exam:
#     ExamID = ex.ExamID
# print(Complete.query.filter_by(exam_id=ExamID).all())

# exam = Exam.query.filter_by(ExamTitle='exam7')
# ExamID = 0
# for ex in exam:
#     ExamID = ex.ExamID
# print(Truefalse.query.filter_by(exam_id=ExamID).all())

# exam = Exam.query.filter_by(ExamTitle='exam8')
# ExamID = 0
# for ex in exam:
#     ExamID = ex.ExamID
# print(Essay.query.filter_by(exam_id=ExamID).all())

# print(Exam.query.filter_by(ExamTitle='newExam').all())
# Exams = MCQ.query.filter_by(exam_id=2).all()
# print(Exams)
# for exam in Exams:
#     UpdateExamMCQ('new question','hello q', '', 'new ans', 'newExam')
#     print( MCQ.query.filter_by(exam_id=2).all())
#print(Exam.query.filter_by(instructor_id = 2).all())

# # # print(User.query.first()) #Display first entry
# # # print(User.query.filter_by(username='omar').all())
# # # print(User.query.filter_by(username='omar').first()) #get user with no list
# # # user=User.query.filter_by(username='omar').first()
# # # print(user.id)
# # # user=User.query.get(1) #Get user of id = 1
# # # print(user)
# # # print(post1.author)
# # # print(User.query.all()) #Display all the table
# # # db.drop_all()
# # # db.create_all()
# # # print(User.query.all()) #Display all the table


