from src.models import Post, db

class PostRepository:

    def get_all_posts(self):
        return Post.query.all()

    def get_post_by_id(self, post_id):
        return Post.query.get(post_id)

    def create_post(self, user_id, title, post_date_time, content):
        new_post = Post(user_id=user_id, title=title, post_date_time=post_date_time, content=content)

        db.session.add(new_post)
        db.session.commit()
        return new_post

# Usage Example:

# Assume you have a Flask app and db initialized:
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'your_database_uri_here'
# db = SQLAlchemy(app)

# Create an instance of the repository and pass the db session
post_repository_singleton = PostRepository()

# Example of using the repository
# post_repository.create_post(user_id=1, title='My Post', post_date_time=datetime.now(), content='Content of the post')

# After performing operations, you can commit changes when needed
# db.session.commit()
