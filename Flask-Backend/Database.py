from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ease.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Student(db.Model):
    StudentID       = db.Column(db.Integer,    primary_key=True)
    StudentUserName = db.Column(db.String(50), unique=True, nullable=False)
    StudentPassword = db.Column(db.String(60), nullable=False)
    #email = db.Column(db.String(120), unique=True, nullable=False)
    #posts = db.relationship('Post', backref='author', lazy=True)
    def __repr__(self):
        return f"('{self.StudentUserName})"

class Instructor(db.Model):
    InstructorID       = db.Column(db.Integer,    primary_key=True)
    InstructorUserName = db.Column(db.String(50), unique=True, nullable=False)
    InstructorPassword = db.Column(db.String(60), nullable=False)
    Exams              = db.relationship('Exam', backref='put', lazy=True) #Instructor 1:many exams
    MCQS               = db.relationship('MCQ', backref='put', lazy=True) #Instructor 1:many MCQs
    Completes          = db.relationship('Complete', backref='put', lazy=True) #Instructor 1:many Complete
    TFS                = db.relationship('TrueAndFalse', backref='put', lazy=True) #Instructor 1:many TF
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
    trueandfalse  = db.relationship('TrueAndFalse', backref='has', lazy=True) #Exam 1:many  
    essay         = db.relationship('Essay',        backref='has', lazy=True) #Exam 1:many  
    def __repr__(self):
        return f"('{self.ExamID}','{self.ExamTitle}', '{self.instructor_id}')"

class MCQ(db.Model):
    QuestionID    = db.Column(db.Integer, primary_key=True)
    Question      = db.Column(db.Text,    nullable=False)
    Answers       = db.Column(db.Text,    nullable=False) #will be separated by a slash for example
    CorrectAnswer = db.Column(db.Text,    nullable=False)
    Grade         = db.Column(db.Integer, nullable=False)
    ILO           = db.Column(db.Text, db.ForeignKey('ilo.ILOContent'), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.InstructorID'), nullable=False)
    exam_id       = db.Column(db.Integer, db.ForeignKey('exam.ExamID'), nullable=False)
    #ilo_id        = db.Column(db.Integer, db.ForeignKey('iLO_.ILO_ID'), nullable=False)
    def __repr__(self):
        return f"('{self.Question}', '{self.Answers}', '{self.CorrectAnswer}', '{self.ILO}')"

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

class TrueAndFalse(db.Model):
    QuestionID    = db.Column(db.Integer, primary_key=True)
    Question      = db.Column(db.Text,    nullable=False) 
    CorrectAnswer = db.Column(db.Text,    nullable=False)
    Grade         = db.Column(db.Integer, nullable=False)
    ILO           = db.Column(db.Text, db.ForeignKey('ilo.ILOContent'), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.InstructorID'), nullable=False)
    exam_id       = db.Column(db.Integer, db.ForeignKey('exam.ExamID'), nullable=False)
    #ilo_id        = db.Column(db.Integer, db.ForeignKey('iLO_.ILO_ID'), nullable=False)
    def __repr__(self):
        return f"('{self.Question}', '{self.CorrectAnswer}', '{self.ILO}')"

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
        return f"('{self.Question}', '{self.CorrectAnswer}', '{self.ILO}')"

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

def GetExamByInstructorID(InstructorID):
    ExamList=[]
    Exams = Exam.query.filter_by(instructor_id = InstructorID).all()
    for exam in Exams:
        ExamList.append(exam.ExamTitle)
    return ExamList

def CreateExamIfNotExist(Examtitle,InstructoiD):
    Exams = Exam.query.filter_by(ExamTitle = Examtitle).all()
    if (not Exams): #if it does not exist in the database
        try:
            NewExam = Exam(ExamTitle=Examtitle, instructor_id=InstructoiD)
            db.session.add(NewExam)
            db.session.commit()
            return 'Exam is added successfully'
        except:
            return 'There was an issue creating the exam'
    else:
        return 'ExamFound'

def AddMCQ(Question, Answers, CorrectAns, Grade,ILO, ExamTitle, InstructorID):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle)
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

def UpdateMCQ(OldQuestion,NewQuestion, NewAnswers, NewCorrectAns, ExamTitle):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle).all()
    ExamID = 0
    for ex in exam:
        ExamID = ex.ExamID
    question = MCQ.query.filter_by(Question=OldQuestion, exam_id=ExamID).all()
    for ex in question:
        if (NewQuestion != ''):
            try:
                ex.Question=NewQuestion
                db.session.commit()
            except:
                return 'There was an issue Updating mcq question'
        if (NewAnswers!=''):
            try:
                ex.Answers=NewAnswers
                db.session.commit()
            except:
                return 'There was an issue Updating mcq options'
        if (NewCorrectAns!=''):
            try:
                ex.CorrectAnswer=NewCorrectAns
                db.session.commit()
            except:
                return 'There was an issue Updating mcq correct answer'
        return 'Mcq is updated successfully'

def AddComplete(Question, CorrectAns,Grade, ILO, ExamTitle, InstructorID):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle)
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
                    
def UpdateComplete(OldQuestion,NewQuestion, NewCorrectAns, ExamTitle):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle).all()
    ExamID = 0
    for ex in exam:
        ExamID = ex.ExamID
    question = Complete.query.filter_by(Question=OldQuestion, exam_id=ExamID).all()
    for ex in question:
        if (NewQuestion != ''):
            try:
                ex.Question=NewQuestion
                db.session.commit()
            except:
                return 'There was an issue Updating complete question'
        if (NewCorrectAns!=''):
            try:
                ex.CorrectAnswer=NewCorrectAns
                db.session.commit()
            except:
                return 'There was an issue Updating complete correct answer'
        return 'Complete question is updated successfully'

def AddTrueFalse(Question, CorrectAns, Grade, ILO, ExamTitle, InstructorID):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle)
    ExamID = 0
    for ex in exam:
        ExamID = ex.ExamID
    QuestionExist = TrueAndFalse.query.filter_by(Question=Question, exam_id=ExamID).all()
    if (QuestionExist):
        return 'Question already exists in the exam'
    try:
        question = TrueAndFalse(Question=Question, CorrectAnswer=CorrectAns,Grade=Grade, ILO=ILO, exam_id=ExamID, instructor_id=InstructorID)
        db.session.add(question)
        db.session.commit()
        return 'T&F question is added successfully'
    except:
        return 'There was an issue adding T&F question'

def UpdateTrueFalse(OldQuestion,NewQuestion, NewCorrectAns, ExamTitle):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle).all()
    ExamID = 0
    for ex in exam:
        ExamID = ex.ExamID
    question = TrueAndFalse.query.filter_by(Question=OldQuestion, exam_id=ExamID).all()
    for ex in question:
        if (NewQuestion != ''):
            try:
                ex.Question=NewQuestion
                db.session.commit()
            except:
                return 'There was an issue Updating True False question'
        if (NewCorrectAns!=''):
            try:
                ex.CorrectAnswer=NewCorrectAns
                db.session.commit()
            except:
                return 'There was an issue Updating True False correct answer'
        return 'TF question is updated successfully'

def AddEssay(Question, CorrectAns, Grade, ILO, ExamTitle, InstructorID):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle)
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

def UpdateEssay(OldQuestion,NewQuestion, NewCorrectAns, ExamTitle):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle).all()
    ExamID = 0
    for ex in exam:
        ExamID = ex.ExamID
    question = Essay.query.filter_by(Question=OldQuestion, exam_id=ExamID).all()
    for ex in question:
        if (NewQuestion != ''):
            try:
                ex.Question=NewQuestion
                db.session.commit()
            except:
                return 'There was an issue Updating essay question'
        if (NewCorrectAns!=''):
            try:
                ex.CorrectAnswer=NewCorrectAns
                db.session.commit()
            except:
                return 'There was an issue Updating essay correct answer'
        return 'Essay question is updated successfully'

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

def MixMCQ(ExamTitle, InstructorID, ILO, Number):
    Count=0
    Questions = MCQ.query.filter_by(ILO=ILO, instructor_id=InstructorID).all()
    for ques in Questions:
        Count+=1
    if (Count < Number):
        return "The existing questions with this ILO are less than the required number"
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
                    return 'There was an issue adding MCQ, please try again'
        return "MCQ is added successfully"

def MixComplete(ExamTitle, InstructorID, ILO, Number):
    Count=0
    Questions = Complete.query.filter_by(ILO=ILO, instructor_id=InstructorID).all()
    for ques in Questions:
        Count+=1
    if (Count < Number):
        return "The existing questions with this ILO are less than the required number"
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
                    return 'There was an issue adding Complete question, please try again'
        return "Complete question is added successfully"

def MixTF(ExamTitle, InstructorID, ILO, Number):
    Count=0
    Questions = TrueAndFalse.query.filter_by(ILO=ILO, instructor_id=InstructorID).all()
    for ques in Questions:
        Count+=1
    if (Count < Number):
        return "The existing questions with this ILO are less than the required number"
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
                    question   = TrueAndFalse(Question=Question, CorrectAnswer=CorrectAns,Grade=Grade, ILO=ILO, exam_id=ExamID, instructor_id=InstructorID)
                    db.session.add(question)
                    db.session.commit()
                    Count-=1
                except:
                    return 'There was an issue adding TF question, please try again'
        return "TF question is added successfully"

def MixEssay(ExamTitle, InstructorID, ILO, Number):
    Count=0
    Questions = Essay.query.filter_by(ILO=ILO, instructor_id=InstructorID).all()
    for ques in Questions:
        Count+=1
    if (Count < Number):
        return "The existing questions with this ILO are less than the required number"
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
                    return 'There was an issue adding essay question, please try again'
        return "Essay question is added successfully"

def GetILO(InstructorID):
    ILO_List = []
    ILOs = Ilo.query.filter_by(instructor_id = InstructorID).all()
    for ilo in ILOs:
        ILO_List.append(ilo.ILOContent)
    return ILO_List

ilo = Ilo.query.filter_by(instructor_id = 1).all()
comp = Complete.query.all()
tf = TrueAndFalse.query.all()
ess=Essay.query.all()
x=1
# db.drop_all()
# db.session.add(Ilo(ILOContent='ilo 1 ins 1',instructor_id=1))
# db.session.add(MCQ(Question='this is mcq1', Answers='1234', CorrectAnswer='1', ILO='ilo 1 ins 1', Grade=10, exam_id='1'))
# #db.session.add(Ilo(ILOContent='ilo 1 ins 1',instructor_id=2))
# db.session.commit()

# Exams = Instructor.query.all()
# print(Exams)
# x=1

# Exams = Exam.query.all()
# print(Exams)
# x=1

# Exams = TrueAndFalse.query.filter_by(exam_id='1').all()
# print(Exams)

# Exams = Essay.query.filter_by(exam_id='1').all()
# print(Exams)

# for exam in Exams:
#     print(UpdateEssay('essay5','hello q', 'new ans', 'exam1'))
#     print(Essay.query.filter_by(exam_id=1).all())
# Exams = TrueAndFalse.query.filter_by(exam_id=1).all()
# print(Exams)

# x=2



# db.drop_all()
# #Database is already created, do not uncomment the next line
#db.create_all()

# stud1= student(studentid='1',studentusername='stud1',studentpassword='stud1')
# stud2= student(studentid='2',studentusername='stud2',studentpassword='stud2')

#ins1=Instructor(InstructorID='1',InstructorUserName='ins1name',InstructorPassword='ins1pw')
# ins2=instructor(instructorid='2',instructorusername='ins2name',instructorpassword='ins2pw')

#ilo1 = Ilo(ILOContent='ilo 1 ins 1',instructor_id=1)
# ilo2 = ilo(ilocontent='ilo 2 ins 1',instructor_id=1)
# ilo3 = ilo(ilocontent='ilo 1 ins 2',instructor_id=2)
# ilo4 = ilo(ilocontent='ilo 2 ins 2',instructor_id=2)

#exam1=Exam(ExamID='1', ExamTitle='exam1', instructor_id='1')
# exam2=exam(examid='2', examtitle='exam2', instructor_id='2')
# exam3=exam(examid='3', examtitle='exam3', instructor_id='1')

# mcq1=mcq(question='this is mcq1', answers='1234', correctanswer='1', ilo='ilo 1 ins 1', grade=10, exam_id='1')
# mcq2=mcq(question='this is mcq2', answers='1234', correctanswer='1', ilo='ilo 1 ins 1', grade=10, exam_id='1')
# mcq3=mcq(question='this is mcq3', answers='1234', correctanswer='1', ilo='ilo 2 ins 2', grade=10, exam_id=2)


#comp1=Complete(Question='this is comp1', CorrectAnswer='1', Grade=10, ILO='ilo 1 ins 1', instructor_id=1, exam_id='1')
#comp2=complete(question='this is comp2', correctanswer='1', ilo='ilo 1 ins 1', grade=10, exam_id='3')

# tf1=trueandfalse(question='this is tf1', correctanswer='1',ilo='ilo', grade=10, exam_id='1')
# tf2=trueandfalse(question='this is tf2', correctanswer='1',ilo='ilo', grade=10, exam_id='3')

# mcq3=mcq(question='this is mcq3', answers='1234', correctanswer='1',ilo='ilo', grade=10, exam_id='2')
# comp3=complete(question='this is comp3', correctanswer='1',ilo='ilo', grade=10, exam_id='2')
# tf3=trueandfalse(questionid='3', question='this is tf3', correctanswer='1',ilo='ilo', grade=10, exam_id='2')


# stud1exam1=studenttakeexam(student_id=1,exam_id='1')
# stud1exam3=studenttakeexam(student_id=1,exam_id='3')
# stud2exam2=studenttakeexam(student_id=2,exam_id='2')

#db.session.add(ilo1)
# db.session.add(ilo2)
# db.session.add(ilo3)
# db.session.add(ilo4)
# db.session.add(stud1)
#db.session.add(ins1)
# db.session.add(ins2)
#db.session.add(exam1)
# db.session.add(exam2)
# db.session.add(exam3)
# db.session.add(mcq1)
# db.session.add(mcq2)
# db.session.add(mcq3)
#db.session.add(comp1)
# db.session.add(comp2)
# db.session.add(tf1)
# db.session.add(tf2)
# db.session.add(mcq3)
# db.session.add(comp3)
# db.session.add(tf3)
# db.session.add(essay3)
# db.session.add(essay4)
# db.session.add(stud1exam1)
# db.session.add(stud1exam3)
# db.session.add(stud2exam2)

#db.session.commit()

#MixComplete('new exam', 1, 'ilo 1 ins 1', 1)

#print(Complete.query.all())

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
# print(TrueAndFalse.query.all()) #Display all the table
# print(Essay.query.all()) #Display all the table

# print(ins1.Exams)
# print(ins2.Exams)

# print(exam1.mcq)
# print(exam1.complete)
# print(exam1.trueandfalse)
# print(exam1.essay)

# print(exam2.mcq)
# print(exam2.complete)
# print(exam2.trueandfalse)
# print(exam2.essay)

# print(exam3.mcq)
# print(exam3.complete)
# print(exam3.trueandfalse)
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
# print(TrueAndFalse.query.filter_by(exam_id=ExamID).all())

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

    
x=5
