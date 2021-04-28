from flask import Blueprint, render_template, flash
from flask_login import login_required, current_user

blog = Blueprint("blog", __name__)

@blog.route("/")
@blog.route("/index/")
def index():
    return render_template("index.html")

@blog.route("/profile/")
@login_required
def profile():
    return render_template("profile.html", name=current_user.name)