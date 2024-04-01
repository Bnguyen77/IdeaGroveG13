from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from . import db


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    message_id = db.Column(db.Integer, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)