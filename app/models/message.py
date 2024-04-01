from . import db

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message_content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())

    sender = db.relationship('User', foreign_keys=[sender_id], backref=db.backref('sent_messages', lazy='dynamic'))
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref=db.backref('received_messages', lazy='dynamic'))

    def __repr__(self):
        return f"Message('{self.sender_id}', '{self.recipient_id}', '{self.timestamp}')"
    
    
    @classmethod
    def send_message(cls, sender_id, receiver_id, content):
        message = cls(sender_id=sender_id, receiver_id=receiver_id, content=content)
        db.session.add(message)
        db.session.commit()
        return message

    @classmethod
    def get_messages(cls, user_id):
        return cls.query.filter(db.or_(cls.sender_id == user_id, cls.receiver_id == user_id)).all()