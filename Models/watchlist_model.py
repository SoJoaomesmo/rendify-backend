from flask_sqlalchemy import SQLAlchemy
from flask import Blueprint, request, jsonify
from Extras import db
import werkzeug.security

class Watchlist(db.db.Model):
    id = db.db.Column(db.db.Integer, primary_key=True)
    stock_symbol = db.db.Column(db.db.String(10), nullable=False)  # "AAPL", "PETR4"
    user_id = db.db.Column(db.db.Integer, db.db.ForeignKey('user.id'), nullable=False)

    user = db.db.relationship('User', backref=db.db.backref('watchlist', lazy=True))