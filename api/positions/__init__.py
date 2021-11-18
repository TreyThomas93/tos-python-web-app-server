from flask import Blueprint, jsonify, request
from assets.extensions import mongo
from assets.decors import errorhandler, tokenrequired
from pprint import pprint

positions = Blueprint("positions", __name__, url_prefix="/positions")


# POSITIONS
@positions.route("/<account_id>", methods=["GET"])
@tokenrequired
@errorhandler
def get_positions(current_user, account_id):

    filter = {
        "Account_ID": int(account_id)
    }

    for k, v in request.args.items():

        if v == "" or v == None:

            return jsonify({"error": "invalid query parameter"}), 400

        if k != "position_name":

            if k == "account_position":

                k = k.replace("_", " ").title().replace(" ", "_").strip()

                v = v.title()

            filter[k] = v

    position_name = request.args.get("position_name")

    collection = mongo.db.open_positions if position_name == "open_positions" else mongo.db.closed_positions

    # get positions
    positions = []

    for obj in collection.find(filter):

        # convert id to string
        obj["_id"] = str(obj["_id"])

        positions.append(obj)
    
    return jsonify({"positions": positions, "account_id": account_id}), 200
