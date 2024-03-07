from flask import render_template, Blueprint, session, redirect, url_for, flash
from ..models.user import User
from ..models.tag import Tag


views = Blueprint("views", __name__)


@views.route("/", methods=["GET"])
def index():
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
        available_tags = Tag.query.all()
        return render_template("user.html",  available_tags=available_tags)
    else:
        return redirect(url_for("auth_controller.login"))


# @views.route("/flashT", methods = ["GET"])
# def flashT():
#     flash("TEST TEST TEST    !", "info")
#     return redirect (url_for ('views.index'))
