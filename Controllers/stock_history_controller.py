from flask import Blueprint, request, jsonify
from datetime import date
from Extras import db
from Models.stock_history_model import StockHistory
from Models.stock_model import StockModel
from decimal import Decimal

def add_or_update_stock_history(stock_id, data):
    if not data or 'price' not in data:
        return jsonify({"Message": "Data 'price' is obrigatory", "Result":"None", "Status":400})

    try:
        price_today = Decimal(str(data['price']))
    except:
        return jsonify({"Message": "Invalid Price", "Result":"Error", "Status":400})

    stock = StockModel.query.get(stock_id)
    if not stock:
        return jsonify({"Message": "Stock Not Found", "Status":404, "Result":"Error"})

    today = date.today()
    today_entry = StockHistory.query.filter_by(stock_id=stock_id, date=today).first()

    if today_entry:
        change = None
        last_entry_before_today = (
            StockHistory.query
            .filter(StockHistory.stock_id == stock_id, StockHistory.date < today)
            .order_by(StockHistory.date.desc())
            .first()
        )
        if last_entry_before_today:
            change = price_today - last_entry_before_today.price
        else:
            change = None

        today_entry.price = price_today
        today_entry.change = change
        db.db.session.commit()

        return jsonify({
            "Message": "Today's history updated successfully",
            "Result": {
                "date": today_entry.date.isoformat(),
                "price": str(today_entry.price),
                "change": str(today_entry.change) if today_entry.change is not None else None
            },
            "Status": 200
        })
    else:
        last_entry = (
            StockHistory.query
            .filter(StockHistory.stock_id == stock_id)
            .order_by(StockHistory.date.desc())
            .first()
        )

        change = None
        if last_entry:
            change = price_today - last_entry.price

        new_entry = StockHistory(
            stock_id=stock_id,
            price=price_today,
            change=change
        )
        db.db.session.add(new_entry)
        db.db.session.commit()

        return jsonify({
            "Message": "History successfully saved",
            "Result": {
                "date": new_entry.date.isoformat(),
                "price": str(new_entry.price),
                "change": str(new_entry.change) if new_entry.change is not None else None
            },
            "Status": 201
        })
