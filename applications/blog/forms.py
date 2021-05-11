from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField

class LoginForm(FlaskForm):
    email = StringField("votre mail".upper())
    password = PasswordField(label="votre mot de passe".upper())
    remember_me = BooleanField(label="Se souvenir de moi")
    submit = SubmitField(label="Se connecter")


class SignupForm(FlaskForm):
    name = StringField(label="votre nom".upper())
    email = StringField("votre mail".upper())
    password = PasswordField(label="votre mot de passe".upper())
    submit = SubmitField(label="S'inscrire")


class EmailForm(FlaskForm):
    email = StringField(label="Votre mail".upper())
    submit = SubmitField(label="Envoyer")

class PasswordForm(FlaskForm):
    password = PasswordField(label="Votre nouveau mot de passe")
    cpassword = PasswordField(label="Confirmation mot de passe")
    submit = SubmitField(label="Modifier")

