from . import db
from flask_avatars import Identicon
from flask import current_app
import os
import random
import string

def random_string(length=5, additional_string=''):
    random_part = ''.join(random.choices(string.ascii_letters, k=length))
    combined_string = random_part + additional_string
    combined_list = list(combined_string)
    random.shuffle(combined_list)
    return ''.join(combined_list)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    bio = db.Column(db.Text, nullable=True)  # Added bio field
    avatar = db.relationship('Avatar', backref='user', uselist=False)
    skills = db.relationship(
        'Tag', secondary='user_skills', backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return f"User(id={self.id}, user_name='{self.user_name}')"

    def check_password(self, password):
        return password == self.password

    @classmethod
    def get_user_by_user_name(cls, user_name):
        return User.query.filter_by(user_name=user_name).first()

    @classmethod
    def get_user_by_user_id(cls, user_id):
        return User.query.filter_by(id=user_id).first()

    @classmethod
    def get_user_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    
    def get_user_skills(self):
        return self.skills
    
    
    def add_skills(self, tag_ids):
        from .tag import Tag
        selected_tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        self.skills = selected_tags
        db.session.commit() 
    
    
    def generate_avatar(self):
    # Generate a random Identicon avatar URL
        avatar = Identicon()
        # Assuming you have a configuration variable for the save path
        path = current_app.config['AVATARS_SAVE_PATH']
        # Delete previous avatar files if they exist
        if self.avatar:
            previous_avatar_paths = [
                os.path.join(path, getattr(self.avatar, f'avatar_url_{size}'))
                for size in ['s', 'm', 'l']
            ]
            for previous_avatar_path in previous_avatar_paths:
                if os.path.exists(previous_avatar_path):
                    os.remove(previous_avatar_path)
        # Generate new avatar URLs for all three sizes
        fileNames = avatar.generate(text=random_string(5, self.user_name))
        # Assuming fileNames contains URLs for small, medium, and large avatars
        avatar_urls = fileNames[:3]
        # Create or update the avatar associated with the user
        if self.avatar:
            self.avatar.avatar_url_s, self.avatar.avatar_url_m, self.avatar.avatar_url_l = avatar_urls
        else:
            self.avatar = Avatar(
                user_id=self.id,
                avatar_url_s=avatar_urls[0],
                avatar_url_m=avatar_urls[1],
                avatar_url_l=avatar_urls[2]
            )
        db.session.commit()

   

class Avatar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id'), unique=True, nullable=False)
    avatar_url_s = db.Column(db.String(255), nullable=False)
    avatar_url_m = db.Column(db.String(255), nullable=False)
    avatar_url_l = db.Column(db.String(255), nullable=False)


users_skills = db.Table(
    'user_skills',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)
