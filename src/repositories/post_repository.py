from src.models import db, Post

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

post_repository_singleton = PostRepository()