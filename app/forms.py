from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,PasswordField,SubmitField,EmailField
from wtforms.validators import DataRequired,EqualTo,ValidationError,Length
from app.models import User




class LoginForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired(),Length(max=64)])
    password = PasswordField("Password",validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Sign in")

class RegisterForm(FlaskForm):
    email = EmailField("Email",validators=[DataRequired(),Length(max=120)])
    username = StringField('Username',validators=[DataRequired(),Length(max=64)])
    password = PasswordField('password',validators=[DataRequired()])
    confirm_password = PasswordField('confirm your password',validators=[DataRequired(),EqualTo('password',"passwords don't match")])
    submit  =SubmitField("Register")


    #define functions to raise an error when a user name or an email is already in use

    def validate_username(self,given_username):
        user = User.query.filter_by(username = given_username.data).first()
        if user is not None:
            raise ValidationError('Username was taken,pleas user a different username.')
        
    def validate_email(self,given_email):
        user = User.query.filter_by(email = given_email.data).first()
        if user is not None:
            raise ValidationError('Email was taken,pleas user a different email.')
        


class PasswordResetForm(FlaskForm):
    password = PasswordField('Password',validators=[DataRequired()])
    confirm_password = PasswordField('confirm your password',validators=[DataRequired(),EqualTo('password',"passwords don't match")])
    submit  =SubmitField("Reset password")


class RequestResetForm(FlaskForm):
    email = EmailField("Email",validators=[DataRequired(),Length(max=120)])
    submit  =SubmitField("Request reset")


class SearchForm(FlaskForm):
    searched = StringField("searched",validators=[DataRequired()])
    submit  =SubmitField("Search user")