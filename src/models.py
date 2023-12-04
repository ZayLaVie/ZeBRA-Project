from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    __table_args__ = {'schema': 'user_accounts_schema'}

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

    # Required methods for Flask-Login
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.user_id)

class Post(db.Model):
    __tablename__ = 'post'
    __table_args__ = {'schema': 'user_accounts_schema'}

    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    post_date_time = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __init__(self, user_id, title, post_date_time, content):
        self.user_id = user_id
        self.title = title
        self.post_date_time = post_date_time
        self.content = content

    @classmethod
    def get_user_id_by_email(cls, email):
        user = User.query.filter_by(email=email).first()
        if user:
            return user.user_id
        else:
            return None