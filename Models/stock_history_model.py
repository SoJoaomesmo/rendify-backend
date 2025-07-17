from datetime import date
from Extras import db

class StockHistory(db.db.Model):
    id = db.db.Column(db.db.Integer, primary_key=True)
    stock_id = db.db.Column(db.db.Integer, db.db.ForeignKey('stock_model.id'), nullable=False)
    date = db.db.Column(db.db.Date, default=date.today, nullable=False)
    price = db.db.Column(db.db.Numeric(18, 8), nullable=False)
    change = db.db.Column(db.db.Numeric(18, 8))  # EM NÚMERO, não porcentagem

    stock = db.relationship('StockModel', backref=db.backref('history', lazy=True))