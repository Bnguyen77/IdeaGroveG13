from flask import Blueprint, render_template, redirect, url_for, session, flash, request, jsonify
from ..models.user import User, db
from ..models.tag import Tag
from ..models.post import Post
from datetime import datetime



post_controller = Blueprint("post_controller", __name__)


@post_controller.route("/create_post", methods=["POST"])
def create_post():
    if 'user_id' in session:
        user_id = session['user_id']
        current_user = User.get_user_by_user_id(user_id=user_id)
    
        title = request.form.get("title")
        content = request.form.get("content") 
        is_question = request.form.get('is_question') == 'on'
        tag_ids = request.form.getlist('tags')
        
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        
        post = Post(title = title, content = content, is_question = is_question, user_id = current_user.id)
        post.tags = tags
        post.creation_date = datetime.now()
        
        db.session.add(post)
        db.session.commit()
        
        return redirect(url_for('views.index'))
    
    
@post_controller.route("/get_post_data/", methods=["POST"])
def get_post_data():
    if 'user_id' in session:
        user_id = session['user_id']
        current_user = User.get_user_by_user_id(user_id=user_id)
    
        title = request.form.get("title")
        content = request.form.get("content") 
        is_question = request.form.get('is_question') == 'on'
        tag_ids = request.form.getlist('tags')
        
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        
        post = Post(title = title, content = content, is_question = is_question, user_id = current_user.id)
        post.tags = tags
        post.creation_date = datetime.now()
        
        db.session.add(post)
        db.session.commit()
        
        return redirect(url_for('views.index'))
    

   