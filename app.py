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
import config

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

    su_name = f'{config.su_first_name} {config.su_last_name}'

    print(f"Querying for {su_name} user...")

    user_data = query(Users).filter(Users.email == config.su_email).first()

        super_admin_role = query(Roles).filter(Roles.name == 'super_admin').first()

        if user_data is None:

            print(f"{su_name} not found! Creating {config.su_email} user...")

            newpw = os.getenv('ON_MESSAGE_ADMIN_PW', '')

            while newpw == '' or newpw is None:
                newpw = input(f' Enter a password for {su_name}:')

                password = newpw
                hashed_password = bcrypt.generate_password_hash(password).decode("utf8")

                db.session.flush()

                record = Users(
                    first_name=config.su_first_name,
                    last_name=config.su_last_name,
                    email=config.su_email,
                    password=hashed_password,
                    active=True,
                )
                record.roles.append(super_admin_role)

                db.session.add(record)

                db.session.commit()

        else:
            print(f"{su_name} user found!")
    with app.app_context():
        print("Creating Tables")
        db.create_all()
        print("All Done")

create_all()
if __name__ == "__main__":
    app.run(port=8089, host="0.0.0.0", debug=True)