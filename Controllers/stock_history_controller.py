from flask import Blueprint, request, jsonify
from datetime import date
from Extras import db
from Models.stock_history_model import StockHistory
from Models.stock_model import StockModel
from decimal import Decimal

def get_stock_history(stock_id):
    stock_name = StockModel.query.filter_by(id=stock_id).first()
    history = StockHistory.query.filter_by(stock_id=stock_id).order_by(StockHistory.date.asc()).all()
    if not history:
        return jsonify({"Message": "No Register from this Stock", "Status":404, "Result":"None"}),

    result = []
    for entry in history:
        result.append({
            "date": entry.date.isoformat(),
            "price": str(entry.price),
            "change": str(entry.change) if entry.change is not None else None
        })
    return jsonify({"Message":f"History of {stock_name.name}", "Result": result, "Status":200})

def add_stock_history(stock_id):
    data = request.get_json()
    if not data or 'price' not in data:
        return jsonify({"Message": "Data 'price' is obrigatory", "Result":"None", "Status":400})

    try:
        price_today = Decimal(str(data['price']))
    except:
        return jsonify({"Message": "Invalid Price", "Result":"Error", "Status":400})

    stock = StockModel.query.get(stock_id)
    if not stock:
        return jsonify({"Message": "Stock Not Found", "Status":404, "Result":"Error"})
    
    last_entry = StockHistory.query.filter_by(stock_id=stock_id).order_by(StockHistory.date.desc()).first()
    change = None
    if last_entry:
        change = price_today - last_entry.price

    today_entry = StockHistory.query.filter_by(stock_id=stock_id, date=date.today()).first()
    if today_entry:
        return jsonify({"Message": "Today stock history already exists", "Result":"Error", "Status":409})

    new_entry = StockHistory(
        stock_id=stock_id,
        price=price_today,
        change=change
    )
    db.db.session.add(new_entry)
    db.db.session.commit()

    return jsonify({
        "Message": "History suceffuly saved",
        "Result":{
            "date": new_entry.date.isoformat(),
            "price": str(new_entry.price),
            "change": str(new_entry.change) if new_entry.change is not None else None
        },
        "Status":201
    })