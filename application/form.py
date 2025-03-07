from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, FileField, EmailField, RadioField, DateField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, Optional

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

class SponserDetailForm(FlaskForm):
    company_name = StringField('Company/Individual Name*', validators = [DataRequired()])
    industry = SelectField('Industry*', choices=[], validators = [DataRequired()])
    budget = IntegerField('Company Budget*', validators = [DataRequired()])
    about = StringField('About You or Your Company')
    submit = SubmitField('Submit')

class InfluencerDetailForm(FlaskForm):
    name = StringField('Name*', validators = [DataRequired()])
    category = SelectField('Category*', choices=[],validators = [DataRequired()])
    about = StringField('About Yourself')
    submit = SubmitField('Submit')

class CampaignDetails(FlaskForm):
    campaign_name = StringField('Campaign Name*', validators = [DataRequired()])
    desc = TextAreaField('Description*', validators = [DataRequired()])
    category = SelectField('Category*', choices=[],validators = [DataRequired()])
    requirements = TextAreaField('requirements*', validators = [DataRequired()])
    start_date = DateField('Start-Date')
    end_date = DateField('End-Date*', validators = [DataRequired()])
    budget = IntegerField('Campaign Budget*', validators = [DataRequired()])
    visibility = RadioField('Visibilty*', choices =[(0,'Privet'), (1, 'Public')],validators = [DataRequired()])
    goals = TextAreaField('Goals')
    image = FileField('Campaign Image')
    submit = SubmitField('Create')

class PostDetails(FlaskForm):
    post_title = StringField('Post Title*', validators = [DataRequired()])
    desc = TextAreaField('Post Description*', validators = [DataRequired()])
    post_for = SelectField('Post For', validators=[DataRequired()])
    image = FileField('Post Image')
    submit = SubmitField('Create')

class UpdateProfileForm(FlaskForm):
    email = EmailField('New Email')
    password = PasswordField('New Password')
    conf_password = PasswordField('Confirm Password (Only if you want to edit)')
    image = FileField('New Profile Pic')
    submit = SubmitField('Update')

class UpdateCampForm(FlaskForm):
    start_date = DateField('Start Date', validators=[Optional()])
    end_date = DateField('End Date', validators=[Optional()])
    image = FileField('New Campaign Image', validators=[Optional()])
    submit = SubmitField('Update')

class UpdatePostForm(FlaskForm):
    image = FileField('New Post Image', validators=[Optional()])
    submit = SubmitField('Update')

class NegotiateForm(FlaskForm):
    negotiate = IntegerField('Negotiate?')    
    submit = SubmitField('Colab')

class SuggestionForm(FlaskForm):
    suggest = StringField('Suggestions?')    
    submit = SubmitField('Suggest')

class PaymentForm(FlaskForm):
    amount = IntegerField('Amount (in $dollars)*', validators=[DataRequired()])    
    password = PasswordField('Password*', validators=[DataRequired()])
    submit = SubmitField('Pay')

categories = {
        "None": [
            "None"
        ],
        "Niche/Industry": [
            "Fashion",
            "Beauty",
            "Travel",
            "Fitness",
            "Food",
            "Technology",
            "Gaming",
            "Lifestyle",
            "Parenting",
            "Finance",
            "Education",
            "Automotive",
            "Music",
            "Photography",
            "Art and Crafts",
            "Books and Literature",
            "Environment and Sustainability",
            "Pets",
            "Business",
            "Sports"
        ],
        "Content Type": [
            "Vloggers",
            "Reviewers",
            "Tutorial Creators",
            "Entertainers",
            "Activists",
            "Live Streamers"
        ],
        "Platform": [
            "Instagram",
            "YouTube",
            "TikTok",
            "Twitter",
            "Facebook",
            "Blogging",
            "Twitch",
            "LinkedIn",
            "Pinterest"
        ],
        "Audience Demographics": [
            "Teens",
            "Young Adults",
            "Parents",
            "Professionals",
            "Seniors"
        ]
    }