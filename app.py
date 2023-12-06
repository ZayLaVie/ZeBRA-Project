from flask import Flask, render_template, request, redirect, url_for, abort, flash, session
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from src.models import User, Post, db
from src.repositories.user_repository import user_repository_singleton
from src.repositories.post_repository import post_repository_singleton
from datetime import datetime
from functools import wraps

app = Flask(__name__)
# Secret key for session security purposes.
# Obtain secret key from @asamsomb
app.secret_key = ''

login_manager = LoginManager(app)
# Sets 'login.html' for unauthorized users (not registered)
login_manager.login_view = 'login'

# Configure Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://' 
# Create 'user_account_schema' in your MySQL local database and add info here. REMOVE BEFORE COMMIT!!!
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db.init_app(app)

def login_required(view_func):
    @wraps(view_func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        return view_func(*args, **kwargs)
    return decorated_function

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # User Authentication
        user = user_repository_singleton.authenticate_user(email, password)

        if user:
            # Session variable to represent user log-in
            session['user_id'] = user.user_id
            login_user(user) # Log in user w/ Flask-Login
            return redirect(url_for('forum'))  # Redirect to the forum (protected)
        else:
            # Shows invalid credentials if user credentials are not recognized
            flash('Invalid credentials. Please try again.', 'danger')

    # Pass additional variable to template to indicate authentication status
    return render_template('login.html', authentication_failed=request.method == 'POST')

@app.route('/logout')
def logout():
    logout_user() # log out user w/ Flask-Login
    return redirect(url_for('login')) # Redirects to 'login.html'

# route to Home page
@app.get('/')
def index(): 
    return render_template('index.html')

# route to Rida forum page
@app.get('/forum_2')
def forum_2(): 
    return render_template('forum_2.html')

# Route to About Us page
@app.get('/about-uniconx')
def about_uniconx(): 
    return render_template('about-uniconx.html')

# Route to Contact Us page
@app.get('/contact-uniconx')
def contact_uniconx(): 
    return render_template('contact-uniconx.html')

# Route to Contact Us page
@app.get('/tech_portfolio')
@login_required
def tech_portfolio(): 
    return render_template('techPortfolio.html')

# Route to Create New Account form
@app.get('/users/new')
def create_account_form():
    return render_template('create_account_form.html', create_account_active=True)

@app.route('/unauthorized_access')
def unauthorized_access():
    return render_template('permission-denied.html')

# For dev purposes---routes to deletion of a user/account
@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get(user_id)

    if user:
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('registered_users'))
    else:
        # Handle case where the user does not exist
        return "User not found"
    
# For dev purposes---routes to deletion of a post
@app.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get(post_id)

    if not post:
        return "Post not found"
    
    if current_user.user_id == 32 or current_user.user_id == post.user_id:
        db.session.delete(post)
        db.session.commit()
        return redirect(url_for('forum'))
    else:
        return redirect(url_for('unauthorized_access'))

# For dev purposes---
# Displays all registered users while requiring users to be logged in.
# Users not registered cannot view registered users.

# admin@admin.com
# Admin2331$AdmiN#775389%
@app.get('/registered_users')
@login_required
def registered_users():
    if current_user.user_id != 32:
        return redirect(url_for('unauthorized_access'))

    all_users = user_repository_singleton.get_all_users()
    return render_template('registered_users.html', users=all_users)

# Requires users to be logged in to post on and view forums.
@app.route('/forum', methods=['GET', 'POST'])
def forum(): 
    print("Current User:", current_user)  # Debug Statement: Shows active user and activity.
    print("Session User ID:", session.get('user_id')) # Debug Statement: Shows active user and activity.

    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('Please Log In or Create an Account to post.', 'danger')
            return redirect(url_for('login'))

        title = request.form.get('title')
        content = request.form.get('content')

        # Assume user is already logged in, and user_id is available
        user_id = current_user.get_id()

        # Insert new post into the database via Flask-SQLAlchemy
        new_post = post_repository_singleton.create_post(user_id=user_id, title=title, post_date_time=datetime.now(), content=content)
        db.session.add(new_post)
        db.session.commit()

    # Get posts from the database using Flask-SQLAlchemy
    posts = db.session.query(Post, User.email).join(User, Post.user_id == User.user_id).all()

    return render_template('forum.html', posts=posts)

# Creates new user
@app.route('/users', methods=['POST'])
def create_user():
    first_name = request.form.get('first_name', '')
    last_name = request.form.get('last_name', '')
    email = request.form.get('email', '')
    password = request.form.get('password', '')

    if first_name == '' or last_name == '' or email == '' or password == '':
        abort(400)

    created_user = user_repository_singleton.create_user(first_name, last_name, email, password)

    if created_user:
        flash('Account Created Successfully!', 'success')
        return redirect(url_for('forum'))
    else:
        return {'error': 'User with the same email already exists'}, 400

# routes to redirect form on About Us page
@app.route('/create_account_redirect', methods=['POST'])
def create_account_redirect():
    return redirect(url_for('create_account_form'))

if __name__ == '__main__':
    db.create_all(bind='__all__', tables=[User.__table__, Post.__table__])
    app.run(debug=True)