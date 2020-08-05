import os
import secrets
import us
from PIL import Image
from flask import Flask, render_template, url_for, flash, redirect, request
from tcm import app, db, bcrypt
from tcm.forms import RegistrationForm, LoginForm, UpdateAccountForm, PatientForm
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
# def add_patients_db():
#     patients=[]
# fake = Faker('en_US')
# for _ in range(100):
#     my_dict = {    'name': fake.name(),
#                     'dob': fake.date_of_birth(),
#                     'address': fake.street_address(),
#                     'phone_number': fake.phone_number(),
#                     'last_visited': fake.date_this_month(),
#                  }
#     patients.append(my_dict)

# Home
@app.route('/home')
@login_required
def home():
    
    image_file= url_for('static',filename='img/profile_pics/'+current_user.image_file)
    return render_template('home.html',title="Home", image_file=image_file)

# Search Patient
@app.route('/patient/search')
@login_required
def search_patients():
    patients= Patient.query.all()
    image_file= url_for('static',filename='img/profile_pics/'+current_user.image_file)
    return render_template('/patients/search.html',title="Search Patients", patients=patients, image_file=image_file)

# Symptom Test
@app.route('/patient/test')
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

def save_picture(form_picture):
    random_hex =secrets.token_hex(8)
    _,f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex +f_ext
    picture_path = os.path.join(app.root_path,'static/img/profile_pics',picture_fn)
    
    # Resize image
    output_size =(512,512)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)
    return picture_fn

# Account
@app.route('/account',methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.first_name= form.first_name.data
        current_user.last_name= form.last_name.data
        current_user.username= form.username.data
        db.session.commit()
        flash(f'The account has been updated!.','success')
        return redirect(url_for('account'))
    elif request.method =='GET':
        form.first_name.data =current_user.first_name
        form.last_name.data =current_user.last_name
        form.username.data =current_user.username
    image_file= url_for('static',filename='img/profile_pics/'+current_user.image_file)
    return render_template('account.html',title='Account Profile', image_file=image_file, form=form)

@app.route('/patient/add',methods=['GET','POST'])
@login_required
def add_patient():
    form = PatientForm()
    form.state.choices = us.states.STATES
    if form.validate_on_submit():
        patient = Patient(first_name= form.first_name.data, last_name=form.last_name.data, birthday=form.birthday.data, 
                    gender=form.gender.data, address=form.address.data, city=form.city.data, state=form.state.data,
                    zipcode=form.zipcode.data, phone_number=form.phone_number.data,user_modified=current_user, note=form.note.data)
        db.session.add(patient)
        db.session.commit()
        flash(f'The patient has been added to database!.','success')
        return redirect(url_for('search_patients'))
    image_file= url_for('static',filename='img/profile_pics/'+current_user.image_file)
    return render_template('patients/add_patient.html',title='Add Patient', image_file=image_file, form=form)  