import os
import logging
import uuid
import hashlib
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "your-secret-key-here")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///college_events.db"
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize the app with the extension
db.init_app(app)

# Define models inline to avoid import issues
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    usn = db.Column(db.String(20), unique=True, nullable=False)
    year = db.Column(db.String(10), nullable=False)
    semester = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Student {self.name} - {self.usn}>'

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    rules = db.Column(db.Text, nullable=False)
    prize = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    venue = db.Column(db.String(200), nullable=False)
    lead_name = db.Column(db.String(100), nullable=False)
    lead_phone = db.Column(db.String(15), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Event {self.name}>'

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    ticket_code = db.Column(db.String(20), unique=True, nullable=False)
    blockchain_hash = db.Column(db.String(64), nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    student = db.relationship('Student', backref=db.backref('registrations', lazy=True))
    event = db.relationship('Event', backref=db.backref('registrations', lazy=True))

    def __repr__(self):
        return f'<Registration {self.ticket_code}>'

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registration_id = db.Column(db.Integer, db.ForeignKey('registration.id'), nullable=False)
    status = db.Column(db.String(20), default='Present')
    marked_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    registration = db.relationship('Registration', backref=db.backref('attendance', lazy=True))

    def __repr__(self):
        return f'<Attendance {self.status}>'

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Admin {self.username}>'

with app.app_context():
    db.create_all()

def simulate_blockchain_store(ticket_code, student_id, event_id):
    """Simulate blockchain storage by creating a hash"""
    data = f"{ticket_code}-{student_id}-{event_id}-{datetime.now().isoformat()}"
    blockchain_hash = hashlib.sha256(data.encode()).hexdigest()
    logging.info(f"Blockchain simulation: Stored hash {blockchain_hash} for ticket {ticket_code}")
    return blockchain_hash

def simulate_blockchain_verify(ticket_code, blockchain_hash):
    """Simulate blockchain verification"""
    # In a real blockchain, we would verify the hash exists on the blockchain
    # For simulation, we just check if the hash exists in our database
    registration = Registration.query.filter_by(ticket_code=ticket_code, blockchain_hash=blockchain_hash).first()
    return registration is not None

def mock_send_sms(phone_number, ticket_code):
    """Mock SMS sending - prints to console instead of real SMS"""
    message = f"Your event registration is confirmed! Ticket Code: {ticket_code}"
    logging.info(f"SMS Mock: Sending to {phone_number}: {message}")
    print(f"[SMS SENT] To: {phone_number} | Message: {message}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def student_register():
    if request.method == 'POST':
        name = request.form.get('name')
        usn_raw = request.form.get('usn')
        year = request.form.get('year')
        semester = request.form.get('semester')
        phone = request.form.get('phone')
        email = request.form.get('email')
        event_id = request.form.get('event_id')
        
        # Validate required fields
        if not all([name, usn_raw, year, semester, phone, email, event_id]):
            flash('All fields are required!', 'error')
            return render_template('student_register.html', events=Event.query.all())
        
        usn = usn_raw.upper()
        
        # Validate USN format
        if not usn.startswith('1KS'):
            flash('USN must start with "1KS"', 'error')
            return render_template('student_register.html', events=Event.query.all())
        
        # Check if student already exists
        student = Student.query.filter_by(usn=usn).first()
        if not student:
            student = Student(
                name=name, 
                usn=usn, 
                year=year, 
                semester=semester, 
                phone=phone, 
                email=email
            )
            db.session.add(student)
            db.session.commit()
        
        # Check if already registered for this event
        existing_registration = Registration.query.filter_by(student_id=student.id, event_id=event_id).first()
        if existing_registration:
            flash('You are already registered for this event!', 'error')
            return render_template('student_register.html', events=Event.query.all())
        
        # Generate unique ticket code
        ticket_code = str(uuid.uuid4())[:8].upper()
        
        # Simulate blockchain storage
        blockchain_hash = simulate_blockchain_store(ticket_code, student.id, event_id)
        
        # Create registration
        registration = Registration(
            student_id=student.id,
            event_id=int(event_id),
            ticket_code=ticket_code,
            blockchain_hash=blockchain_hash
        )
        db.session.add(registration)
        db.session.commit()
        
        # Mock SMS sending
        mock_send_sms(phone, ticket_code)
        
        flash(f'Registration successful! Your ticket code is: {ticket_code}', 'success')
        return redirect(url_for('events'))
    
    events = Event.query.all()
    return render_template('student_register.html', events=events)

@app.route('/events')
def events():
    events_list = Event.query.all()
    return render_template('events.html', events=events_list)

@app.route('/timetable')
def timetable():
    events_list = Event.query.order_by(Event.date, Event.time).all()
    return render_template('timetable.html', events=events_list)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Username and password are required!', 'error')
            return render_template('admin_login.html')
        
        admin = Admin.query.filter_by(username=username).first()
        
        if admin and check_password_hash(admin.password_hash, password):
            session['admin_id'] = admin.id
            session['admin_username'] = admin.username
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_id', None)
    session.pop('admin_username', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        flash('Please login to access admin dashboard', 'error')
        return redirect(url_for('admin_login'))
    
    events = Event.query.all()
    total_students = Student.query.count()
    total_registrations = Registration.query.count()
    total_events = Event.query.count()
    
    stats = {
        'total_students': total_students,
        'total_registrations': total_registrations,
        'total_events': total_events
    }
    
    return render_template('admin_dashboard.html', events=events, stats=stats)

@app.route('/admin/add_event', methods=['GET', 'POST'])
def add_event():
    if 'admin_id' not in session:
        flash('Please login to access this page', 'error')
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        rules = request.form.get('rules')
        prize = request.form.get('prize')
        date = request.form.get('date')
        time = request.form.get('time')
        venue = request.form.get('venue')
        lead_name = request.form.get('lead_name')
        lead_phone = request.form.get('lead_phone')
        
        # Validate required fields
        if not all([name, description, rules, prize, date, time, venue, lead_name, lead_phone]):
            flash('All fields are required!', 'error')
            return render_template('add_event.html')
        
        event = Event(
            name=name,
            description=description,
            rules=rules,
            prize=prize,
            date=date,
            time=time,
            venue=venue,
            lead_name=lead_name,
            lead_phone=lead_phone
        )
        
        db.session.add(event)
        db.session.commit()
        
        flash('Event added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('add_event.html')

@app.route('/admin/event/<int:event_id>/registrations')
def event_registrations(event_id):
    if 'admin_id' not in session:
        flash('Please login to access this page', 'error')
        return redirect(url_for('admin_login'))
    
    event = Event.query.get_or_404(event_id)
    registrations = db.session.query(Registration, Student).join(Student).filter(Registration.event_id == event_id).all()
    
    return render_template('event_registrations.html', event=event, registrations=registrations)

@app.route('/admin/attendance', methods=['GET', 'POST'])
def mark_attendance():
    if 'admin_id' not in session:
        flash('Please login to access this page', 'error')
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        ticket_code_raw = request.form.get('ticket_code')
        
        if not ticket_code_raw:
            flash('Ticket code is required!', 'error')
            return render_template('attendance.html')
        
        ticket_code = ticket_code_raw.upper()
        
        registration = Registration.query.filter_by(ticket_code=ticket_code).first()
        
        if not registration:
            flash('Invalid ticket code!', 'error')
            return render_template('attendance.html')
        
        # Verify with simulated blockchain
        if not simulate_blockchain_verify(ticket_code, registration.blockchain_hash):
            flash('Ticket verification failed!', 'error')
            return render_template('attendance.html')
        
        # Check if already marked
        existing_attendance = Attendance.query.filter_by(registration_id=registration.id).first()
        if existing_attendance:
            flash('Attendance already marked for this ticket!', 'warning')
            return render_template('attendance.html')
        
        # Mark attendance
        attendance = Attendance(registration_id=registration.id, status='Present')
        db.session.add(attendance)
        db.session.commit()
        
        student = Student.query.get(registration.student_id)
        event = Event.query.get(registration.event_id)
        
        if student and event:
            flash(f'Attendance marked for {student.name} (USN: {student.usn}) for event: {event.name}', 'success')
        else:
            flash('Attendance marked successfully!', 'success')
        return render_template('attendance.html')
    
    return render_template('attendance.html')

@app.route('/admin/delete_event/<int:event_id>')
def delete_event(event_id):
    if 'admin_id' not in session:
        flash('Please login to access this page', 'error')
        return redirect(url_for('admin_login'))
    
    event = Event.query.get_or_404(event_id)
    
    # Delete related registrations and attendance first
    registrations = Registration.query.filter_by(event_id=event_id).all()
    for reg in registrations:
        Attendance.query.filter_by(registration_id=reg.id).delete()
    Registration.query.filter_by(event_id=event_id).delete()
    
    # Delete the event
    db.session.delete(event)
    db.session.commit()
    
    flash('Event deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
