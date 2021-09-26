from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField)
from wtforms.fields.simple import PasswordField
from wtforms.validators import ValidationError, DataRequired
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
    api_password = PasswordField('API Password', validators=[DataRequired()])
    submit = SubmitField('Save')
