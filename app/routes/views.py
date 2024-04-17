from flask import render_template, Blueprint, session, redirect, url_for, request
from sqlalchemy import desc
from ..models.user import User
from ..models.tag import Tag
from ..models.post import Post
from ..models.message import Message


views = Blueprint("views", __name__)


@views.route("/", methods=["GET"])
def index():
    if 'user_id' in session:
        user_id = session.get('user_id')
        user = User.query.get(user_id)
        available_tags = Tag.query.all()
        user_skills = user.get_user_skills()

        # Extract category and order from request arguments
        category = request.args.get('category')
        order = request.args.get('order')

        # Apply filtering and ordering logic for posts
        if category == "your":
            posts = Post.query.filter_by(user_id=user_id).all()
        elif category == "other":
            posts = Post.query.filter(Post.user_id != user_id).all()
        elif category == "pending":
            posts = Post.get_post_by_sender_id(user_id=user_id, status= 0)
        elif category == "denied":
            posts = Post.get_post_by_sender_id(user_id=user_id, status= 2)
        elif category == "accepted":
            posts = Post.get_post_by_sender_id(user_id=user_id, status= 1)
    
        else:
            posts = Post.query.all()

        # Apply ordering if specified
        if order == "latest":
            posts = sorted(posts, key=lambda x: x.creation_date, reverse=True)
        elif order == "earliest":
            posts = sorted(posts, key=lambda x: x.creation_date)

        messages = Message.query.filter_by(recipient_id=user_id).all()

        return render_template("dashboard.html", user=user, available_tags=available_tags, messages=messages, posts=posts)
    else:
        return render_template("index.html")


@views.route("/user_route", methods=["GET"])
def user_route():
    if 'user_id' in session:
        return redirect(url_for("views.user"))
    else:
        return redirect(url_for("auth_controller.login"))


@views.route("/user", methods=["GET"])
def user():
    if 'user_id' in session:
        user_id = session.get('user_id')
        available_tags = Tag.query.all()
        user = User.query.get(user_id)

        return render_template("user.html", user=user, available_tags=available_tags)
    else:
        return redirect(url_for("auth_controller.login"))



@views.route("/project/<int:post_id>", methods=["GET"])
def project(post_id):
    # Check if the user is logged in
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        post = Post.query.get(post_id)
        if post:
            # Check if a status filter is provided in the request
            status_filter = request.args.get('messageFilter')
            if status_filter is not None:
                status_filter = int(status_filter)
                if status_filter == 0:
                    # Return messages with status 0 (pending)
                    messages = post.get_post_messages(status_filter=0)
                elif status_filter == 1:
                    # Return messages with status 1 (accepted)
                    messages = post.get_post_messages(status_filter=1)
                elif status_filter == 2:
                    # Return messages with status 2 (denied)
                    messages = post.get_post_messages(status_filter=2)
                else:
                    # Invalid status filter provided, return all messages
                    messages = post.get_post_messages()
            else:
                # If no status filter provided, get all messages
                messages = post.get_post_messages()
                
            return render_template("_project.html", post_id = post.id,  user = user, post=post, messages=messages)
    
    # If the user is not logged in or is not the author of the post, you can handle it accordingly
    # For example, you can redirect the user to a login page or display an error message
    return render_template("login.html")  # Return a forbidden error




