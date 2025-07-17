from flask import Blueprint, request, jsonify
from Models.stock_model import StockModel
from Extras import db
from twelvedata import TDClient
from Controllers.stock_history_controller import add_stock_history

td = TDClient(apikey="d84cec2223444503b9878a61089236ca")

def get_or_create_stock(symbol):
    try:
        existing_stock = StockModel.query.filter_by(symbol=symbol.upper()).first()
        response = td.price(symbol=symbol.upper()).as_json()
        if 'price' not in response:
            return jsonify({'Message': 'Invalid Symbol or Search Error', "Status":400, "Result":"Error"})

        current_price = float(response['price'])
        new_stock = None
        if existing_stock:
            existing_stock.price = current_price
        else:
            new_stock = StockModel(symbol=symbol.upper(), price=current_price)
            db.db.session.add(new_stock)

        db.db.session.commit()
        return jsonify({"Result":{
            'symbol': symbol.upper(),
            'price': current_price,
        }, "Message":"Found Price", "Status":200})

    except Exception as e:
        return jsonify({'Result': str(e), "Message":"Error", "Status":500})