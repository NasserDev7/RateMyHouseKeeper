from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, RadioField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, NumberRange


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[Optional()])
    last_name = StringField('Last Name', validators=[Optional()])
    country = StringField('Country', validators=[Optional()])
    contact_email = StringField('Contact Email', validators=[Optional(), Email()])
    contact_number = StringField('Contact Number', validators=[Optional()])
    password = PasswordField('New Password', validators=[Optional()])
    submit = SubmitField('Update Profile')

class HousekeeperForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    passport_number = StringField('Passport Number', validators=[DataRequired()])
    nationality = StringField('Nationality', validators=[Optional()])
    working_countries = StringField('Working Countries', validators=[Optional()])
    note = TextAreaField('Note', validators=[Optional()])
    submit = SubmitField('Add Housekeeper')

class RatingForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    score = IntegerField("Score (1-5)", validators=[DataRequired(), NumberRange(min=1, max=5)])
    comment = TextAreaField("Comment", validators=[Optional()])
    submit = SubmitField("Submit Rating")

class LikeDislikeForm(FlaskForm):
    like = SubmitField('Like')
    dislike = SubmitField('Dislike')

class EvaluationForm(FlaskForm):
    choices = [(1, '1 - Poor'), (2, '2 - Fair'), (3, '3 - Good'), (4, '4 - Very Good'), (5, '5 - Excellent')]
    cleaning = SelectField('Cleaning', choices=choices, validators=[DataRequired()])
    timing = SelectField('Timing', choices=choices, validators=[DataRequired()])
    cooking = SelectField('Cooking', choices=choices, validators=[DataRequired()])
    childcare = SelectField('Childcare', choices=choices, validators=[DataRequired()])
    respect = SelectField('Respect', choices=choices, validators=[DataRequired()])
    submit = SubmitField('Submit Evaluation')