from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='staff')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    blood_type = db.Column(db.String(3), nullable=True)
    medical_condition = db.Column(db.String(255), nullable=True)
    date_of_admission = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    discharge_date = db.Column(db.Date, nullable=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    hospital = db.Column(db.String(100), nullable=True)
    insurance_provider = db.Column(db.String(100), nullable=True)
    billing_amount = db.Column(db.Float, nullable=True)
    room_number = db.Column(db.String(10), nullable=True)
    admission_type = db.Column(db.String(50), nullable=True)
    medication = db.Column(db.String(255), nullable=True)
    test_results = db.Column(db.Text, nullable=True)

    doctor = db.relationship('User', backref='patients')
class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    reason = db.Column(db.String(255), nullable=True)

    patient = db.relationship('Patient', backref='appointments')
    doctor = db.relationship('User', backref='appointments')