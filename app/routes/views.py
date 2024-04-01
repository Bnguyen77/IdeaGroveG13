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
        posts = Post.query.all()
        user_skills = user.get_user_skills()

        # Apply filtering logic for posts
        category = request.args.get('category')
        if category == "related":
            posts = Post.get_most_related_posts(user_skills)
        elif category == "lastest":
            posts = Post.query.order_by(desc(Post.creation_date)).all()
        elif category == "earliest":
            posts = Post.query.order_by(Post.creation_date).all()
        else:
            posts = Post.query.order_by(desc(Post.creation_date)).all()

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
