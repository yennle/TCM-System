from tcm import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Model
class User(db.Model, UserMixin):
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
    users = db.relationship(User)
    def __repr__(self):
        return f"Patient('{self.first_name}', '{self.last_name}')"
