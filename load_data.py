import csv
from datetime import datetime
from app import app
from models import db, Patient, User

def load_patients(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            doctor = User.query.filter_by(username=row['Doctor']).first()
            patient = Patient(
                name=row['Name'],
                age=int(row['Age']),
                gender=row['Gender'],
                blood_type=row['Blood Type'],
                medical_condition=row['Medical Condition'],
                date_of_admission=datetime.strptime(row['Date of Admission'], '%Y-%m-%d').date(),
                discharge_date=datetime.strptime(row['Discharge Date'], '%Y-%m-%d').date() if row['Discharge Date'] else None,
                doctor_id=doctor.id if doctor else None,
                hospital=row['Hospital'],
                insurance_provider=row['Insurance Provider'],
                billing_amount=float(row['Billing Amount']) if row['Billing Amount'] else 0.0,
                room_number=row['Room Number'],
                admission_type=row['Admission Type'],
                medication=row['Medication'],
                test_results=row['Test Results']
            )
            db.session.add(patient)
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        load_patients('data/patients.csv')
        print('Patients loaded successfully.')
