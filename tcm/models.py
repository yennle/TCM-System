from tcm import db, login_manager
# from __main__ import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    first_name = db.Column(db.String(30),nullable=False)
    last_name = db.Column(db.String(30),nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    modified_patient = db.relationship('Patient', backref='user_modified', lazy=True)
    assign_tests = db.relationship('Test', backref='assigner', lazy=True)
    def __repr__(self):
        return f"User('{self.username}', '{self.first_name}', '{self.last_name}', '{self.image_file}')"

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30),nullable=False)
    last_name = db.Column(db.String(30),nullable=False)
    birthday = db.Column(db.DateTime, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(100),nullable=False)
    city = db.Column(db.String(64))
    state = db.Column(db.String(2))
    zipcode = db.Column(db.String(9))
    phone_number = db.Column(db.String(100),nullable=False)
    lasted_visted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    upcoming_appt = db.Column(db.DateTime, nullable=True)
    date_modified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modified_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # doctor = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    note = db.Column(db.Text)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    tests = db.relationship('Test', backref='tester', lazy=True)
    status = db.Column(db.Integer, default=0)
    # 1: 
    # 2:
    # 3: 
    def __repr__(self):
        return f"Patient('{self.first_name}', '{self.last_name}','{self.status}')"

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    patient = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    assinged_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_completed= db.Column(db.Boolean, nullable=False, default= False)
    is_examined = db.Column(db.Boolean, nullable=False, default= False)
    # patient_questions = db.relationship('PatientQuestion', backref='questions', lazy=True)

class PatientQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    element_number = db.Column(db.String(10), nullable= False)
    feature_number = db.Column(db.String(10), nullable= False)
    feature = db.Column(db.String(50), nullable= False)
    question = db.Column(db.String(100), nullable= False)
    category = db.Column(db.String(20), nullable=False)
    subgroup = db.Column(db.String(20), nullable=True)
    group= db.Column(db.String(20),  nullable=True)
    # answers = db.relationship('TestResult', backref='results', lazy=True)
    
    # test_id= db.Column(db.Integer, db.ForeignKey('test.id'), nullable=True)
    def __repr__(self):
        return f"PatientQuestion('{self.element_number}', '{self.question}')"

class TestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_id= db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)
    answer = db.Column(db.Boolean, nullable=True)
    # question =db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    element_number = db.Column(db.String(10), nullable= False)
    feature_number = db.Column(db.String(10), nullable= False)
    category = db.Column(db.String(20), nullable=False)
    patient = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    is_completed= db.Column(db.Boolean, nullable=False, default= False)
    is_confimred = db.Column(db.Boolean, nullable=False, default= False)
    def __repr__(self):
        return f"TestResult( Test ID: {self.test_id}, Patient: {self.patient},Element No: {self.element_number}, Category: {self.category} ,Answer: {self.answer})"




