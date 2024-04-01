from flask import Blueprint, render_template, redirect, url_for, session, flash, request, jsonify
from ..models.user import User, db
from ..models.tag import Tag
from ..models.post import Post
from ..models.message import Message
from datetime import datetime



message_controller = Blueprint("message_controller", __name__)


@message_controller.route("/send_message", methods=["POST"])
def send_message():
    if 'user_id' in session:
        sender_id = session['user_id']
        recipient_id = request.form.get("recipient_id")
        message_content = request.form.get("message_content")
    
        if recipient_id and message_content:
            # Create the message
            message = Message(sender_id=sender_id, recipient_id=recipient_id, message_content=message_content)
            db.session.add(message)
            db.session.commit()
        
       
            flash('Message sent successfully!', 'success')
            return redirect(url_for('views.index'))
        else:
            flash('Error: Receiver ID and content are required.', 'error')
            return redirect(url_for('views.index'))
    else:
        flash('Please log in to send a message.', 'error')
        return redirect(url_for('auth_controller.login'))
    
