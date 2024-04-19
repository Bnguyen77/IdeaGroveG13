from datetime import datetime
from . import db

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    messages = db.relationship('ChatMessage', backref='chat', lazy=True)
    members = db.relationship('ChatMember', backref='chat', lazy=True)

    def __repr__(self):
        return f"Chat('{self.id}')"


class ChatMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"ChatMember('{self.chat_id}', '{self.user_id}')"
    def serialize(self):
        """Return a dictionary representation of the ChatMessage object."""
        return {
            'id': self.id,
            'chat_id': self.chat_id,
            'user_id': self.user_id,
            'avatar_url': self.get_member_avatar()
        }
    
    def get_member_avatar(self):
        from .user import User
        # Assuming you have a User model with an 'avatar' attribute
        user = User.query.get(self.user_id)
        if user:
            return user.avatar.avatar_url_s
        return None


class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"ChatMessage('{self.chat_id}', '{self.sender_id}', '{self.timestamp}')"
    def serialize(self):
        """Return a dictionary representation of the ChatMessage object."""
        return {
            'id': self.id,
            'chat_id': self.chat_id,
            'sender_id': self.sender_id,
            'content': self.content,
            'avatar_url': self.get_member_avatar(),
            'sender_name': self.get_member_name(),
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')  # Convert timestamp to string
        }
        
    def get_member_avatar(self):
        from .user import User
        # Assuming you have a User model with an 'avatar' attribute
        user = User.query.get(self.sender_id)
        if user:
            return user.avatar.avatar_url_s
        return None
    
    def get_member_name(self):
        from .user import User
        # Assuming you have a User model with an 'avatar' attribute
        user = User.query.get(self.sender_id)
        if user:
            return user.name
        return None
