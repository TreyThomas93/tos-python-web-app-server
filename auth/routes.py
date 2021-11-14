from flask import Blueprint, current_app, request, jsonify
from assets.extensions import mongo, bcrypt
from assets.decors import errorhandler
from datetime import datetime, timedelta
import json
from bson import json_util
import jwt
import time

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.route("/login", methods=["POST"])
@errorhandler
def login():

    username = request.json["username"]

    password = request.json["password"]

    user = mongo.db.users.find_one({
        "Username": username
    })

    if user:

        if bcrypt.check_password_hash(user["Password"], password):

            del user["Username"]

            del user["Password"]

            token = jwt.encode({"user": json.loads(json_util.dumps(user)), "exp": datetime.utcnow(
            ) + timedelta(hours=24)}, current_app.config["SECRET_KEY"], algorithm="HS256")

            current_app.logger.info(f"Login Successful - Username: {username}")

            return jsonify({"access_token": token, "user": json.loads(json_util.dumps(user))})

    current_app.logger.info(
        f"Invalid Username and/or Password - Username: {username}")

    return jsonify({"error": "Invalid Username and/or Password"}), 401


@auth.route("/checkAuthToken", methods=["GET"])
@errorhandler
def checkAuthToken():
    """ used to check if user is authorized to view pages
    Returns:
        [json]: [response]
    """

    token = request.headers.get("x-access-token")

    # check blacklist
    blacklisted = mongo.db.jwtblacklist.find_one({"Token": token})

    if token != None and token != "" and blacklisted == None:

        try:

            jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"])

            return jsonify({"authenticated": True}), 200

        except jwt.ExpiredSignatureError as e:

            return jsonify({"error": "Token Expired"}), 401

        except jwt.DecodeError as e:

            return jsonify({"error": "Token Decode Error"}), 401

    return jsonify({"error": "Token Does Not Exist"}), 401


@auth.route("/logout", methods=["GET"])
@errorhandler
def logout():
    """ add users token to blacklist.
    """

    token = request.headers.get("x-access-token")

    if token != None and token != "":

        mongo.db.jwtblacklist.update_one({"Token": token},
                                         {"$set": {"Token": token, "Timestamp": time.time()}}, upsert=True)

        return jsonify({"message": "user logged out. token blacklisted"}), 200

    return jsonify({"message": "user logged out. token not blacklisted"}), 200
