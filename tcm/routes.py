from flask import Flask, render_template, url_for, flash, redirect, request
from tcm import app, db, bcrypt
from tcm.forms import RegistrationForm, LoginForm
from tcm.models import User, Patient
from flask_login import login_user, current_user, logout_user, login_required

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
# Home
@app.route('/home')
@login_required
def home():
    return render_template('home.html',title="Home")

# Search Patient
@app.route('/patients/search')
@login_required
def search_patients():
    return render_template('/patients/search.html',title="Search Patients", patients=patients)

# Symptom Test
@app.route('/patients/test')
@login_required
def test_patients():
    return render_template('/patients/symptom_test.html',title="Symptoms Test")

# Register
@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username= form.username.data, first_name= form.first_name.data, last_name= form.last_name.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'The account has been created! You are now able to log in.','success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register',form=form)

# Login
@app.route('/',methods=['GET','POST'])
@app.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login Unsuccessfully. Please check username and password!','danger')
    return render_template('login.html',title='Login',form=form)

#Logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# Account
@app.route('/account')
@login_required
def account():
    return render_template('account.html',title='Account Profile')