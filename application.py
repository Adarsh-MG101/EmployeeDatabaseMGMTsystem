import pymysql
pymysql.install_as_MySQLdb()
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash 
from dotenv import load_dotenv
load_dotenv()
import os

application = Flask(__name__)
application.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
application.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application) 

# Authentication setup
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(application)

# Employee model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    salary = db.Column(db.Float, nullable=False)
    hire_date = db.Column(db.String(20), nullable=False)

# Admin user model (single admin demo)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@application.before_request
def create_tables():
    db.create_all()
    if not User.query.filter_by(username="admin").first():
        admin = User(username="admin", password=generate_password_hash("admin",method='pbkdf2:sha256'))  # store hashed password
        db.session.add(admin)
        db.session.commit()

@application.route('/')
def home():
    return redirect(url_for('login'))

@application.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()


        # Check if user already exists
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists!', 'danger')
            return redirect(url_for('register'))

        # Create new user with hashed password
        new_user = User(username=username)
        new_user.password = generate_password_hash(password, method='pbkdf2:sha256')
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@application.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        print(password)
        print(f"User found: {user.username}")
        if user:
            print(f"Stored hash: {user.password}")
            print(f"Password match: {check_password_hash(user.password, password)}")
        if user and check_password_hash(user.password, password)==False:
            login_user(user)         
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')


@application.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@application.route('/dashboard')
@login_required
def dashboard():
    employees = Employee.query.all()
    return render_template('dashboard.html', employees=employees)

@application.route('/employee/add', methods=['GET', 'POST'])
@login_required
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        department = request.form['department']
        email = request.form['email']
        salary = request.form['salary']
        hire_date = request.form['hire_date']
        emp = Employee(name=name, department=department, email=email, salary=salary, hire_date=hire_date)
        db.session.add(emp)
        db.session.commit()
        flash('Employee added successfully!','success')
        return redirect(url_for('dashboard'))
    return render_template('employee_form.html', action="Add", employee=None)

@application.route('/employee/edit/<int:emp_id>', methods=['GET', 'POST'])
@login_required
def edit_employee(emp_id):
    employee = Employee.query.get_or_404(emp_id)
    if request.method == 'POST':
        employee.name = request.form['name']
        employee.department = request.form['department']
        employee.email = request.form['email']
        employee.salary = request.form['salary']
        employee.hire_date = request.form['hire_date']
        db.session.commit()
        flash('Employee updated successfully!','success')
        return redirect(url_for('dashboard'))
    return render_template('employee_form.html', action="Edit", employee=employee)

@application.route('/employee/delete/<int:emp_id>', methods=['POST'])
@login_required
def delete_employee(emp_id):
    employee = Employee.query.get_or_404(emp_id)
    db.session.delete(employee)
    db.session.commit()
    flash('Employee deleted successfully!')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    if not os.path.exists("instance"):
        os.makedirs("instance")
    application.run(debug=True)
