from datetime import datetime
from . import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_question = db.Column(db.Boolean, default=True)

    # Relationships with user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('posts', lazy=True))
    
    # Relationships with tag
    tags = db.relationship('Tag', secondary='post_tag', backref=db.backref('posts', lazy=True))


    def __repr__(self):
        return f"Post(id={self.id}, title='{self.title}')"
    
    @classmethod
    def get_all_posts(cls):
        return cls.query.all()
    
    @classmethod    
    def get_post_by_id(cls, post_id):
        return cls.query.get(post_id)
    
    @classmethod
    def get_post_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id = user_id).all()
    
    @classmethod
    def get_question_posts (cls):
        return cls.query.filter_by(is_question = True).all()
    
    @classmethod
    def get_collaboration_posts (cls):
        return cls.query.filter_by(is_question = False).all()
    
    @classmethod
    def get_most_related_posts(cls,user_skills):
        # Retrieve all posts from the database
        all_posts = cls.query.all()

        # Calculate similarity scores for each post
        related_posts = []
        for post in cls.query.all():
            post_tags_id = set(tag.id for tag in post.tags)
            user_skills_id = set(skill.id for skill in user_skills)
            similarity_score = len(post_tags_id.intersection(user_skills_id))
            related_posts.append((post, similarity_score))

        # Sort the related posts based on the similarity score in descending order
        related_posts.sort(key=lambda x: x[1], reverse=True)

        # Extract only the Post objects from the sorted list
        sorted_posts = [post[0] for post in related_posts]
        return sorted_posts
    
    
    @classmethod
    def create_post(cls, title, content, user_id):
        new_post = cls(title=title, content=content, user_id=user_id)
        db.session.add(new_post)
        db.session.commit()
        return new_post
    

post_tag = db.Table('post_tag',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)