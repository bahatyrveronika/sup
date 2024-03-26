from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime
from flask_login import current_user, login_required

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    name = db.Column(db.String(150))
    image_file = db.Column(db.String(20), nullable=False, default='website/static/user_photo.png')
    notes = db.relationship('Note')
    reviews = db.relationship('Review')

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    feedback = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    # restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
