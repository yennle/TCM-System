from flask import Flask, render_template,url_for,flash,redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY']='2bcc64794f0d49b05f097a8729e353dd'

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