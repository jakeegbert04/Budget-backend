from flask import request, jsonify
import requests
import time
import os

from urllib.parse import urlparse

ACCESS_URL = os.getenv("ACCESS_URL")

def _get_auth():
    parsed = urlparse(ACCESS_URL)
    base = f"{parsed.scheme}://{parsed.hostname}{parsed.path}"
    return base, (parsed.username, parsed.password)

def get_accounts():
    try:
        base_url, auth = _get_auth()
        response = requests.get(f"{base_url}/accounts", auth=auth)
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def get_transactions():
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    params = {}
    if not start_date:
        params["start-date"] = int(time.time()) - (7 * 86400)
    if end_date:
        params["end-date"] = end_date

    try:
        response = requests.get(f"{ACCESS_URL}/accounts", params=params)
        response.raise_for_status()
        data = response.json()

        all_transactions = []
        for account in data.get("accounts", []):
            for txn in account.get("transactions", []):
                txn["account_name"] = account.get("name")
                txn["account_id"] = account.get("id")
                all_transactions.append(txn)

        return jsonify(all_transactions)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# @app.route("/accounts/balance", methods=["GET"])
# def get_balances():
#     """Get just the balances for each account"""
#     try:
#         response = requests.get(f"{ACCESS_URL}/accounts")
#         response.raise_for_status()
#         data = response.json()

#         balances = [
#             {
#                 "account_id": acct.get("id"),
#                 "name": acct.get("name"),
#                 "balance": acct.get("balance"),
#                 "currency": acct.get("currency"),
#                 "balance_date": acct.get("balance-date"),
#             }
#             for acct in data.get("accounts", [])
#         ]

#         return jsonify(balances)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500