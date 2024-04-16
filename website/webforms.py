from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms.validators import ValidationError
from .models import User

# Create a search form to be injected into the nav bar. The search is performed on the recipes and the associated tags.
class SearchForm(FlaskForm):
	searched = StringField("Searched", validators=[DataRequired()])
	submit = SubmitField("Submit")	

# Create a password reset request form for the pasword reset functionality
class RequestResetForm(FlaskForm):
	email = StringField("Email", validators = [DataRequired(), Email()])
	submit = SubmitField("Request Password Reset")

	def validate_email(self, email):
		email.data = email.data.lower()
		user = User.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError('There is no account with that email. You must register first.')

# Create a password reset form for the password reset functinality where the user inputs their new password
class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Reset Password')

# Create a form for updating tags associated with a particular recipe
class UpdateTagsForm(FlaskForm):
	tags = StringField('Tags')
	submit = SubmitField('Update Tags')

	def process_tags(self):
		return [tag.strip().title() for tag in self.tags.split(',') if tag.strip()]

	

		
