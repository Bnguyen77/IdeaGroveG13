from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from ..models.user import User, db
from ..models.tag import Tag
from .forms import LoginForm, RegisterForm

auth_controller = Blueprint("auth_controller", __name__)


@auth_controller.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        existing_username = User.get_user_by_user_name(form.user_name.data)
        existing_email = User.get_user_by_email(form.email.data)
        if existing_email or existing_username:
            flash("Email or username has been used", "warning")
            return render_template("register.html", form=form)
        else:
            new_user = User(name=form.name.data, user_name=form.user_name.data,
                            email=form.email.data, password=form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash(
                f"Registration successful...please log in!: {new_user.name}", "success")
            return redirect(url_for('auth_controller.login'))
    else:
        if 'user_id' in session:
            return redirect(url_for('views.index'))
        return render_template("register.html", form=form)


@auth_controller.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        existing_username = User.get_user_by_user_name(form.user_name.data)
        if existing_username and existing_username.check_password(form.password.data):
            session['user_id'] = existing_username.id
            session['user_name'] = existing_username.user_name
            session['email'] = existing_username.email
            session['bio'] = existing_username.bio
            session.permanent = True
            flash('Login successful!', 'success')
            return redirect(url_for('views.index'))
        else:
            flash('Invalid username or password. Please try again.', 'warning')
            return render_template("login.html", form=form)
    else:
        if 'user_id' in session:
            return redirect(url_for('views.index'))
        return render_template("login.html", form=form)


@auth_controller.route("/logout")
def logout():
    if "user_id" in session:
        user = session["user_name"]
        session.pop("user_name", None)
        session.pop("user_id", None)
        flash(f"You have been logged out, {user}", "danger")
    else:
        flash(f"Invalid action", "warning")
    return redirect(url_for("views.index"))


@auth_controller.route("/add_bio", methods=["POST"])
def add_bio():
    if "user_id" in session:
        current_user = User.get_user_by_user_id(session['user_id'])
        # Check if 'bio' field exists in the form data
        if 'bio' in request.form:

            # handling bio
            current_user.bio = request.form['bio']
            session["bio"] = current_user.bio

            # handling tags for user skills
            selected_tag_ids = request.form.getlist('tags')
            selected_tags = Tag.query.filter(Tag.id.in_(selected_tag_ids)).all()
            current_user.skills = selected_tags
            
            db.session.commit()
            return redirect(url_for("views.user"))
        else:
            # Handle the case where 'bio' is not present in the form data
            flash("Bio field is missing in the form.")
            return redirect(url_for("views.user"))

    else:
        # Handle the case where 'user_id' is not in session
        flash("User not logged in.")
        return redirect(url_for("auth_controller.login"))
