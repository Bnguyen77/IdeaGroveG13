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
    tags = db.relationship('Tag', secondary='post_tag',
                           backref=db.backref('posts', lazy=True))

    collaborators = db.relationship('User', secondary='post_collaborator',
                                    backref=db.backref('collaborations', lazy=True))
    
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
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def get_question_posts(cls):
        return cls.query.filter_by(is_question=True).all()

    @classmethod
    def get_collaboration_posts(cls):
        return cls.query.filter_by(is_question=False).all()

    @classmethod
    def get_most_related_posts(cls, user_skills):
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
    
  
    @classmethod   
    def get_post_by_sender_id (cls, user_id, status):
        from .message import Message
        return Post.query.join(Message, Message.post_id == Post.id).filter(Message.sender_id == user_id, Message.status == status).all()
    
    
    def has_user_sent_message(self, user_id):
        from .message import Message
        return Message.query.filter_by(sender_id=user_id, post_id=self.id).first() is not None
    
    def message_status(self, user_id):
        from .message import Message
        message = Message.query.filter_by(sender_id=user_id, post_id=self.id).first()
        if message:
            return message.status
        else:
            return None
        
    def message_status2(self, user_id, recipient_id):
        from .message import Message
        message = Message.query.filter_by(sender_id=user_id,recipient_id =recipient_id, post_id=self.id).first()
        if message:
            return message.status
        else:
            return None
                
    def is_status_message_undefined(self, user_id, recipient_id):
        from .message import Message
        message = Message.query.filter_by(sender_id=user_id,recipient_id =recipient_id, post_id=self.id).first()
        if message:
            return False
        else:
            return True
        
    def message_status_by_recipient(self, user_id):
        from .message import Message
        message = Message.query.filter_by(recipient_id=user_id, post_id=self.id).first()
        if message:
            return message.status
        else:
            return None
        
    def check_collab(self, user_id):
        # Iterate through collaborators to check if the user_id exists
        for collaborator in self.collaborators:
            if collaborator.id == user_id:
                return True
        return False

    
    def request_accepted(self, user_id):
        from .message import Message
        return Message.query.filter_by(sender_id=user_id, post_id=self.id).first() is not None


    def get_post_messages(self, status_filter=None):
        from .message import Message
        if status_filter is not None:
            # Filter messages based on the provided status filter
            messages = Message.query.filter_by(post_id=self.id, status=status_filter).all()
        else:
            # If no status filter provided, return all messages for the post
            messages = Message.query.filter_by(post_id=self.id).all()
        return messages
    



post_tag = db.Table('post_tag',
                    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                    )

# Define the association table for the many-to-many relationship between Post and User for collaborators
post_collaborator = db.Table('post_collaborator',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)