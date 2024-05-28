from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, EmailField, RadioField
from wtforms.validators import DataRequired, Email

class RegisterForm(FlaskForm):
    email = EmailField('Your Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    conf_password = PasswordField('Confirm Password', validators=[DataRequired()])
    role = RadioField('Your Role?', choices = [(2,'Influencer'), (3,'Sponser')],validators = [DataRequired()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    email = EmailField('Your Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = RadioField('Your Role?', choices = [(2,'Influencer'), (3,'Sponser')],validators = [DataRequired()])
    submit = SubmitField('Submit')

class SponserDetailForm(FlaskForm):
    company_name = StringField('Company/Individual Name', validators = [DataRequired()])
    industry = StringField('Industry', validators = [DataRequired()])
    budget = IntegerField('Company Budget', validators = [DataRequired()])
    submit = SubmitField('Submit')

class InfluencerDetailForm(FlaskForm):
    name = StringField('Name', validators = [DataRequired()])
    category = StringField('Category', validators = [DataRequired()])
    niche = StringField('Niche', validators = [DataRequired()])
    submit = SubmitField('Submit')