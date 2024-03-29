"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import datetime
import jwt
import os
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_jwt_extended import create_access_token, JWTManager
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import timedelta

api = Blueprint('api', __name__)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200


@api.route("/signup", methods=["POST"])
def signup():
    # username = request.json.get("username", None)
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"msg": "User already exists"}), 400

    new_user = User(email=email, password=password, is_active=True)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"user_id": new_user.id}), 200


@api.route("/token", methods=["POST"])
def create_token():
    # username = request.json.get("username", None)
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(email=email, password=password).first()
    if user is None:
        return jsonify({"msg": "Wrong credentials"}), 401
    expires = timedelta(minutes=2)
    access_token = create_access_token(identity=user.id, expires_delta=expires)
    return jsonify({"token": access_token, "user_id": user.id})

@api.route('/validate-token', methods=['GET'])
@jwt_required()
def validate_token():
    current_user = get_jwt_identity()
    return jsonify({"msg": "Token is valid", "user_id": current_user}), 200


@api.route('/login', methods=['POST'])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    if email is None or password is None:
        return jsonify({"msg": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"msg": "Invalid credentials"}), 401

    expiration_date = datetime.datetime.utcnow() + datetime.timedelta(days=1)
    secret_key = os.environ.get("SECRET_KEY", "my_precious")
    token = jwt.encode({"id": user.id, "exp": expiration_date},
                       secret_key, algorithm="HS256")

    return jsonify({"token": token}), 200