from flask import Blueprint, render_template, redirect, request, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required

from .forms import LoginForm, SignupForm
from .models import db, User

auth = Blueprint("auth", __name__)

@auth.route("/login/", methods=("GET", "POST"))
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        email = request.form.get("email")
        password = request.form.get("password")
        remember_me = True if request.form.get("remember_me") else False

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash(
                "Veuillez vérifier vos infomations de connexion, puis réessayer",
                "warning"
            )
            return redirect(url_for("auth.login"))
        else:
            login_user(user, remember=remember_me)
            return redirect(url_for("blog.profile"))
    else:
        form = LoginForm()
    return render_template("login.html", form=form)

@auth.route("/signup/", methods=("GET", "POST"))
def signup():
    form = SignupForm()
    if request.method == "POST" and form.validate_on_submit():
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user:
            flash("Cet utilisateur existe dejà", "warning")
            return redirect(url_for("auth.signup"))

        else:
            new_user = User(
                name=name,
                email=email,
                password=generate_password_hash(
                    password, method="sha256"
                )
            )
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for("auth.login"))
    else:
        form = SignupForm()
    return render_template("signup.html", form=form)

@auth.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("blog.index"))