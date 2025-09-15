Employee Management System
A Flask web application for managing employee records with login and registration features, built using MySQL, SQLAlchemy, and Flask-Login.

Features
User authentication (registration, login, logout, secure password storage)

CRUD operations for employee records: Add, Edit, Delete, View

Admin dashboard listing all employees

Flash messaging for user feedback

Responsive UI with custom styling

Tech Stack
Backend: Flask, Flask-SQLAlchemy, Flask-Login

Database: MySQL (using PyMySQL driver)

Frontend: HTML (Jinja templates), CSS

Project Structure
File / Folder	Description
application.py	Main Flask application with all route logic
templates/	Jinja HTML templates (dashboard, login, etc.)
static/style.css	Custom stylesheet
requirements.txt	Python dependencies
Prerequisites
Python 3.7+

MySQL Server (cloud or local)

pip

Local Setup Instructions
Clone the repository

bash
git clone <your-repo-url>
cd <your-repo-directory>
Set up a virtual environment

bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies

bash
pip install -r requirements.txt
Configure Environment Variables

Copy and edit sensitive values instead of storing credentials in the code.

Set:

SECRET_KEY

SQLALCHEMY_DATABASE_URI (e.g., mysql+pymysql://user:password@host/dbname)

bash
export SECRET_KEY=your_secret_key
export SQLALCHEMY_DATABASE_URI=your_database_uri
Run the Application

bash
flask run
or (if using the script directly)

bash
python application.py
Usage
Go to http://simpleemployeedatabasemanagement-env.eba-vjju9ktr.ap-south-1.elasticbeanstalk.com/dashboard in a web browser.

Register a new user or login as admin (admin/admin, unless changed).

Once logged in, access the dashboard to manage employees.

Main Files and Their Purpose
File	Purpose
application.py	Main flask app, routes, models, auth logic
templates/	HTML interfaces: login, register, dashboard
static/style.css	Styling for the app
Security & Best Practices
Never commit credentials (DB URI, secret keys) to source control; use environment variables.

Passwords are hashed using secure algorithms before storage.

Flask session secrets and DB credentials should be kept private.

In production, set debug=False and use a production-ready server.

Sample Users
Default admin is auto-created:

Username: admin
Password: admin (change after first login)

License
MIT License (or your preferred license)

Acknowledgements
Flask Documentation
SQLAlchemy Docs
Flask-Login Docs

Contact
For feedback, contact [officialamg100@gmail.com] or open an issue on the repository.