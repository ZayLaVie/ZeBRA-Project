from flask import Flask, render_template, request, redirect, url_for, abort
from flask_bcrypt import Bcrypt
from src.models import user, db
from src.repositories.user_repository import user_repository_singleton

app = Flask(__name__)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://*************************************' # create user_account_schema in your MySQL local database and add info here. REMOVE BEFORE COMMIT!!!
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db.init_app(app)

bcrypt = Bcrypt(app)

@app.get('/login')
def login():
    return render_template('login.html')

@app.get('/')
def index(): 
    return render_template('index.html')

@app.get('/about-uniconx')
def about_uniconx(): 
    return render_template('about-uniconx.html')

@app.get('/contact-uniconx')
def contact_uniconx(): 
    return render_template('contact-uniconx.html')

@app.get('/users/new')
def create_account_form():
    return render_template('create_account_form.html', create_account_active=True)

@app.get('/registered_users')
def registered_users():
    all_users = user_repository_singleton.get_all_users()
    return render_template('registered_users.html', users=all_users)

@app.post('/users')
def create_user():
    first_name = request.form.get('first_name', '')
    last_name = request.form.get('last_name', '')
    email = request.form.get('email', '')
    password = request.form.get('password', '')

    if first_name == '' or last_name == '' or email == '' or password == '':
        abort(400)

    created_user = user_repository_singleton.create_user(first_name, last_name, email, password)

    if created_user:
        return redirect(f'/users/{created_user.user_id}')
    else:
        return {'error': 'User with the same email already exists'}, 400

@app.route('/create_account_redirect', methods=['POST'])
def create_account_redirect():
    return redirect(url_for('create_account_form'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)