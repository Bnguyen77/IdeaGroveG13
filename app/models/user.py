from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    bio = db.Column(db.Text, nullable=True)  # Added bio field
    skills = db.relationship('Tag', secondary='user_skills', backref=db.backref('users', lazy='dynamic'))

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


users_skills = db.Table(
    'user_skills',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
)
