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

    def get_id(self):
           return (self.user_id)

class UserRoles(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'), primary_key=True)

    user = db.relationship('User', backref=db.backref('user_roles', cascade="all, delete-orphan"))
    role = db.relationship('Role', backref=db.backref('user_roles', cascade="all, delete-orphan"))


class Sponser(db.Model):
    sponser_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    company_name = db.Column(db.String, nullable = False)
    industry = db.Column(db.String, nullable = False)
    budget = db.Column(db.Integer, nullable = False)

    user = db.relationship('User', backref=db.backref('sponsers', cascade="all, delete-orphan"))

class Influencer(db.Model):
    influencer_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    name = db.Column(db.String, nullable = False)
    category = db.Column(db.String, nullable = False)
    niche = db.Column(db.String, nullable = False)

    # reach = db.Column(db.Integer, nullable = True)
    user = db.relationship('User', backref=db.backref('influencers', cascade="all, delete-orphan"))

class Campaign(db.Model):
    campaign_id = db.Column(db.Integer, primary_key=True, autoincrement = True)
    campaign_by = db.Column(db.Integer, db.ForeignKey("sponser.sponser_id"))
    campaign_name = db.Column(db.String, unique=True)
    desc = db.Column(db.String, nullable=False)
    start_date = db.Column(db.DateTime, default = datetime.utcnow())
    end_date = db.Column(db.DateTime, nullable=True)
    budget = db.Column(db.Integer, nullable=True)
    visibility = db.Column(db.Boolean)
    goals = db.Column(db.String, nullable=True)
    image_path = db.Column(db.String, nullable=True, default = 'https://mdbcdn.b-cdn.net/img/new/slides/041.webp')
    sponser = db.relationship('Sponser', backref = db.backref('campaigns', cascade = "all, delete-orphan"))

class Camp_request(db.Model):
    request_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaign.campaign_id"))
    influencer_id = db.Column(db.Integer, db.ForeignKey("influencer.influencer_id"))
    requirements = db.Column(db.String)
    payment_amount = db.Column(db.Integer)
    stutus = db.Column(db.String(15))

    influencer = db.relationship('Influencer', backref = db.backref('camp_requests', cascade = "all, delete-orphan"))
    campaign = db.relationship('Campaign', backref = db.backref('camp_requests', cascade = "all, delete-orphan"))

class Camp_msg(db.Model):
    msg_id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    request_id = db.Column(db.Integer, db.ForeignKey("camp_request.request_id"))
    msg = db.Column(db.String)