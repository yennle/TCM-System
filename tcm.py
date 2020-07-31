from datetime import datetime
from flask import Flask, render_template,url_for,flash,redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY']='2bcc64794f0d49b05f097a8729e353dd'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///tcm.db'

db=SQLAlchemy(app)
# Fake Data
from faker import Faker
from faker.providers import internet, phone_number, address, date_time
patients=[]
fake = Faker('en_US')
for _ in range(100):
    my_dict = {    'name': fake.name(),
                    'dob': fake.date_of_birth(),
                    'address': fake.street_address(),
                    'phone_number': fake.phone_number(),
                    'last_visited': fake.date_this_month(),
                 }
    patients.append(my_dict)
# Model
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    first_name = db.Column(db.String(30),nullable=False)
    last_name = db.Column(db.String(30),nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    modified_patient = db.relationship('Patient', backref='user_modified', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.first_name}', '{self.last_name}', '{self.image_file}')"


class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30),nullable=False)
    last_name = db.Column(db.String(30),nullable=False)
    birthday = db.Column(db.DateTime, nullable=False)
    gender = db.Column(db.Enum('M', 'F'))
    address = db.Column(db.String(100),nullable=False)
    city = db.Column(db.String(64))
    state = db.Column(db.String(2))
    zipcode = db.Column(db.String(9))
    phone_number = db.Column(db.String(100),nullable=False)
    lasted_visted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    upcoming_appt = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    modified_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # doctor = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    note = db.Column(db.Text)
    def __repr__(self):
        return f"Patient('{self.first_name}', '{self.last_name}')"




@app.route('/')
def home():
    return render_template('home.html',title="Home")
@app.route('/patients/search')
def search_patients():
    return render_template('/patients/search.html',title="Search Patients", patients=patients)
@app.route('/patients/test')
def test_patients():
    return render_template('/patients/symptom_test.html',title="Symptoms Test")
@app.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)
@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'admin' and form.password.data =='admin':
            flash(f'You have been logged in!','success')
            return redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessfull. Please check username and password!','danger')
    return render_template('login.html',title='Login',form=form)


if __name__=='__main__':
    app.run(debug=True)