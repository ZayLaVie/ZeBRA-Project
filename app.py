from flask import Flask, render_template, request, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from src.models import user, db

app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:nemo8739@localhost:3306/user_accounts_schema' # create user_account_schema in your MySQL local database and add info here. REMOVE BEFORE COMMIT!!!
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

@app.get('/login')
def login():
    return render_template('login.html')

@app.get('/')
def index(): 
    return render_template('ZeBRA-Project/templates/index.html')

@app.get('/users/new')
def create_account_form():
    return render_template('create_account_form.html')

@app.get('/list_users')
def list_users():
    return render_template('list_users.html')

@app.get('/users')
def create_user():
    first_name = request.form.get('first_name', '')
    last_name = request.form.get('last_name', '')
    email = request.form.get('email', '')
    password = request.form.get('password', '')

    if first_name == '' or last_name == '' or email == '' or password == '':
        abort(400)
    created_user = user_repository_singleton.create_user(first_name, last_name, email, password)
    return redirect(f'/users/{created_user.user_id}')

@app.route('/create_account_form', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        email = request.form['email']
        password = request.form['password']

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Insert user into the database
        new_user = user(first_name=first_name, last_name=last_name, email=email, password=hashed_password)
        db.session.add(new_user)

        try:
            db.session.commit()
            return redirect(url_for('ZeBRA-Project/templates/index.html'))  # Redirect to login page after successful registration
        except IntegrityError:
            db.session.rollback()
            return render_template('create_account_form.html', error="Email already exists. Please choose another.")

    return render_template('create_account_form.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)