# College Event Management System (CEM)

A web application for managing college events. Students can browse upcoming events and register for them, and administrators can create, update and manage events from a dashboard.

**Live demo:** https://neeha.pythonanywhere.com

---

## Features

- Browse upcoming college events with date, venue and description
- Student registration for events with email validation
- Admin login with a dashboard to add, edit and delete events
- View registrations for each event
- Session-based authentication
- SQLite database managed through SQLAlchemy

## Tech Stack

| Layer      | Technology                         |
|------------|------------------------------------|
| Backend    | Python, Flask                      |
| Database   | SQLite, Flask-SQLAlchemy           |
| Frontend   | HTML, CSS, Jinja2 templates        |
| Validation | email-validator                    |
| Hosting    | PythonAnywhere                     |

## Project Structure

```
CEM/
├── app.py          # Flask app, models and routes
├── main.py         # Local entry point
├── init_db.py      # Creates the database, admin account and sample events
├── templates/      # Jinja2 HTML templates
├── static/         # CSS, JS and images
└── README.md
```

## Getting Started (Local Setup)

### Prerequisites

- Python 3.10 or later
- pip

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/CEM.git
   cd CEM
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS / Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install flask flask-sqlalchemy email-validator
   ```

4. Set the session secret:
   ```bash
   # Windows (PowerShell)
   $env:SESSION_SECRET="any-random-string"
   # macOS / Linux
   export SESSION_SECRET=any-random-string
   ```

5. Initialise the database:
   ```bash
   python init_db.py
   ```
   This creates the database, a default admin account and 4 sample events.

6. Run the app:
   ```bash
   python main.py
   ```
   Open http://127.0.0.1:5000 in your browser.

### Default Admin Login

| Username | Password   |
|----------|------------|
| admin    | admin123   |

> Change the default admin password before using this in a real setting.

## Deployment (PythonAnywhere)

1. Open a Bash console and clone the repo into `/home/<username>/CEM`.
2. Create a virtualenv and install the dependencies listed above.
3. Run `python init_db.py` once.
4. In the **Web** tab, add a new web app with **Manual configuration** (Python 3.12).
5. Set **Source code** and **Working directory** to `/home/<username>/CEM`, and **Virtualenv** to your virtualenv path.
6. Replace the contents of the WSGI file with:
   ```python
   import sys, os
   sys.path.insert(0, '/home/<username>/CEM')
   os.environ['SESSION_SECRET'] = 'any-long-random-string'
   from app import app as application
   ```
7. Click **Reload** and open `https://<username>.pythonanywhere.com`.

Free PythonAnywhere apps must be renewed once a month from the Web tab (**Run until 1 month from today**) or they are disabled.

## Environment Variables

| Variable         | Purpose                                 |
|------------------|-----------------------------------------|
| `SESSION_SECRET` | Secret key used to sign Flask sessions  |

## Future Improvements

- Email notifications for event registrations
- Event categories, search and filters
- Export registrations to CSV
- Role-based access for event coordinators

## Author

**Neeharika Shakthivelan**
B.E. Computer Science and Engineering (ICB), K. S. Institute of Technology, Bengaluru

## License

This project was built for academic purposes. Feel free to use it for learning.
