from src.models import User, db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class UserRepository:
    def get_all_users(self):
        return User.query.all()
    
    def get_user_by_id(self, user_id):
        return User.query.get(user_id)

    def get_user_by_name(self, first_name, last_name):
        return User.query.filter_by(first_name=first_name, last_name=last_name).first()

    def create_user(self, first_name, last_name, email, password):
        # Hash the password before storing it
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(first_name=first_name, last_name=last_name, email=email, password=hashed_password)
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return None

        try:
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except Exception as e:
            # Handle the error, log it, and possibly rollback the session
            print(f"Error creating user: {e}")
            db.session.rollback()
            return None

    def authenticate_user(self, email, password):
        # Retrieve the user from the database based on the email
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return None

user_repository_singleton = UserRepository()
