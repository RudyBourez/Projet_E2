from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(1000))
    last_name = db.Column(db.String(1000))
    predictions = db.relationship("Prediction", backref='Users', lazy=True)
    
class Prediction(db.Model):
    __tablename__ = 'Predictions'
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    neighborhood = db.Column(db.String(80))
    garage_area = db.Column(db.Integer)
    garage_cars = db.Column(db.Integer)
    fst_flr_sf = db.Column(db.Integer)
    total_bsmt_sf = db.Column(db.Integer)
    gr_liv_area = db.Column(db.Integer)
    overall_qual = db.Column(db.Integer)
    kitchen_qual = db.Column(db.String(20))
    bsmt_qual = db.Column(db.String(20))
    age_house = db.Column(db.Integer)
    bath = db.Column(db.Integer)
    estimated_price = db.Column(db.Integer)
