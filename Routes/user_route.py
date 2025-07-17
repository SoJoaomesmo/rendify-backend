from flask import Blueprint
from Controllers import user_controller

user_bp = Blueprint('/user', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    return user_controller.register()

@user_bp.route('/login', methods=['POST'])
def login():
    return user_controller.login()

@user_bp.route('/change-password', methods=['POST'])
def change_pass():
    return user_controller.change_password()