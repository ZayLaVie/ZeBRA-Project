from src.models import user, db

class UserRepository:

    def get_user_by_name(self, first_name, last_name):
        return user.query.get(first_name, last_name)
    
    def create_user(self, first_name, last_name, email, password):
        new_user = user(first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return new_user
    
user_repository_singleton = UserRepository()