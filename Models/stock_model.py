from flask_sqlalchemy import SQLAlchemy
from Extras import db

class StockModel(db.db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symbol = db.Column(db.String(30), unique=True)
    price = db.Column(db.Numeric(10, 8), nullable=False)