from flask import Blueprint, jsonify, request
from assets.extensions import mongo
from assets.decors import errorhandler, tokenrequired
from datetime import datetime

forbidden = Blueprint("forbidden", __name__, url_prefix="/forbidden")


# FORBIDDEN
@forbidden.route("/<account_id>", methods=["GET", "POST"])
@tokenrequired
@errorhandler
def handle_forbidden(current_user, account_id):

    if request.method == "GET":

        # get forbidden data
        forbidden = []

        for obj in mongo.db.forbidden.find({"Account_ID": account_id}):

            # convert id to string
            obj["_id"] = str(obj["_id"])

            forbidden.append(obj)

        return jsonify({"forbidden": forbidden, "account_id": account_id}), 200

    elif request.method == "POST":

        data = request.json

        data["Account_ID"] = account_id

        data["Created"] = datetime.now()

        mongo.db.forbidden.insert_one(data)

        del data["_id"]

        return jsonify({"forbidden": data, "account_id": account_id}), 201


@forbidden.route("/<account_id>/<symbol>", methods=["DELETE"])
@tokenrequired
@errorhandler
def remove_forbidden(current_user, account_id, symbol):

    resp = mongo.db.forbidden.delete_one(
        {"Symbol": symbol, "Account_ID": account_id})

    # if update did not occur because no strategy found with account id
    if resp.deleted_count == 0:

        return jsonify({"error": "failed to update strategy"}), 400

    return jsonify({"success": "strategy updated"}), 201
