"""
Initialize the database with sample data and admin account.
Run this script once to set up the system.
"""

import os
import sys
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Admin, Event

def create_admin_account():
    """Create default admin account"""
    with app.app_context():
        # Check if admin already exists
        existing_admin = Admin.query.filter_by(username='admin').first()
        if existing_admin:
            print("Admin account already exists!")
            return
        
        # Create new admin
        admin = Admin(
            username='admin',
            password_hash=generate_password_hash('admin123')
        )
        
        db.session.add(admin)
        db.session.commit()
        print("Admin account created successfully!")
        print("Username: admin")
        print("Password: admin123")

def create_sample_events():
    """Create sample events for demonstration"""
    with app.app_context():
        # Check if events already exist
        if Event.query.count() > 0:
            print("Sample events already exist!")
            return
        
        sample_events = [
            {
                'name': 'Tech Quiz Competition',
                'description': 'A challenging quiz competition covering various technology topics including programming, AI, and cybersecurity.',
                'rules': '1. Teams of 2-3 members allowed\n2. No external devices permitted\n3. Questions will be multiple choice and descriptive\n4. Duration: 2 hours\n5. Top 3 teams will be awarded',
                'prize': '₹15,000 (1st: ₹8,000, 2nd: ₹5,000, 3rd: ₹2,000)',
                'date': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d'),
                'time': '10:00',
                'venue': 'Main Auditorium',
                'lead_name': 'Dr. Rajesh Kumar',
                'lead_phone': '9876543210'
            },
            {
                'name': 'Coding Marathon',
                'description': 'A 6-hour coding competition where participants solve algorithmic problems and build innovative solutions.',
                'rules': '1. Individual participation only\n2. Any programming language allowed\n3. Internet access for documentation only\n4. Plagiarism will lead to disqualification\n5. Judged on correctness and efficiency',
                'prize': '₹25,000 (1st: ₹15,000, 2nd: ₹7,000, 3rd: ₹3,000)',
                'date': (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d'),
                'time': '09:00',
                'venue': 'Computer Science Lab',
                'lead_name': 'Prof. Priya Sharma',
                'lead_phone': '9765432109'
            },
            {
                'name': 'Project Showcase',
                'description': 'Present your innovative projects and compete with fellow students. Categories include Web Development, Mobile Apps, AI/ML, and Hardware.',
                'rules': '1. Teams of 1-4 members\n2. Project must be original work\n3. 10-minute presentation + 5-minute Q&A\n4. Working prototype required\n5. Judged on innovation, technical complexity, and presentation',
                'prize': '₹20,000 (1st: ₹12,000, 2nd: ₹5,000, 3rd: ₹3,000)',
                'date': (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d'),
                'time': '14:00',
                'venue': 'Seminar Hall',
                'lead_name': 'Dr. Arun Patel',
                'lead_phone': '9654321098'
            },
            {
                'name': 'Cybersecurity Workshop',
                'description': 'Hands-on workshop covering ethical hacking, network security, and cybersecurity best practices.',
                'rules': '1. Bring your own laptop\n2. Basic programming knowledge required\n3. Certificate will be provided\n4. Attendance mandatory for full duration\n5. No registration fee',
                'prize': 'Certificates and Goodies worth ₹2,000',
                'date': (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d'),
                'time': '11:00',
                'venue': 'IT Lab 1',
                'lead_name': 'Mr. Vikram Singh',
                'lead_phone': '9543210987'
            }
        ]
        
        for event_data in sample_events:
            event = Event(**event_data)
            db.session.add(event)
        
        db.session.commit()
        print(f"Created {len(sample_events)} sample events!")

def main():
    """Main function to initialize the database"""
    print("Initializing College Event Management System Database...")
    print("=" * 60)
    
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created!")
        
        # Create admin account
        create_admin_account()
        
        # Create sample events
        create_sample_events()
        
        print("=" * 60)
        print("Database initialization complete!")
        print("\nYou can now:")
        print("1. Run the application: python main.py")
        print("2. Login as admin with username: admin, password: admin123")
        print("3. Students can register using USN starting with '1KS'")
        print("4. Test ticket codes will be printed in console (SMS simulation)")

if __name__ == '__main__':
    main()
