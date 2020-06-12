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
        return f"Student('{self.StudentUserName})"

class Instructor(db.Model):
    InstructorID       = db.Column(db.Integer,    primary_key=True)
    InstructorUserName = db.Column(db.String(50), unique=True, nullable=False)
    InstructorPassword = db.Column(db.String(60), nullable=False)
    Exams = db.relationship('Exam', backref='put', lazy=True) #Instructor 1:many exams
    def __repr__(self):
        return f"Instructor('{self.InstructorUserName})"

class Exam(db.Model):
    ExamID        = db.Column(db.Integer,     primary_key=True)
    ExamTitle     = db.Column(db.String(100), nullable=False)
    date_posted   = db.Column(db.DateTime,    nullable=False, default=datetime.utcnow)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.InstructorID'), nullable=False)
    mcq           = db.relationship('MCQ',          backref='has', lazy=True) #Exam 1:many  MCQ
    complete      = db.relationship('Complete',     backref='has', lazy=True) #Exam 1:many  MCQ
    trueandfalse  = db.relationship('TrueAndFalse', backref='has', lazy=True) #Exam 1:many  MCQ
    essay         = db.relationship('Essay',        backref='has', lazy=True) #Exam 1:many  MCQ
    def __repr__(self):
        return f"Exam('{self.ExamTitle}', '{self.instructor_id}')"

class MCQ(db.Model):
    QuestionID    = db.Column(db.Integer, primary_key=True)
    Question      = db.Column(db.Text,    nullable=False)
    Answers       = db.Column(db.Text,    nullable=False) #will be separated by a slash for example
    CorrectAnswer = db.Column(db.Text,    nullable=False)
    exam_id       = db.Column(db.Integer, db.ForeignKey('exam.ExamID'), nullable=False)
    def __repr__(self):
        return f"MCQ('{self.Question}', '{self.Answers}', '{self.CorrectAnswer}')"

class Complete(db.Model):
    QuestionID    = db.Column(db.Integer, primary_key=True)
    Question      = db.Column(db.Text,    nullable=False) #2 texts will be separated by a slash for example
    CorrectAnswer = db.Column(db.Text,    nullable=False)
    exam_id       = db.Column(db.Integer, db.ForeignKey('exam.ExamID'), nullable=False)
    def __repr__(self):
        return f"Complete('{self.Question}', '{self.CorrectAnswer}')"

class TrueAndFalse(db.Model):
    QuestionID    = db.Column(db.Integer, primary_key=True)
    Question      = db.Column(db.Text,    nullable=False) #2 texts will be separated by a slash for example
    CorrectAnswer = db.Column(db.Text,    nullable=False)
    exam_id       = db.Column(db.Integer, db.ForeignKey('exam.ExamID'), nullable=False)
    def __repr__(self):
        return f"TrueAndFalse('{self.Question}', '{self.CorrectAnswer}')"

class Essay(db.Model):
    QuestionID    = db.Column(db.Integer, primary_key=True)
    Question      = db.Column(db.Text,    nullable=False) #2 texts will be separated by a slash for example
    CorrectAnswer = db.Column(db.Text,    nullable=False)
    exam_id       = db.Column(db.Integer, db.ForeignKey('exam.ExamID'), nullable=False)
    def __repr__(self):
        return f"Essay('{self.Question}', '{self.CorrectAnswer}')"

#db.drop_all()
#Database is already created, do not uncomment the next line
#db.create_all()

# stud1= Student(StudentID='1',StudentUserName='stud1',StudentPassword='stud1')

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

# db.session.commit()

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
