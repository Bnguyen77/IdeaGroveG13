from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from ..models.user import User

class LoginForm(FlaskForm):
    user_name = StringField("User name", validators=[DataRequired()],render_kw={"placeholder": "Enter your username"})
    password = PasswordField("password", validators=[DataRequired(),Length (8, 20)],render_kw={"placeholder": "Enter Password"})
    remember_me = BooleanField()


class RegisterForm(FlaskForm):
    user_name = StringField("User name", validators=[DataRequired()], render_kw={"placeholder": "Enter your username"})
    name = StringField("Name", validators=[DataRequired()],render_kw={"placeholder": "Your real name"})
    email = EmailField("Email", validators=[DataRequired(), Email()],render_kw={"placeholder": "Enter your email"})
    password = PasswordField("Password", validators=[
        DataRequired() ,
        EqualTo("repassword", message="Passwords must match"),
        Length (8, 20)
        ],render_kw={"placeholder": "Enter Password"})
    repassword = PasswordField("Confirm password", validators=[DataRequired()],render_kw={"placeholder": "Confirm Password"})
    
