from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User
from app import photos
from werkzeug.utils import secure_filename

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=120)])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=3, max=140)])
    teacher = BooleanField('Are you a teacher?')
    password = PasswordField('Password', validators=[DataRequired(), Length(min=3)])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

class AssignmentForm(FlaskForm):
    q1 = TextAreaField('Question 1', validators=[Length(min=0, max=512)])
    a1 = TextAreaField('Answer 1', validators=[Length(min=0, max=16384)])
    q2 = TextAreaField('Question 2', validators=[Length(min=0, max=512)])
    a2 = TextAreaField('Answer 2', validators=[Length(min=0, max=16384)])
    q3 = TextAreaField('Question 3', validators=[Length(min=0, max=512)])
    a3 = TextAreaField('Answer 3', validators=[Length(min=0, max=16384)])
    submit = SubmitField('Publish Question')

class SubmitForm(FlaskForm):
    photo = FileField('Image', validators=[FileRequired(), FileAllowed(photos, 'Images only!')])
    submit = SubmitField('Submit')
