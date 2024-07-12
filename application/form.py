from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, FileField, EmailField, RadioField, DateField, TextAreaField
from wtforms.validators import DataRequired, Email

class SeachForm(FlaskForm):
    search = StringField('Search for: ')
    submit = SubmitField()

class RegisterForm(FlaskForm):
    email = EmailField('Your Email*', validators = [DataRequired(), Email()])
    password = PasswordField('Password*', validators=[DataRequired()])
    conf_password = PasswordField('Confirm Password*', validators=[DataRequired()])
    role = RadioField('Your Role?*', choices = [(2,'Influencer'), (3,'Sponser')], validators = [DataRequired()])
    image = FileField('Profile Image')
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = EmailField('Your Email*', validators = [DataRequired(), Email()])
    password = PasswordField('Password*', validators=[DataRequired()])
    submit = SubmitField('Login')

# class AdminLoginForm(FlaskForm):
#     email = EmailField('Your Email*', validators = [DataRequired(), Email()])
#     password = PasswordField('Password*', validators=[DataRequired()])
#     submit = SubmitField('Login')

class SponserDetailForm(FlaskForm):
    company_name = StringField('Company/Individual Name*', validators = [DataRequired()])
    industry = StringField('Industry*', validators = [DataRequired()])
    budget = IntegerField('Company Budget*', validators = [DataRequired()])
    about = StringField('About You or Your Company')
    submit = SubmitField('Submit')

class InfluencerDetailForm(FlaskForm):
    name = StringField('Name*', validators = [DataRequired()])
    category = StringField('Category*', validators = [DataRequired()])
    niche = StringField('Niche*', validators = [DataRequired()])
    about = StringField('About Yourself')
    submit = SubmitField('Submit')

class CampaignDetails(FlaskForm):
    campaign_name = StringField('Campaign Name*', validators = [DataRequired()])
    desc = TextAreaField('Description*', validators = [DataRequired()])
    requirements = TextAreaField('requirements*', validators = [DataRequired()])
    end_date = DateField('End-Date*', validators = [DataRequired()])
    budget = IntegerField('Campaign Budget*', validators = [DataRequired()])
    visibility = RadioField('Visibilty*', choices =[(0,'Privet'), (1, 'Public')],validators = [DataRequired()])
    goals = TextAreaField('Goals')
    image = FileField('Campaign Image')
    submit = SubmitField('Create')

class UpdateProfileForm(FlaskForm):
    email = EmailField('New Email')
    password = PasswordField('New Password')
    conf_password = PasswordField('Confirm Password (Only if you want to edit)')
    image = FileField('New Profile Pic')
    submit = SubmitField('Update')

class NegotiateForm(FlaskForm):
    negotiate = IntegerField('Negotiate?')    
    submit = SubmitField('Colab')