from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ease.db'
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
    Exams = db.relationship('Exam', backref='put', lazy=True) #Instructor 1:many exams
    def __repr__(self):
        return f"('{self.InstructorUserName})"

class Exam(db.Model):
    ExamID        = db.Column(db.Integer,     primary_key=True)
    ExamTitle     = db.Column(db.String(100), nullable=False, unique=True)
    date_posted   = db.Column(db.DateTime,    nullable=False, default=datetime.utcnow)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.InstructorID'), nullable=False)
    mcq           = db.relationship('MCQ',          backref='has', lazy=True) #Exam 1:many  MCQ
    complete      = db.relationship('Complete',     backref='has', lazy=True) #Exam 1:many  MCQ
    trueandfalse  = db.relationship('TrueAndFalse', backref='has', lazy=True) #Exam 1:many  MCQ
    essay         = db.relationship('Essay',        backref='has', lazy=True) #Exam 1:many  MCQ
    def __repr__(self):
        return f"('{self.ExamTitle}', '{self.instructor_id}')"

class MCQ(db.Model):
    QuestionID    = db.Column(db.Integer, primary_key=True)
    Question      = db.Column(db.Text,    nullable=False)
    Answers       = db.Column(db.Text,    nullable=False) #will be separated by a slash for example
    CorrectAnswer = db.Column(db.Text,    nullable=False)
    exam_id       = db.Column(db.Integer, db.ForeignKey('exam.ExamID'), nullable=False)
    def __repr__(self):
        return f"('{self.Question}', '{self.Answers}', '{self.CorrectAnswer}')"

class Complete(db.Model):
    QuestionID    = db.Column(db.Integer, primary_key=True)
    Question      = db.Column(db.Text,    nullable=False) #2 texts will be separated by a slash for example
    CorrectAnswer = db.Column(db.Text,    nullable=False)
    exam_id       = db.Column(db.Integer, db.ForeignKey('exam.ExamID'), nullable=False)
    def __repr__(self):
        return f"('{self.Question}', '{self.CorrectAnswer}')"

class TrueAndFalse(db.Model):
    QuestionID    = db.Column(db.Integer, primary_key=True)
    Question      = db.Column(db.Text,    nullable=False) #2 texts will be separated by a slash for example
    CorrectAnswer = db.Column(db.Text,    nullable=False)
    exam_id       = db.Column(db.Integer, db.ForeignKey('exam.ExamID'), nullable=False)
    def __repr__(self):
        return f"('{self.Question}', '{self.CorrectAnswer}')"

class Essay(db.Model):
    QuestionID    = db.Column(db.Integer, primary_key=True)
    Question      = db.Column(db.Text,    nullable=False) #2 texts will be separated by a slash for example
    CorrectAnswer = db.Column(db.Text,    nullable=False)
    exam_id       = db.Column(db.Integer, db.ForeignKey('exam.ExamID'), nullable=False)
    def __repr__(self):
        return f"('{self.Question}', '{self.CorrectAnswer}')"

class StudentTakeExam(db.Model):
    student_id = db.Column(db.Integer, db.ForeignKey('student.StudentID'), primary_key=True)
    exam_id    = db.Column(db.Integer, db.ForeignKey('exam.ExamID'), primary_key=True)
    def __repr__(self):
        return f"('{self.student_id}', '{self.exam_id}')"

def GetExamByInstructorID(InstructorID):
    ExamList=[]
    Exams = Exam.query.filter_by(instructor_id = InstructorID).all()
    for exam in Exams:
        ExamList.append(exam.ExamTitle)

def CreateExamIfNotExist(Examtitle,InstructoidD):
    Exams = Exam.query.filter_by(ExamTitle = Examtitle).all()
    if (not Exams): #if it does not exist in the database
        try:
            NewExam = Exam(ExamTitle=Examtitle, instructor_id=InstructoidD)
            db.session.add(NewExam)
            db.session.commit()
            return 'Exam is added successfully'
        except:
            return 'There was an issue creating the exam'
    else:
        return 'ExamFound'

def AddMCQ(Question, Answers, CorrectAns,ExamTitle):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle)
    ExamID = 0
    for ex in exam:
        ExamID = ex.ExamID
    try:
        Question = MCQ(Question=Question, Answers=Answers, CorrectAnswer=CorrectAns, exam_id=ExamID)
        db.session.add(Question)
        db.session.commit()
        return 'MCQ question is added successfully'
    except:
        return 'There was an issue adding mcq'

def AddComplete(Question, CorrectAns,ExamTitle):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle)
    ExamID = 0
    for ex in exam:
        ExamID = ex.ExamID
    try:
        Question = Complete(Question=Question, CorrectAnswer=CorrectAns, exam_id=ExamID)
        db.session.add(Question)
        db.session.commit()
        return 'Complete question is added successfully'
    except:
        return 'There was an issue adding complete question'

def AddTrueFalse(Question, CorrectAns,ExamTitle):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle)
    ExamID = 0
    for ex in exam:
        ExamID = ex.ExamID
    try:
        Question = TrueAndFalse(Question=Question, CorrectAnswer=CorrectAns, exam_id=ExamID)
        db.session.add(Question)
        db.session.commit()
        return 'T&F question is added successfully'
    except:
        return 'There was an issue adding T&F question'

def AddEssay(Question, CorrectAns,ExamTitle):
    exam = Exam.query.filter_by(ExamTitle=ExamTitle)
    ExamID = 0
    for ex in exam:
        ExamID = ex.ExamID
    try:
        Question = Essay(Question=Question, CorrectAnswer=CorrectAns, exam_id=ExamID)
        db.session.add(Question)
        db.session.commit()
        return 'Essay question is added successfully'
    except:
        return 'There was an issue adding essay question'

# db.drop_all()
# #Database is already created, do not uncomment the next line
# db.create_all()

# stud1= Student(StudentID='1',StudentUserName='stud1',StudentPassword='stud1')
# stud2= Student(StudentID='2',StudentUserName='stud2',StudentPassword='stud2')

# ins1=Instructor(InstructorID='1',InstructorUserName='ins1name',InstructorPassword='ins1pw')
# ins2=Instructor(InstructorID='2',InstructorUserName='ins2name',InstructorPassword='ins2pw')

# exam1=Exam(ExamID='1', ExamTitle='exam1', instructor_id='1')
# exam2=Exam(ExamID='2', ExamTitle='exam2', instructor_id='2')
# exam3=Exam(ExamID='3', ExamTitle='exam3', instructor_id='1')

# mcq1=MCQ(Question='this is mcq1', Answers='1234', CorrectAnswer='1', exam_id='1')
# mcq2=MCQ(Question='this is mcq2', Answers='1234', CorrectAnswer='1', exam_id='1')

# comp1=Complete(Question='this is comp1', CorrectAnswer='1', exam_id='1')
# comp2=Complete(Question='this is comp2', CorrectAnswer='1', exam_id='3')

# tf1=TrueAndFalse(Question='this is tf1', CorrectAnswer='1', exam_id='1')
# tf2=TrueAndFalse(Question='this is tf2', CorrectAnswer='1', exam_id='3')

# mcq3=MCQ(Question='this is mcq3', Answers='1234', CorrectAnswer='1', exam_id='2')
# comp3=Complete(Question='this is comp3', CorrectAnswer='1', exam_id='2')
# tf3=TrueAndFalse(QuestionID='3', Question='this is tf3', CorrectAnswer='1', exam_id='2')
# essay3=Essay(Question='this is essay3', CorrectAnswer='1', exam_id='2')
# essay4=Essay(Question='this is essay4', CorrectAnswer='1', exam_id='2')

# stud1exam1=StudentTakeExam(student_id=1,exam_id='1')
# stud1exam3=StudentTakeExam(student_id=1,exam_id='3')
# stud2exam2=StudentTakeExam(student_id=2,exam_id='2')

# db.session.add(stud1)
# db.session.add(ins1)
# db.session.add(ins2)
# db.session.add(exam1)
# db.session.add(exam2)
# db.session.add(exam3)
# db.session.add(mcq1)
# db.session.add(mcq2)
# db.session.add(comp1)
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

# db.session.commit()
# print(StudentTakeExam.query.all())

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
