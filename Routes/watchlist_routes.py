from flask import Blueprint, request
from Controllers import watchlist_controller

watchlist_bp = Blueprint('/watchlist', __name__)

@watchlist_bp.route('/add/<int:user_id>/<symbol>', methods=['POST'])
def add(user_id, symbol):
    return watchlist_controller.add_to_watchlist(user_id, symbol)

@watchlist_bp.route('/view/<int:user_id>', methods=['GET'])
def view(user_id):
    return watchlist_controller.view_watchlist(user_id)

@watchlist_bp.route('/remove/<int:user_id>/<symbol>', methods=['DELETE'])
def remove(user_id, symbol):
    return watchlist_controller.remove_from_watchlist(user_id, symbol)
