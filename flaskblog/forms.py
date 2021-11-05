from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User

class RegistrationForm(FlaskForm):
	"""docstring for RegistrationForm"""
	username = StringField("Username", 
							validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField("Email", 
						validators=[DataRequired(), Email()])
	password = PasswordField("Password",
							validators=[DataRequired()])
	confirm_password = PasswordField("Confirm Password",
									validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField("Sign Up")

	def validate_username(self,username):

		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError("Username Already taken!!. Please choose a different one")

	def validate_email(self,email):

		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError("Account exists with the email provided. Please Login or try Forgot password")


class LoginForm(FlaskForm):
	"""docstring for LoginForm"""
	email = StringField("Email", 
						validators=[DataRequired(), Email()])
	password = PasswordField("Password",
							validators=[DataRequired()])
	remember = BooleanField("Remember Me")
	submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
	"""docstring for UpdateAccountForm"""
	username = StringField("Username", 
							validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField("Email", 
						validators=[DataRequired(), Email()])
	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField("Update")

	def validate_username(self,username):
		if username.data!=current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError("Username Already taken!!. Please choose a different one")

	def validate_email(self,email):
		if email.data!=current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError("Account exists with the email provided. Please Login or try Forgot password")


class PostForm(FlaskForm):
	title = StringField('Title', validators=[DataRequired(), Length(min=2, max=20)])
	content = TextAreaField('Content', validators=[DataRequired(), Length(min=2, max=20)])
	submit = SubmitField('Post')



class RequestResetForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Request Password Reset')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError('There is no account with that email. You must register first.')
	

class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Reset Password')