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
        post_id = request.form.get("post_id")
        message_content = request.form.get("message_content")
    
        if recipient_id and message_content:
            # Create the message
            message = Message(sender_id=sender_id, recipient_id=recipient_id, post_id = post_id, message_content=message_content)
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
    

@message_controller.route('/get_post_messages/<int:post_id>', methods=['GET'])
def get_post_messages(post_id):
    # Query the database to fetch messages for the given post ID
    messages = Message.query.filter_by(post_id=post_id).all()

    # Serialize the messages data into JSON format
    messages_data = [{'id': message.id, 'sender_name': message.sender.name, 'message_content': message.message_content} for message in messages]

    # Return the messages data as a JSON response
    return jsonify({'messages': messages_data})


@message_controller.route("/handle_message/<int:message_id>/<int:post_id>/<action>", methods=["POST"])
def handle_message(message_id,post_id, action):
    # Retrieve the message from the database
    message = Message.query.get(message_id)

    if action == 'accept':
        # Add the sender to the post's collaborators list
        post = message.post
        sender = message.sender
        post.collaborators.append(sender)
        message.status = 1 
        db.session.commit()
        flash('request accepted', 'success')
      

    elif action == 'deny':
        # Delete the message from the database
        message.status = 2
        db.session.commit()
        flash('request deny', 'success')
    

    elif action == 'delete':
        # Delete the message from the database
        db.session.delete(message)
        db.session.commit()
        flash('request delete', 'success')
        

    return redirect(url_for('views.project', post_id=post_id))