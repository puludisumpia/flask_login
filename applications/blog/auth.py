import random
import string

from flask import Blueprint, render_template, redirect, request, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required

from applications import mail, Message
from .forms import LoginForm, SignupForm, EmailForm, PasswordForm
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
                    password, 
                    method="sha256"
                )
            )
            db.session.add(new_user)
            db.session.commit()

            msg = Message(
                "Confirmation inscription",
                sender="votre_email@gmail.com",
                recipients=[email]
            )
            msg.body = f"""
                    Bonjour { name },
                    Toute l'équipe vous souhaite le bienvenu.
                    Voici vos identifiants de connexion:
                    Identifiant: { email }
                    Mot de passe: { password }
                """
            mail.send(msg)
            return redirect(url_for("auth.login"))
    else:
        form = SignupForm()
    return render_template("signup.html", form=form)

@auth.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("blog.index"))


@auth.route("/confirmation/")
def confirm_send():
    return render_template("confirmation.html")

@auth.route("/reset/", methods=("GET", "POST"))
def reset_password():
    form = EmailForm()
    if request.method == "POST":
        email = request.form.get("email")

        user = User.query.filter_by(email=email).first()

        if user:
            hash_code = "".join(random.choices(string.ascii_letters + string.digits, k=250))
            user.hash_code = hash_code
            db.session.commit()
            msg = Message(
                "Confirmation changement mot de passe",
                sender="votre_email@gmail.com",
                recipients=[email]
            )
            msg.body = f"""
                        Bonjour,
                        Nous avons réçu votre demande de réinitialisation de mot passe.
                        Nous vous invitons à suivre le lien ci-dessous pour rédefinir un
                        nouveau mot de passe.
                        http://localhost:5000/""" + user.hash_code
            mail.send(msg)

            flash("Un mail vous a été envoyé. veuillez votre adresse mail", "success")
            return render_template("confirmation.html")
            
        else:
            flash("Ce mail n'est pas connu, veuillez saisir le bon mail ou inscrivez-vous", "warning")
            form = EmailForm()
    else:
        form = EmailForm()
    return render_template("send_link.html", form=form)


@auth.route("/<string:hash_code>/", methods=("GET", "POST"))
def hascode(hash_code):
    form = PasswordForm()
    user = User.query.filter_by(hash_code=hash_code).first()
    if user:
        if request.method == "POST":
            password = request.form.get("password")
            cpassword = request.form.get("cpassword")

            if password == cpassword:
                user.password = generate_password_hash(password, method="sha256")
                user.hash_code = None
                db.session.commit()

                return redirect(url_for("auth.login"))
            else:
                flash("Les mots de passe ne correspondent pas", "warning")
                form = PasswordForm()
        else:
            form = PasswordForm()
    else:
        form = PasswordForm()
    return render_template("password_reset.html", form=form)
