from bson.objectid import ObjectId
from flask import Blueprint, jsonify
from assets.extensions import mongo
from assets.decors import errorhandler, tokenrequired

accounts = Blueprint("accounts", __name__, url_prefix="/accounts")


# STATUS
@accounts.route("/<account_id>/status", methods=["GET"])
@tokenrequired
@errorhandler
def get_status(current_user, account_id):

    # query the user collection for account status
    accounts = mongo.db.users.find_one({"_id": ObjectId(current_user["_id"]["$oid"])})[
        "Accounts"]

    if account_id in accounts:

        status = accounts[account_id]["Active"]

        return jsonify({"account_status": status, "account_id": account_id}), 200

    return jsonify({"error": "invalid account id", "account_id": account_id}), 400


@accounts.route("/<account_id>/status", methods=["PUT"])
@tokenrequired
@errorhandler
def update_status(current_user, account_id):

    resp = mongo.db.users.update_one({"_id": ObjectId(current_user["_id"]["$oid"])},
                                     [{"$set": {f"Accounts.{account_id}.Active": {"$eq": [False, f"$Accounts.{account_id}.Active"]}}}])

    # if update did not occur because no account id found
    if resp.matched_count == 0 or resp.modified_count == 0:

        return jsonify({"error": "failed to update status", "account_id": account_id}), 400

    return jsonify({"success": "status updated", "account_id": account_id}), 201
