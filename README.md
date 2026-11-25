# 🎓 College Event Management System

A Flask web application for managing college technical events. Students can browse events, register online and get a unique ticket code by SMS. Admins can manage events, check payments and mark attendance using blockchain-verified tickets.

Built for **K. S. Institute of Technology (KSIT), Bengaluru**. Only students with a USN starting with `1KS` can register.

🔗 **Live demo:** [neeha.pythonanywhere.com](https://neeha.pythonanywhere.com)

---

## ✨ Features

### Students
- View all events with date, time, venue, prize pool, fee, rules and coordinator contact
- Event timetable with important notes for participants
- Registration form with USN check (`1KS...`), email check and one registration per event
- Pay by UPI (with transaction ID) or cash (verified by an admin)
- Unique ticket code sent by SMS, used for attendance

### Admins
- Secure admin login
- Add and manage events
- View registrations and verify payments
- Mark attendance by checking ticket codes
- Tamper-proof tickets secured with a SHA-256 hash chain

---

## 🧰 Tech Stack

| Layer     | Technology                     |
|-----------|--------------------------------|
| Backend   | Python, Flask                  |
| Database  | SQLite, Flask-SQLAlchemy       |
| Frontend  | HTML, CSS, JavaScript, Jinja2  |
| Security  | Blockchain-style hashed tickets, Flask sessions |
| Hosting   | PythonAnywhere                 |

---

## 🗺️ Pages

| Route          | Description                                   |
|----------------|-----------------------------------------------|
| `/`            | Home page                                     |
| `/events`      | All events with details and rules             |
| `/timetable`   | Date-wise event schedule                      |
| `/register`    | Student registration and payment              |
| `/admin/login` | Admin login and dashboard                     |

---

## 📁 Project Structure

```
CollegeEventManagement/
├── app.py         # Flask app, models and routes
├── main.py        # Entry point for running locally
├── init_db.py     # Creates the database, admin account and sample events
├── templates/     # HTML templates
├── static/        # CSS, JS and images
└── README.md
```

---

## 💻 Run Locally

```bash
git clone https://github.com/neeha-04/CollegeEventManagement.git
cd CollegeEventManagement

python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

pip install flask flask-sqlalchemy email-validator

set SESSION_SECRET=any-random-string        # Windows
# export SESSION_SECRET=any-random-string   # macOS / Linux

python init_db.py
python main.py
```

Open **http://127.0.0.1:5000** in your browser.

**Demo admin login:** `admin` / `admin123`

---

## 🚀 Deployment

The app is hosted on **PythonAnywhere** using a manual WSGI configuration:

```python
import sys, os
sys.path.insert(0, '/home/<username>/CollegeEventManagement')
os.environ['SESSION_SECRET'] = 'any-long-random-string'
from app import app as application
```

---

## 🔮 Future Enhancements

- Razorpay payment gateway
- QR-code tickets
- Export registrations to Excel
- Automatic participation certificates

---

## 👩‍💻 Author

**Neeharika Shakthivelan**
B.E. Computer Science and Engineering (ICB), KSIT Bengaluru
GitHub: [@neeha-04](https://github.com/neeha-04)
