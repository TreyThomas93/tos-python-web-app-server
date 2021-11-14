from flask import Blueprint, jsonify
from assets.extensions import mongo
from assets.decors import errorhandler, tokenrequired
from datetime import datetime, timedelta

historical = Blueprint("historical", __name__, url_prefix="/historical")


# HISTORICAL
# @historical.route("/<account_id>", methods=["GET"])
# @tokenrequired
# @errorhandler
# def get_queue(current_user, account_id):

#     # get queue data
#     queue = []

#     for obj in mongo.db.queue.find({"Account_ID": int(account_id)}):

#         # convert id to string
#         obj["_id"] = str(obj["_id"])

#         queue.append(obj)

#     return jsonify({"queue": queue, "account_id": account_id}), 200
