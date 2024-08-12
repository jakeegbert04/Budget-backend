from flask import Flask
from db import *
import os
from flask_marshmallow import Marshmallow
from flask_cors import CORS

from routes.auth_routes import auth
from routes.user_routes import user
from routes.category_routes import category
from routes.account_routes import account
from routes.transaction_routes import transaction

database_pre = os.environ.get("DATABASE_PRE")
database_addr = os.environ.get("DATABASE_ADDR")
database_user = os.environ.get("DATABASE_USER")
database_port = os.environ.get("DATABASE_PORT")
database_name = os.environ.get("DATABASE_NAME")
database_pass = os.environ.get("DATABASE_PASS")

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = f"{database_pre}{database_user}:{database_pass}@{database_addr}:{database_port}/{database_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

init_db(app, db)
CORS(app)
ma = Marshmallow(app)

app.register_blueprint(auth)
app.register_blueprint(user)
app.register_blueprint(category)
app.register_blueprint(account)
app.register_blueprint(transaction)

def create_all():
    with app.app_context():
        print("Creating Tables")
        db.create_all()
        print("All Done")

create_all()
if __name__ == "__main__":
    app.run(port=8089, host="0.0.0.0", debug=True)