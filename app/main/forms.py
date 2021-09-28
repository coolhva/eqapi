from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, IntegerField, BooleanField)
from wtforms.fields.simple import PasswordField
from wtforms.validators import ValidationError, DataRequired, NumberRange
from app.models import User


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class SettingsForm(FlaskForm):
    api_username = StringField('API Username', validators=[DataRequired()])
    api_password = PasswordField('API Password')
    interval = IntegerField('API Query interval (seconds)', validators=[
        DataRequired(),
        NumberRange(min=10,
                    max=3600,
                    message='Seconds must be between %(min)s and %(max)s')
        ], default=300)
    disable_registration = BooleanField('Disable user registration')
    submit = SubmitField('Save')
