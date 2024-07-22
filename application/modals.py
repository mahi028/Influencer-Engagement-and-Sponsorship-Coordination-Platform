from application import db
from datetime import datetime
from flask_login import UserMixin

class Role(db.Model):
    role_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    name = db.Column(db.String)

class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, autoincrement = True, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String, nullable=False)
    active_flag = db.Column(db.Boolean, default = False, nullable = False)
    profile = db.Column(db.String, nullable = True, default = 'user.png')
    flag = db.Column(db.Boolean, nullable = False, default = False)
    flag_reason = db.Column(db.String, nullable = True)
    wallet_balance = db.Column(db.Integer, nullable = False, default = 0)

    def get_id(self):
           return (self.user_id)

class UserRoles(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'), primary_key=True)

    user = db.relationship('User', backref=db.backref('user_roles', cascade="all, delete-orphan"))
    role = db.relationship('Role', backref=db.backref('user_roles', cascade="all, delete-orphan"))

class Admin(db.Model):
    admin_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    name = db.Column(db.String, nullable = False)

    user = db.relationship('User', backref=db.backref('admins', cascade="all, delete-orphan"))
     
class Sponser(db.Model):
    sponser_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    company_name = db.Column(db.String, nullable = False)
    industry = db.Column(db.String, nullable = False)
    budget = db.Column(db.Integer, nullable = False)
    about = db.Column(db.String, nullable = True)
    user = db.relationship('User', backref=db.backref('sponsers', cascade="all, delete-orphan"))

class Influencer(db.Model):
    influencer_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    name = db.Column(db.String, nullable = False)
    category = db.Column(db.String, nullable = False)
    niche = db.Column(db.String, nullable = False)
    about = db.Column(db.String, nullable = True)
    # reach = db.Column(db.Integer, nullable = True)
    user = db.relationship('User', backref=db.backref('influencers', cascade="all, delete-orphan"))

class Campaign(db.Model):
    campaign_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    campaign_by = db.Column(db.Integer, db.ForeignKey("sponser.sponser_id"), nullable = False)
    campaign_name = db.Column(db.String, unique=True)
    desc = db.Column(db.String, nullable=False)
    requirements = db.Column(db.String, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default = datetime.utcnow())
    end_date = db.Column(db.DateTime, nullable=False)
    budget = db.Column(db.Integer, nullable=True)
    visibility = db.Column(db.Boolean)
    goals = db.Column(db.String, nullable=True)
    image_path = db.Column(db.String, nullable=True, default = 'user.png')
    flag = db.Column(db.Boolean, nullable = False, default = False)
    flag_reason = db.Column(db.String, nullable = True)
    
    sponser = db.relationship('Sponser', backref = db.backref('campaigns', cascade = "all, delete-orphan"))

class Posts(db.Model):
    post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_by = db.Column(db.Integer, db.ForeignKey("influencer.influencer_id"), nullable=False)
    post_for = db.Column(db.Integer, db.ForeignKey("requests.request_id"), nullable=False)
    post_title = db.Column(db.String, nullable=False)
    desc = db.Column(db.String, nullable=False)
    image_path = db.Column(db.String, nullable=True, default='user.png')
    flag = db.Column(db.Boolean, nullable=False, default=False)
    flag_reason = db.Column(db.String, nullable=True)
    suggestion = db.Column(db.String, nullable=True)
    visibility = db.Column(db.Boolean)
    influencer = db.relationship('Influencer', backref=db.backref('posts', cascade="all, delete-orphan"))
    request = db.relationship('Requests', backref=db.backref('posts', cascade="all, delete-orphan"))

class Requests(db.Model):
    request_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaign.campaign_id"))
    influencer_id = db.Column(db.Integer, db.ForeignKey("influencer.influencer_id"))
    n_amount = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(15), nullable=False, default='Pending')
    requested_by = db.Column(db.String(15), nullable=False)

    influencer = db.relationship('Influencer', backref=db.backref('requests', cascade="all, delete-orphan"))
    campaign = db.relationship('Campaign', backref=db.backref('requests', cascade="all, delete-orphan"))

# class Camp_request(db.Model):
#     request_id = db.Column(db.Integer, db.ForeignKey("requests.request_id"), primary_key = True)
#     payment_amount = db.Column(db.Integer)
#     stutus = db.Column(db.String(15))
#     n_amount = db.Column(db.Integer, nullable=True)
#     request = db.relationship('Requests', backref = db.backref('camp_requests', cascade = "all, delete-orphan"))

class Camp_msg(db.Model):
    msg_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    request_id = db.Column(db.Integer, db.ForeignKey("requests.request_id"))
    msg = db.Column(db.String)