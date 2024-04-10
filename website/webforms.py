from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.validators import ValidationError
from .models import User

# Create A Search Form
class SearchForm(FlaskForm):
	searched = StringField("Searched", validators=[DataRequired()])
	submit = SubmitField("Submit")

class RequestResetForm(FlaskForm):
	email = StringField("Email", validators = [DataRequired(), Email()])
	submit = SubmitField("Request Password Reset")

	def validate_email(self, email):
		email.data = email.data.lower()
		user = User.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError('There is no account with that email. You must register first.')
	
class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Reset Password')

class UpdateTagsForm(FlaskForm):
    tags = StringField('Tags')
    submit = SubmitField('Update Tags')