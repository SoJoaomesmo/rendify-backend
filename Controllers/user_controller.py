from flask import Blueprint, request, jsonify
from Models import user_model as UserModel
from Extras import db

def register():
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')

    if not name or not password:
        return jsonify({"Message": "Name and password are required", "Status": 400, "Result": "Error"}), 400

    if UserModel.User.query.filter_by(name=name).first():
        return jsonify({"Message": "User already exists", "Status": 409, "Result": "Error"}), 409

    user = UserModel.User(name=name)
    user.change_password(password)
    db.db.session.add(user)
    db.db.session.commit()

    return jsonify({"Message": "User created", "Status": 201, "Result": {"name": name}}), 201

def login():
    data = request.get_json()
    name = data.get('name')
    password = data.get('password')

    user = UserModel.User.query.filter_by(name=name).first()
    if not user:
        return jsonify({"Message": "User not found", "Status": 404, "Result": "Error"}), 404

    result = user.check_password(password)
    status = result["Status"]
    return jsonify(result), status

def change_password():
    data = request.get_json()
    name = data.get('name')
    new_password = data.get('new_password')

    user = UserModel.User.query.filter_by(name=name).first()
    if not user:
        return jsonify({"Message": "User not found", "Status": 404, "Result": "Error"}), 404

    result = user.change_password(new_password)
    db.db.session.commit()
    status = result["Status"]
    return jsonify(result), status