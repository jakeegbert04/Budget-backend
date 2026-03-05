from flask import request, jsonify, json

from controllers.auth_controller import validate_session
from models.categories import CategoriesSchema
from models.transactions import Transactions
from models.accounts import Accounts
from models.users import Users
from lib.authenticate import auth, auth_with_return
from lib.gemini_service import get_gemini_client
from datetime import datetime
from db import db
import requests
import time
import os

from urllib.parse import urlparse

ACCESS_URL = os.getenv("ACCESS_URL")

def _to_unix(date_str):
    return int(datetime.strptime(date_str, "%Y-%m-%d").timestamp())

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

@auth_with_return
def sort_transactions(auth_info):
    if not auth_info:
        return jsonify({"error": "Unauthorized"}), 401
    
    body = request.get_json() or {}
    start_date = body.get("start_date")  # expects "2024-03-04"
    end_date = body.get("end_date")      # expects "2024-03-04"

    params = {}
    params["start-date"] = _to_unix(start_date) if start_date else int(auth_info.last_sign_in.timestamp())
    params["end-date"] = _to_unix(end_date) if end_date else int(time.time())

    try:
        base_url, auth_creds = _get_auth()
        response = requests.get(f"{base_url}/accounts", params=params, auth=auth_creds)
        response.raise_for_status()
        data = response.json()

        # Flatten all transactions across all accounts into a single list
        all_transactions = []
        for account in data.get("accounts", []):
            for txn in account.get("transactions", []):
                txn["account_name"] = account.get("name")
                txn["account_id"] = account.get("id")
                all_transactions.append(txn)

        # Strip down to only what Gemini needs — keeps the payload small and cheap
        trimmed_transactions = [
        {
            "id": txn["id"],
            "description": txn.get("description", ""),
            "payee": txn.get("payee", ""),
            # "amount": txn.get("amount", "")
        }
        for txn in all_transactions
        ]

        # Fetch the user's custom categories to pass into the prompt
        user = Users.query.get(auth_info.user_id)
        categories = user.categories
        category_list = [c.name for c in categories]

        # Tell Gemini to categorize and condense each transaction, returning structured JSON
        prompt = f"""
        You are a personal finance assistant. Categorize each transaction into one of the provided categories. For the description please condense it so it's easy to understand but we still know where it came from.

        Categories: {category_list}

        Transactions:
        {json.dumps(trimmed_transactions, indent=2)}

        Return ONLY a JSON array in this exact format, no explanation:
        [
        {{"id": "TRN-xxx", "category": "category name", "description": "condensed description name"}},
        ...
        ]

        If a transaction doesn't fit any category, use "Uncategorized".
        """

        client = get_gemini_client()
        gemini_response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt
        )

        # Strip markdown code fences if Gemini wraps the response in ```json ... ```
        raw = gemini_response.text.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        gemini_result = json.loads(raw.strip())

        category_map = {item["id"]: item for item in gemini_result}

        # Merge Gemini's category and condensed description back onto each transaction
        for txn in all_transactions:
            match = category_map.get(txn["id"])
            txn["category"] = match["category"] if match else "Uncategorized"
            txn["description"] = match["description"] if match else txn.get("description", "")

        # Look up the local Everyday Checking account to associate with saved transactions
        checking_account = Accounts.query.filter_by(user_id=user.user_id, name="Everyday Checking").first()
        if not checking_account:
            return jsonify({"error": "Everyday Checking account not found"}), 404

        # Save each categorized transaction to the DB, skipping uncategorized ones
        for txn in all_transactions:
            if txn["category"] == "Uncategorized":
                continue

            matched_category = next((c for c in categories if c.name == txn["category"]), None)
            if not matched_category:
                continue

            new_txn = Transactions(
                user_id=user.user_id,
                category_id=matched_category.category_id,
                account_id=checking_account.account_id,
                amount=txn.get("amount", "0"),
                description=txn.get("description", ""),
                date=datetime.fromtimestamp(txn.get("transacted_at", int(time.time()))),
                frequency=None,
                end_date=None,
                indefinitely=False,
            )
            db.session.add(new_txn)

        db.session.commit()

        

        return jsonify({"transactions": all_transactions})
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