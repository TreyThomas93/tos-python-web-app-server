from flask import Blueprint, request, jsonify
from assets.extensions import mongo
from assets.decors import errorhandler, tokenrequired
from bson.objectid import ObjectId
from api.strategies.helpers import maxDrawdown, sharpeRatio
import statistics

strategies = Blueprint("strategies", __name__, url_prefix="/strategies")


# STRATEGIES
@strategies.route("/<account_id>", methods=["GET"])
@tokenrequired
@errorhandler
def get_strategies(current_user, account_id):

    closed_positions = mongo.db.closed_positions.find(
        {"Account_ID": int(account_id)})

    strategies = mongo.db.strategies.find({"Account_ID": int(account_id)})

    strategies_obj = {}

    for strategy in strategies:

        obj = {
            "Wins": 0,
            "Loss": 0,
            "Profit_Loss": 0,
            "Avg_ROI": [],
            "Drawdowns": []}

        strategy.pop("_id", None)

        strategies_obj[strategy["Strategy"]] = {**obj, **strategy}

    for position in closed_positions:

        strategy = position["Strategy"]

        if strategy not in strategies_obj:

            continue

        if position["Position_Type"] == "LONG":

            strategies_obj[strategy]["Profit_Loss"] += (
                (position["Exit_Price"] * position["Qty"]) - (position["Entry_Price"] * position["Qty"]))

            strategies_obj[strategy]["Drawdowns"].append(
                position["Exit_Price"] - position["Entry_Price"])

            roi = round(
                ((position["Exit_Price"] / position["Entry_Price"]) - 1) * 100, 2)

        else:

            strategies_obj[strategy]["Profit_Loss"] += (
                (position["Entry_Price"] * position["Qty"]) - (position["Exit_Price"] * position["Qty"]))

            strategies_obj[strategy]["Drawdowns"].append(
                position["Entry_Price"] - position["Exit_Price"])

            roi = round(
                ((position["Entry_Price"] / position["Exit_Price"]) - 1) * 100, 2)

        if roi > 0:

            strategies_obj[strategy]["Wins"] += 1

        elif roi < 0:

            strategies_obj[strategy]["Loss"] += 1

        else:

            continue

        strategies_obj[strategy]["Avg_ROI"].append(position["ROI"])

    strategies = []

    for key, value in strategies_obj.items():

        value["MDD"] = maxDrawdown(value)

        if len(value["Avg_ROI"]) > 1:

            value["Avg_ROI"] = round(statistics.mean(value["Avg_ROI"]), 2)

            value["SR"] = sharpeRatio(value)

        else:

            value["Avg_ROI"] = 0

            value["SR"] = 0

        value["Profit_Loss"] = round(value["Profit_Loss"], 2)

        value["Strategy"] = key

        try:

            value["WRP"] = round(((value["Wins"] - value["Loss"]) /
                                  value["Wins"]) * 100, 2)

        except:

            value["WRP"] = 0

        del strategies_obj[key]["Drawdowns"]

        del strategies_obj[key]["Wins"]

        del strategies_obj[key]["Loss"]

        strategies.append(value)

    return jsonify({"strategies": strategies, "account_id": account_id}), 200


@ strategies.route("/update", methods=["PUT"])
@ tokenrequired
@ errorhandler
def update_strategy(current_user):

    data = request.json

    _id = data['_id']

    data.pop("_id", None)

    resp = mongo.db.strategies.update_one(
        {"_id": ObjectId(_id)},
        {"$set": data})

    # if update did not occur because no account id found
    if resp.matched_count == 0 or resp.modified_count == 0:

        return jsonify({"error": "failed to update status", "_id": _id}), 400

    return jsonify({"success": "status updated", "_id": _id}), 201
