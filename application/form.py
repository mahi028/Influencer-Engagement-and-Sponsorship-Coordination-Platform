from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, EmailField, RadioField, DateField, TextAreaField
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

class AdminLoginForm(FlaskForm):
    email = EmailField('Your Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
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

class CampaignDetails(FlaskForm):
    campaign_name = StringField('Campaign Name', validators = [DataRequired()])
    desc = TextAreaField('Description', validators = [DataRequired()])
    end_date = DateField('End-Date', validators = [DataRequired()])
    budget = IntegerField('Campaign Budget', validators = [DataRequired()])
    visibility = RadioField('Visibilty', choices =[(0,'Privet'), (1, 'Public')],validators = [DataRequired()])
    goals = TextAreaField('Goals')
    submit = SubmitField('Submit')