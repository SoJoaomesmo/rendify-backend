from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, request, jsonify
from Extras import db
import werkzeug.security

class Watchlist(db.db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock_symbol = db.Column(db.String(10), nullable=False)  # "AAPL", "PETR4"
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('watchlist', lazy=True))