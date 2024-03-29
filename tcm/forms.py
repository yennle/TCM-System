from flask_login import current_user
# from sqlalchemy import text
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DateField, SelectField,DateTimeField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from tcm.models import User
import us

#############################################
#                  USER                     #
#############################################
class RegistrationForm(FlaskForm):
    first_name = StringField('First Name',validators=[DataRequired()])
    last_name = StringField('Last Name',validators=[DataRequired()])
    username = StringField('Username',validators=[DataRequired(), Length(min=5, max=15)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user :
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(), Length(min=5, max=15)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    first_name = StringField('First Name',validators=[DataRequired()])
    last_name = StringField('Last Name',validators=[DataRequired()])
    username = StringField('Username',validators=[DataRequired(), Length(min=5, max=15)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update')

    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user :
                raise ValidationError('That username is taken. Please choose a different one.')

#############################################
#                  PATIENT                  #
#############################################

GENDER_CHOICES=[('M','Male'),('F','Female')]
STATE_CHOICES= [(s.abbr, s.name) for s in us.states.STATES]

class PatientForm(FlaskForm):
    first_name = StringField('First Name',validators=[DataRequired()])
    last_name = StringField('Last Name',validators=[DataRequired()])
    # birthday = DateTimeField('Date of Birth', format='%m/%d/%y', validators=[DataRequired()])
    birthday = DateField('Date of Birth', format='%Y-%m-%d', id="dob")
    gender = SelectField('Gender', choices = GENDER_CHOICES)
    address = StringField('Address',validators=[DataRequired()])
    city = StringField('City',validators=[DataRequired()])
    state = SelectField('State',choices=STATE_CHOICES, validators=[DataRequired()])
    zipcode = StringField('Zipcode', validators=[DataRequired(),Length(min=5,max=5)])
    phone_number = StringField('Phone Number',validators=[DataRequired()])
    note = TextAreaField('Note')
    submit = SubmitField('Add The Patient')
class PatientInfoForm(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    birthday = StringField('Date of Birth')
    gender = StringField('Gender')
    address = StringField('Address')
    city = StringField('City')
    state = StringField('State')
    zipcode = StringField('Zipcode')
    phone_number = StringField('Phone Number')
    note = TextAreaField('Note')
    lasted_visit = StringField('Lasted Visit')
    upcoming_appt = StringField('Upcoming Appointment')
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
class UpdatePatientForm(FlaskForm):
    first_name = StringField('First Name',validators=[DataRequired()])
    last_name = StringField('Last Name',validators=[DataRequired()])
    # birthday = DateTimeField('Date of Birth', format='%m/%d/%y', validators=[DataRequired()])
    birthday = DateField('Date of Birth', format='%Y-%m-%d', id="dob")
    gender = SelectField('Gender', choices=GENDER_CHOICES)
    address = StringField('Address',validators=[DataRequired()])
    city = StringField('City',validators=[DataRequired()])
    state = SelectField('State',choices=STATE_CHOICES, validators=[DataRequired()])
    zipcode = StringField('Zipcode', validators=[DataRequired(),Length(min=5,max=5)])
    phone_number = StringField('Phone Number',validators=[DataRequired()])
    note = TextAreaField('Note')
    lasted_visit = DateField('Lasted Visit', format='%Y-%m-%d')
    upcoming_appt = DateField('Upcoming Appointment', format='%Y-%m-%d')
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Update The Patient')

#############################################
#                  SYMPTOM                  #
#############################################
CATEGORY_CHOICE=[('P','Patient'),('A','Advanced')]
class GroupForm(FlaskForm):
    name = StringField('Group Name: ',validators=[DataRequired()])
class SubgroupForm(FlaskForm):
    name = StringField('Subgroup Name: ',validators=[DataRequired()])
    # group = SelectField('Group', choices=[(g.id, g.name) for g in Group.query.order_by(text('name'))], validators=[DataRequired()] )
    group = SelectField('Group', validators=[DataRequired()] )
    submit = SubmitField('Add Subgroup')
class SymptomForm(FlaskForm):
    feature_number = StringField('Feature Number',validators=[DataRequired()])
    feature = StringField('Feature',validators=[DataRequired()])
    question = TextAreaField('Question',validators=[DataRequired()])
    category = SelectField('Category',choices=CATEGORY_CHOICE, validators=[DataRequired()])
    group = SelectField('Group', validators=[DataRequired()] )
    #subgroup = SelectField('Subgroup', choices=[(g.id, g.name) for g in Subgroup.query.order_by(text('name'))], validators=[DataRequired()] )
    subgroup = SelectField('Subgroup', validators=[DataRequired()] )
    submit = SubmitField('Add Symptom')