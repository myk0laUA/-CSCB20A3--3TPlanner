from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField,FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models import User, Task, Tip, Comment


# a form for logging in with an email and password
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


# a form for registering a new user with a username, email, and password,
#  with validations to ensure that the username and email are unique
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email.')
        

# a form for adding a new task with a title and duration (in minutes)
class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    duration = IntegerField('Duration (min)', validators=[DataRequired()])
    submit = SubmitField('Add Task')


# a form for submitting a tip with some content (limited to 10-140 characters)
class TipForm(FlaskForm):
    content = TextAreaField('Tip', validators=[DataRequired(), Length(min=10, max=140)])
    submit = SubmitField('Submit Tip')


# a form for adding a comment to a tip with some content (limited to 5-140 characters)
class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired(), Length(min=5, max=140)])
    submit = SubmitField('Add Comment')


# a form for using a token with a single submit button
#  (will be used for shop and other activities in the future)
class UseTokensForm(FlaskForm):
    submit = SubmitField('Use Token')

# a form for updating user settings, including a username (limited to 2-20 characters),
# a boolean for enabling dark mode, and a file field for uploading a new profile picture.
class SettingsForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    dark_mode = BooleanField('Dark Mode')
    profile_picture = FileField('Profile Picture')
    submit = SubmitField('Save Changes')