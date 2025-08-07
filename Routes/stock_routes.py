from flask import Blueprint
from Controllers import stock_controller, stock_history_controller

stock_bp = Blueprint("stock", __name__)

@stock_bp.route("/get/<symbol>")
def get_stock_by_symbol(symbol):
    return stock_controller.get_or_create_stock(symbol=symbol)

@stock_bp.route("/history/<symbol>")
def get_stock_history(symbol):
    return stock_history_controller.get_stock_history(symbol=symbol)

@stock_bp.route("/search/<symbol>")
def search_stock(symbol):
    return stock_controller.get_all_stocks(symbols=symbol)