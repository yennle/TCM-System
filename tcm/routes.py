import os
import secrets
import us
import datetime
from PIL import Image
from flask import Flask, render_template, url_for, flash, redirect, request, abort, jsonify, json
from tcm import app, db, bcrypt
from tcm.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                       PatientForm, UpdatePatientForm, PatientInfoForm, STATE_CHOICES, GENDER_CHOICES, SymptomForm, GroupForm, SubgroupForm)
from tcm.models import User, Patient, Test, PatientQuestion, TestResult
from flask_login import login_user, current_user, logout_user, login_required
import pandas as pd

# Fake Data
from faker import Faker
from faker.providers import internet, phone_number, address, date_time
patients = []
fake = Faker('en_US')
for _ in range(100):
    my_dict = {'name': fake.name(),
               'dob': fake.date_of_birth(),
               'address': fake.street_address(),
               'phone_number': fake.phone_number(),
               'last_visited': fake.date_this_month(),
               }
    patients.append(my_dict)


def add_patients_db():
    patients = Patient(first_name=fake.first_name(), last_name=fake.first_name(), birthday=fake.date_of_birth(),
                       gender=form.gender.data, address=form.address.data, city=form.city.data, state=form.state.data,
                       zipcode=form.zipcode.data, phone_number=form.phone_number.data, user_modified=current_user, note=form.note.data)
    # db.session.add(patient)
    # db.session.commit()

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

    image_file = url_for(
        'static', filename='img/profile_pics/'+current_user.image_file)
    return render_template('home.html', title="Home", image_file=image_file)


# Symptom Test
@app.route('/patient/test')
@login_required
def test_patients():
    return render_template('/patients/symptom_test.html', title="Symptoms Test")

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data, first_name=form.first_name.data,
                    last_name=form.last_name.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'The account has been created! You are now able to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# Login
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('search_patient'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('search_patient'))
        else:
            flash(f'Login Unsuccessfully. Please check username and password!', 'danger')
    return render_template('login.html', title='Login', form=form)

# Logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path, 'static/img/profile_pics', picture_fn)

    # Resize image
    output_size = (512, 512)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    i.save(picture_path)
    return picture_fn

# Account
@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.username = form.username.data
        db.session.commit()
        flash(f'The account has been updated!.', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.username.data = current_user.username
    image_file = url_for(
        'static', filename='img/profile_pics/'+current_user.image_file)
    return render_template('account.html', title='Account Profile', image_file=image_file, form=form)

#############################################
#                  PATIENT                  #
#############################################

# Search Patient
@app.route('/patient/search')
@login_required
def search_patient():
    patients = Patient.query.all()
    image_file = url_for(
        'static', filename='img/profile_pics/'+current_user.image_file)
    return render_template('/patients/search.html', title="Search Patients", patients=patients, image_file=image_file)


@app.route('/patient/add', methods=['GET', 'POST'])
@login_required
def add_patient():
    form = PatientForm()
    if form.validate_on_submit():
        patient = Patient(first_name=form.first_name.data, last_name=form.last_name.data, birthday=form.birthday.data,
                          gender=form.gender.data, address=form.address.data, city=form.city.data, state=form.state.data,
                          zipcode=form.zipcode.data, phone_number=form.phone_number.data, user_modified=current_user, note=form.note.data)
        db.session.add(patient)
        db.session.commit()
        flash(f'The patient has been added to database!.', 'success')
        return redirect(url_for('search_patient'))
    image_file = url_for(
        'static', filename='img/profile_pics/'+current_user.image_file)
    return render_template('patients/add_patient.html', title='Add Patient', image_file=image_file, form=form)


@app.route('/patient/<int:patient_id>', methods=['GET', 'POST'])
@login_required
def patient_info(patient_id):
    form = PatientInfoForm()
    image_file = url_for(
        'static', filename='img/profile_pics/'+current_user.image_file)
    patient = Patient.query.get_or_404(patient_id)
    # for test in patient.tests:
    #     print(test.test_datetime)
    # print(patient.tests)
    if request.method == 'GET':
        form.first_name.data = patient.first_name
        form.last_name.data = patient.last_name
        form.birthday.data = patient.birthday.strftime('%m/%d/%Y')
        form.gender.data = dict(GENDER_CHOICES).get(patient.gender)
        form.address.data = patient.address
        form.city.data = patient.city
        # form.state.data = dict(STATE_CHOICES).get(patient.state)
        form.state.data = patient.state
        form.zipcode.data = patient.zipcode
        form.phone_number.data = patient.phone_number
        form.note.data = patient.note
        patient_image = url_for(
            'static', filename='img/profile_pics/'+patient.image_file)
        # dict(form.state.choices).get(form.state.data)
    return render_template('patients/patient_info.html', title='Patient Information', image_file=image_file, patient=patient, form=form, patient_image=patient_image)


@app.route('/patient/<int:patient_id>/update', methods=['GET', 'POST'])
@login_required
def update_patient(patient_id):
    form = UpdatePatientForm()
    form.state.choices = us.states.STATES
    image_file = url_for(
        'static', filename='img/profile_pics/'+current_user.image_file)
    patient = Patient.query.get_or_404(patient_id)
    if patient.user_modified != current_user:
        abort(403)
    if form.validate_on_submit():
        patient.first_name = form.first_name.data
        patient.last_name = form.last_name.data
        patient.birthday = form.birthday.data
        patient.gender = form.gender.data
        patient.address = form.address.data
        patient.city = form.city.data
        patient.state = form.state.data
        patient.zipcode = form.zipcode.data
        patient.phone_number = form.phone_number.data
        patient.note = form.note.data
        patient.date_modified = datetime.datetime.now()
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            patient.image_file = picture_file
        db.session.commit()
        return redirect(url_for('patient_info', patient_id=patient.id))
    elif request.method == 'GET':
        form.first_name.data = patient.first_name
        form.last_name.data = patient.last_name
        form.birthday.data = patient.birthday
        form.gender.data = patient.gender
        form.address.data = patient.address
        form.city.data = patient.city
        form.state.data = patient.state
        form.zipcode.data = patient.zipcode
        form.phone_number.data = patient.phone_number
        form.note.data = patient.note
    return render_template('patients/update_patient.html', title='Patient Information', image_file=image_file, patient=patient, form=form)


@app.route('/patient/<int:patient_id>/delete', methods=['POST'])
@login_required
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    if patient.user_modified != current_user:
        abort(403)
    db.session.delete(patient)
    db.session.commit()
    return redirect(url_for('search_patient'))


def load_question_to_database():
    # Load symptom from excel
    data = pd.read_excel('tcm/static/data/data_v5.xlsx', index_col=0)

    # Add to DataFrame
    df = pd.DataFrame(data)

    # Generate dataframe to json
    df.to_json('tcm/static/data/symptom_json.json', orient='split')
    # Opening a file with the encoding set to utf-8 for chinese characters
    with open('tcm/static/data/symptom_json.json', 'w', encoding='utf-8') as file:
        df.to_json(file, orient='records', force_ascii=False)

    # Load encode file to json variable
    with open('tcm/static/data/symptom_json.json', 'r', encoding='utf-8') as f:
        symptoms = json.load(f)
    # print(symptoms)

    # Add symtoms from json file to database
    questions = []
    # Clear data in database
    currentQuestion = PatientQuestion.query.all()
    if(currentQuestion):
        PatientQuestion.query.delete()

    for symptom in symptoms:
        print(symptom)
        question = PatientQuestion(feature_number=symptom['Feature Number'], feature=symptom['Feature'], question=symptom['English question'],
                                   category=symptom['Category'], subgroup=symptom['Subgroup'], group=symptom['Group'], element_number=symptom['Element Number'])
        questions.append(question)
    db.session.add_all(questions)
    db.session.commit()


@app.route('/survey/result/<int:test_id>', methods=["POST"])
def save_test_result(test_id):
    # Get the target test
    target_test = Test.query.get_or_404(test_id)
    target_test.is_completed = True
    db.session.commit()
    # Retrieve the test result
    test_results = request.get_json()
    # Save the result tp database
    # rresults= TestResult.query.filter_by(test_id=test_id).all()
    # print(rresults)
    # q.append(question.as_dict())
    results = []
    for result in test_results:
        # print('Result:', result)
        # if(result.feature_number == )
        target_result = TestResult.query.filter_by(
            test_id=target_test.id, element_number=result['element_number']).first()
        # print('Target result:',target_result)
        target_result.answer = result['answer']
        # print(target_result.answer)
        db.session.commit()
    # Update patient status:
    target_patient = Patient.query.filter_by(id=target_test.patient).first()
    print(target_patient)
    target_patient.status = 1
    db.session.commit()
    # results.append(answer)
    # print(results)
    # db.session.add_all(results)
    # db.session.commit()
    # print(results)
    # print(db.session.commit())
    return jsonify(test_results)


@app.route('/patient/', methods=['POST', 'GET'])
@login_required
def test_patient():
    patient_id = request.args.get('patient', 1, type=int)
    patient = Patient.query.get_or_404(patient_id)
    # page= request.args.get('page',1,type=int)

    # Load patient question from excel
    load_question_to_database()

    patient_questions = PatientQuestion.query.filter(
        PatientQuestion.category.in_(["P", "P/A"]))

    groups = []
    for group in db.session.query(PatientQuestion.group).filter(PatientQuestion.category.in_(["P", "P/A"])).distinct().all():
        group = str(group).split("'")[1]
        groups.append(group)

    # Create Test Result database
    all_questions = PatientQuestion.query.all()
    test = createTest(patient_id, all_questions)

    return render_template('patients/symptom_test.html', title='Patient Test', patient=patient, questions=patient_questions, groups=groups, test=test)


def createTest(patient_id, questionsList):
    test = Test(patient=patient_id, assinged_by=current_user.id)
    db.session.add(test)
    db.session.commit()
    # add questions to TestResult
    testResults = []
    for question in questionsList:
        answer = TestResult(test_id=test.id, feature_number=question.feature_number,
                            category=question.category, patient=patient_id, element_number=question.element_number)
        testResults.append(answer)
    # print(testResults)
    db.session.add_all(testResults)
    db.session.commit()
    return test


#############################################
#                ASSISTANT DOCTOR           #
#############################################

@app.route('/assistant/', methods=['GET', 'POST'])
@login_required
def examine_patient():
    patients = Patient.query.filter_by(status=1)
    # patients= Patient.query.all()
    image_file = url_for(
        'static', filename='img/profile_pics/'+current_user.image_file)

    return render_template('assistant_doctor/examine_search.html', title='Examine Patient', image_file=image_file, patients=patients)


@app.route('/assistant/<int:patient_id>', methods=['GET', 'POST'])
@login_required
def examine(patient_id):
    image_file = url_for(
        'static', filename='img/profile_pics/'+current_user.image_file)
    patient = Patient.query.get_or_404(patient_id)
    patient_image = url_for(
        'static', filename='img/profile_pics/'+patient.image_file)

    target_test = Test.query.filter_by(patient=patient_id).order_by(
        Test.test_datetime.desc()).first()
    # print(target_test.id)
    assistant_questions = PatientQuestion.query.filter(
        PatientQuestion.category.in_(["A"]))
    confirm_questions = PatientQuestion.query.filter(
        PatientQuestion.category.in_(["P/A"]))
    confirm_results = TestResult.query.filter_by(
        test_id=target_test.id, category='P/A')

    # print(target_test.id)
    # for i in confirm_results:
    #     print(i.category)
    # print('DONE')

    groups = []
    for group in db.session.query(PatientQuestion.group).filter(PatientQuestion.category.in_(["A"])).distinct().all():
        group = str(group).split("'")[1]
        groups.append(group)
    return render_template('assistant_doctor/examine.html', title='Examine Patient',
                           image_file=image_file, patient=patient, patient_image=patient_image,
                           assistant_questions=assistant_questions, groups=groups, confirm_questions=confirm_questions, confirm_results=confirm_results, target_test=target_test)


@app.route('/examine/result/<int:test_id>', methods=["POST"])
def save_examine_result(test_id):
    target_test = Test.query.get_or_404(test_id)
    # Retrieve the answer from client
    examine_results = request.get_json()
    # Save the result tp database
    results = []
    for result in examine_results:
        target_result = TestResult.query.filter_by(
            test_id=target_test.id, element_number=result['element_number']).first()
        # answer = TestResult(test_id =test_id, answer= result['answer'],feature_number= result['feature_number'], patient=target_test.patient, category= result['category'])
        print('Target result')
        target_result.answer = result['answer']
        db.session.commit()
    # Update patient status:
    target_patient = Patient.query.filter_by(id=target_test.patient).first()
    target_patient.status = 2
    db.session.commit()
    # TESTING
    # testing= TestResult.query.filter_by(test_id=target_test.id)
    # for t in testing:
    #     print(t)
    return jsonify(examine_results)
#############################################
#                SENIOR DOCTOR           #
#############################################


@app.route('/senior/', methods=['GET', 'POST'])
@login_required
def diagnose_patient():
    # patients= Patient.query.all()
    patients = Patient.query.filter_by(status=2)
    image_file = url_for(
        'static', filename='img/profile_pics/'+current_user.image_file)

    return render_template('senior_doctor/diagnosis_search.html', title='Diagnose Patient', image_file=image_file, patients=patients)


@app.route('/senior/<int:patient_id>', methods=['GET', 'POST'])
@login_required
def diagnosis(patient_id):
    image_file = url_for(
        'static', filename='img/profile_pics/'+current_user.image_file)
    patient = Patient.query.get_or_404(patient_id)
    patient_image = url_for(
        'static', filename='img/profile_pics/'+patient.image_file)
    target_test = Test.query.filter_by(patient=patient_id).order_by(
        Test.test_datetime.desc()).first()
    patient_groups = []
    for group in db.session.query(PatientQuestion.group).filter(PatientQuestion.category.in_(["P"])).distinct().all():
        group = str(group).split("'")[1]
        patient_groups.append(group)
    assistant_groups = []
    for group in db.session.query(PatientQuestion.group).filter(PatientQuestion.category.in_(["A"])).distinct().all():
        group = str(group).split("'")[1]
        assistant_groups.append(group)

    patient_questions = PatientQuestion.query.filter(
        PatientQuestion.category.in_(["P", "P/A"]))
    patient_result = TestResult.query.filter(TestResult.category.in_(
        ["P", "P/A"]), TestResult.test_id == target_test.id)
    assistant_questions = PatientQuestion.query.filter(
        PatientQuestion.category.in_(["A"]))
    assistant_result = TestResult.query.filter_by(
        test_id=target_test.id, category='A')

    return render_template('senior_doctor/diagnosis.html', title='Examine Patient',
                           image_file=image_file, patient=patient, patient_image=patient_image, assistant_groups=assistant_groups,
                           patient_groups=patient_groups, patient_result=patient_result, assistant_result=assistant_result,
                           patient_questions=patient_questions, assistant_questions=assistant_questions
                           )

    @app.route('/examine/result/<int:test_id>', methods=["POST"])
    def save__result(test_id):
        target_test = Test.query.get_or_404(test_id)
        # Retrieve the answer from client
        examine_results = request.get_json()
        # Save the result tp database
        results = []
        for result in examine_results:
            target_result = TestResult.query.filter_by(
                test_id=target_test.id, element_number=result['element_number']).first()
            # answer = TestResult(test_id =test_id, answer= result['answer'],feature_number= result['feature_number'], patient=target_test.patient, category= result['category'])
            print('Target result')
            target_result.answer = result['answer']
            db.session.commit()
        # Update patient status:
        target_patient = Patient.query.filter_by(
            id=target_test.patient).first()
        target_patient.status = 2
        db.session.commit()
        # TESTING
        # testing= TestResult.query.filter_by(test_id=target_test.id)
        # for t in testing:
        #     print(t)
        return jsonify(examine_results)
