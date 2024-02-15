"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User

from api.utils import generate_sitemap, APIException
from flask_cors import CORS
import os
from flask import Flask, request, jsonify, url_for, send_from_directory
from flask_migrate import Migrate
from flask_swagger import swagger
from api.utils import APIException, generate_sitemap
from api.models import db
from api.admin import setup_admin
from api.commands import setup_commands
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

# import requests
from email.message import EmailMessage
import smtplib
from datetime import datetime, timedelta
import ssl
import uuid
from urllib.parse import unquote, quote
import secrets
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, decode_token
import os
from dotenv import load_dotenv


# from api.emailManager import send_email

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200




# any other endpoint will try to serve it like a static file

#signUp
@api.route('/signup', methods=['POST'])
def createUser():
    first_name = request.json.get("first_name")
    last_name = request.json.get("last_name")
    password = request.json.get("password")
    email = request.json.get("email")

    user = user.query.filter_by(email=email).first()
    if user != None:
        return jsonify({"msg": "email exists"}), 401
    
    if user == None:
        new_user_data = User(first_name=first_name, last_name=last_name ,password=password, email = email)
        db.session.add(new_user_data)
        db.session.commit()
    
        response_body = {
            "msg": "User successfully added"
        }

        return jsonify(response_body), 200

   
# use put or post in signup



#login
@api.route('/token', methods=['POST'])
def create_token():
    email = request.json.get("email")
    password = request.json.get("password")
    
    user = user.query.filter_by(email=email, password=password).first()
    if user is None:
        
        return jsonify({"msg": "Bad email or password"}), 401
    
  
    access_token = create_access_token(identity=user.id)
    return jsonify({ "token": access_token, "user_id": user.id }) ,200


# ask shane what he thinks about that and should be handled

@api.route('/edit_user', methods=[ 'PUT'])
@jwt_required()
def edit_user():
    current_user_id = get_jwt_identity()
    user = user.query.get(current_user_id)

    if user is None:
        return jsonify({"msg":"user does not exist"}), 404

    # Update user fields based on the JSON data (assuming JSON payload)
    data = request.get_json()
    user.first_name = data.get('first_name')
    user.last_name = data.get('last_name')
    user.biography = data.get('biography')
    user.perm_location = data.get('perm_location')
    # user.places_visited = data.get('places_visited')
    # user.wishlist_places = data.get('wishlist_places')

    # Update other fields as needed
    db.session.commit()
    user = user.query.get(current_user_id)
    response_body = {
        "msg": "Success!", "user":user.serialize()
    }
    return jsonify(response_body),200




@api.route('/user/<int:id>', methods=['GET'])
def get_user(id):
   user = user.query.get(id)

   if user is None: 
    raise APIException("Person not found", status_code=404)

   return jsonify(user.serialize()), 200





# @app.route('/user/<int:reservation>', methods=['POST'])
# def get_user(user_id):
#    user = user.query.get(user_id)

#    if user is None: 
#     raise APIException("Person not found", status_code=404)

#    return jsonify(user.serialize()), 200


# @app.route('/user/int:reservation', methods=['GET'])
# def get_user_reservation(user_id):
#    user = user.query.get(user_id)

#    if user is None: 
#     raise APIException("Person not found", status_code=404)

#    return jsonify(user.serialize()), 200




