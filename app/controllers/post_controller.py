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
    
    
@post_controller.route('/filter_posts/<category>')
def get_posts(category):
    # Filter posts based on the selected category
    if category == 'all':
        posts = Post.query.all()
    elif category == 'latest':
        posts = Post.query.order_by(Post.creation_date.desc()).all()
    elif category == 'earliest':
        posts = Post.query.order_by(Post.creation_date).all()
    elif category == 'related':
        user_id = session['user_id']
        if user_id:
            current_user = User.query.get(user_id)
            user_skills = current_user.skills
            
            # Calculate similarity score for each post
            similarity_scores = {}
            for post in Post.query.all():
                post_tags = post.tags
                post_skill_names = [tag.name for tag in post_tags]
                similarity = len(set(user_skills) & set(post_skill_names)) / len(user_skills)
                similarity_scores[post.id] = similarity

            # Sort posts by similarity score
            sorted_post_ids = sorted(similarity_scores, key=similarity_scores.get, reverse=True)
            posts = [Post.query.get(post_id) for post_id in sorted_post_ids]
        else:
            # If the user is not logged in, return all posts
            posts = Post.query.all()
        

    # Render the filtered posts to a template and return it as a response
    return render_template('dashboard.html', posts=posts)
   