from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField
from wtforms.validators import InputRequired, Length, DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)]) # Username must be between 2 to 20 characters long
    email = StringField('Email', validators=[DataRequired(), Email()]) # checks if input is in a valid email format
    name = StringField('Name', validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    gender = RadioField('Gender', validators=[InputRequired()], choices=[('r1', 'Male'), ('r2', 'Female'), ('r3', 'Other')], render_kw={'required': True})
    password = PasswordField('Password', validators=[DataRequired(), Length(6)]) # Password must be at least 6 characters long
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')]) # confirmed password has to be equal to the password
    submit = SubmitField('Sign up')


class SubscribeForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    submit = SubmitField('Subscribe')



