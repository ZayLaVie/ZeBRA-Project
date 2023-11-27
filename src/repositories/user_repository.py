from src.models import user, db

class UserRepository:

    def get_all_users(self):
        return user.query.all()

    def get_user_by_name(self, first_name, last_name):
        return user.query.filter_by(first_name=first_name, last_name=last_name).first()
    
    def create_user(self, first_name, last_name, email, password):
        new_user = user(first_name=first_name, last_name=last_name, email=email, password=password)
        existing_user = user.query.filter_by(email=email).first()

        if existing_user:
            return None
        
        db.session.add(new_user)
        db.session.commit()
        return new_user
    
user_repository_singleton = UserRepository()