from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, Patient, Appointment

app_routes = Blueprint('app_routes', __name__)
login_manager = LoginManager()
login_manager.login_view = 'app_routes.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app_routes.route('/')
@app_routes.route('/home')
def home():
    return render_template('home.html')

@app_routes.route('/login', methods=['GET', 'POST'])
def login():
    # Add logic for user login
    pass

@app_routes.route('/register', methods=['GET', 'POST'])
def register():
    # Add logic for user registration
    pass

@app_routes.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app_routes.route('/appointments', methods=['GET', 'POST'])
@login_required
def appointments():
    if request.method == 'POST':
        patient_id = request.form.get('patient_id')
        doctor_id = request.form.get('doctor_id')
        date = request.form.get('date')
        time = request.form.get('time')
        reason = request.form.get('reason')

        new_appointment = Appointment(patient_id=patient_id, doctor_id=doctor_id, date=date, time=time, reason=reason)
        db.session.add(new_appointment)
        db.session.commit()
        flash('Appointment scheduled successfully!', 'success')
        return redirect(url_for('app_routes.appointments'))
    patients = Patient.query.all()
    doctors = User.query.filter_by(role='doctor').all()
    return render_template('appointments.html', patients=patients, doctors=doctors)

@app_routes.route('/search', methods=['GET'])
@login_required
def search():
    query = request.args.get('query')
    results = Patient.query.filter(Patient.name.like(f'%{query}%')).all()
    return render_template('search_results.html', results=results)

@app_routes.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('app_routes.home'))
    return render_template('admin_dashboard.html')

@app_routes.route('/patient/<int:id>')
@login_required
def patient_detail(id):
    patient = Patient.query.get_or_404(id)
    return render_template('patient_detail.html', patient=patient)
