from flask import Blueprint, render_template, redirect, url_for, session, flash, request, jsonify
from ..models.user import User, db
from ..models.tag import Tag
from ..models.post import Post
from ..models.message import Message
from ..models.chat import Chat, ChatMember, ChatMessage
from datetime import datetime

chat_controller = Blueprint("chat_controller", __name__)


from flask import jsonify

@chat_controller.route("/get_chat_room", methods=["POST"])
def get_chat_room():
    post_id = request.json.get("postId")

    # Check if the chat room already exists
    chat_room = Chat.query.filter_by(post_id=post_id).first()

    if chat_room is None:
        # If the chat room doesn't exist, create a new one
        chat_room = create_chat_room(post_id)
    else:
        # Check if there are new collaborators and add them to the chat room
        add_new_collaborators(chat_room, post_id)

    # Prepare the chat data to send back in the response
    chat_data = {
        "exists": True,
        "current_user_id": session["user_id"],
        "post_title": Post.get_post_by_id(post_id=post_id).title,
        "chat_room_id": chat_room.id,
        "chat_members": [member.id for member in chat_room.members],
        "chat_messages": [message.serialize() for message in chat_room.messages]
    }
    return jsonify(chat_data)




@chat_controller.route("/add_message_to_chat", methods=["POST"])
def add_message_to_chat():
    try:
        # Step 1: Get the message content from the request data
        message_content = request.json.get('message')
        chat_room_id = request.json.get('chat_room_id')

        # Step 2: Add the message to the database
        if message_content:
            # Assuming you have a current user ID available in the session
            current_user_id = session.get('user_id')
            # Assuming you have access to the chat room ID in the session or from the frontend
            
            # Create a new ChatMessage instance
            new_message = ChatMessage(
                chat_id=chat_room_id,
                sender_id=current_user_id,
                content=message_content
            )

            # Add the new message to the database session and commit
            db.session.add(new_message)
            db.session.commit()

            # Step 3: Return a success response
            return jsonify({'success': True})
        else:
            # Return an error response if the message content is missing
            return jsonify({'success': False, 'error': 'Message content is missing'}), 400
    except Exception as e:
        # Return an error response if any exception occurs
        return jsonify({'success': False, 'error': str(e)}), 500
    
    

def create_chat_room(post_id):
    # Create a new chat room
    new_chat_room = Chat(post_id=post_id)
    db.session.add(new_chat_room)
    db.session.commit()

    # Add post owner as a member
    post = Post.query.get(post_id)
    if post:
        add_chat_member(new_chat_room, post.user_id)

    # Add collaborators as members
    for collaborator in post.collaborators:
        add_chat_member(new_chat_room, collaborator.id)

    return new_chat_room


def add_chat_member(chat_room, user_id):
    chat_member = ChatMember(chat_id=chat_room.id, user_id=user_id)
    db.session.add(chat_member)
    db.session.commit()


def add_new_collaborators(chat_room, post_id):
    post = Post.query.get(post_id)
    existing_members = [member.user_id for member in chat_room.members]

    # Find new collaborators not already in the chat room
    new_collaborators = [collaborator for collaborator in post.collaborators if collaborator.id not in existing_members]

    # Add new collaborators as members
    for collaborator in new_collaborators:
        add_chat_member(chat_room, collaborator.id)

        