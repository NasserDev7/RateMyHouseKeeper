from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, RadioField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, NumberRange
import pycountry
from wtforms.widgets import ListWidget, CheckboxInput  # Import ListWidget and CheckboxInput

# Dynamically fetch country names
COUNTRIES = [(country.name, country.name) for country in pycountry.countries]

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
    country = SelectField("Country", choices=COUNTRIES, validators=[DataRequired()])
    contact_email = StringField('Contact Email', validators=[Optional(), Email()])
    contact_number = StringField('Contact Number', validators=[Optional()])
    password = PasswordField('New Password', validators=[Optional()])
    submit = SubmitField('Update Profile')


class HousekeeperForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    passport_number = StringField('Passport Number', validators=[DataRequired()])
    nationality = SelectField("Nationality", choices=COUNTRIES, validators=[DataRequired()])
    working_countries = SelectMultipleField(
        "Working Countries",
        choices=COUNTRIES,
        validators=[DataRequired()]
    )
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
    choices = [(1, 'Poor'), (2, 'Fair'), (3, 'Good'), (4, 'Very Good'), (5, 'Excellent')]
    cleaning = SelectField('Cleaning:', choices=choices, validators=[DataRequired()])
    timing = SelectField('Timing:', choices=choices, validators=[DataRequired()])
    cooking = SelectField('Cooking:', choices=choices, validators=[DataRequired()])
    childcare = SelectField('Childcare:', choices=choices, validators=[DataRequired()])
    respect = SelectField('Respect:', choices=choices, validators=[DataRequired()])
    submit = SubmitField('Submit Evaluation')