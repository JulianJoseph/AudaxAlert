from flask_wtf import Form
from wtforms.fields import StringField, SubmitField
from wtforms.fields.html5 import URLField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo,url, ValidationError
from . models import User

class SignupForm(Form):
    userid = StringField('Audax ID',
                    validators=[
                        DataRequired(), Length(3, 80),
                        Regexp('^[A-Za-z0-9_]{3,}$',
                            message='Please enter your Audax membership id, omitting any letters')])

    email = StringField('Email',
                        validators=[DataRequired(), Length(1, 120), Email()])                            

    def validate_userid(self, username_field):
        if User.query.filter_by(audax_id=username_field.data).first():
            raise ValidationError('This username is already taken.')    

    def validate_email(self, email_field):
        if User.query.filter_by(email=email_field.data).first():
            raise ValidationError('There already is a user with this email address.')
            