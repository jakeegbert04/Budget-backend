import os
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_bcrypt import Bcrypt

from db import db, init_db
import config

from models.roles import Roles
from models.users import Users

from routes.auth_routes import auth
from routes.user_routes import user
from routes.category_routes import category
from routes.account_routes import account
from routes.role_routes import role
from routes.transaction_routes import transaction

from lib.demo_data.roles_demo_data import add_roles


def create_app():
    """
    Application factory for local use.
    Initializes app, configures database, and registers blueprints.
    """
    app = Flask(__name__)
    
    database_pre = os.environ.get("DATABASE_PRE")
    database_addr = os.environ.get("DATABASE_ADDR")
    database_user = os.environ.get("DATABASE_USER")
    database_port = os.environ.get("DATABASE_PORT")
    database_name = os.environ.get("DATABASE_NAME")
    database_pass = os.environ.get("DATABASE_PASS")
    
    app.config["SQLALCHEMY_DATABASE_URI"] = f"{database_pre}{database_user}:{database_pass}@{database_addr}:{database_port}/{database_name}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    init_db(app, db)
    CORS(app, supports_credentials=True)
    Marshmallow(app)
    Bcrypt(app)

    app.register_blueprint(auth)
    app.register_blueprint(user)
    app.register_blueprint(category)
    app.register_blueprint(account)
    app.register_blueprint(role)
    app.register_blueprint(transaction)

    return app


def create_all(app):
    """
    Sets up database schema and adds a super admin user if it does not exist.
    """
    with app.app_context():
        print("Creating tables...")
        db.create_all()
        add_roles()
        
        su_name = f'{config.su_first_name} {config.su_last_name}'
        print(f"Querying for {su_name} user...")

        user_data = db.session.query(Users).filter(Users.email == config.su_email).first()
        super_admin_role = db.session.query(Roles).filter(Roles.name == 'super_admin').first()

        if user_data is None:
            print(f"{su_name} not found! Creating {config.su_email} user...")
            
            newpw = os.getenv('PHOTO_ADMIN_PW', '')
            while not newpw:
                newpw = input(f'Enter a password for {su_name}: ')

            hashed_password = Bcrypt(app).generate_password_hash(newpw).decode("utf8")
            record = Users(
                username=config.su_username,
                first_name=config.su_first_name,
                last_name=config.su_last_name,
                email=config.su_email,
                password=hashed_password,
                active=True,
            )
            record.roles.append(super_admin_role)
            
            db.session.add(record)
            db.session.commit()
            print(f"{su_name} user created!")
        else:
            print(f"{su_name} user already exists!")

        print("All done.")


app = create_app()

if __name__ == "__main__":
    create_all(app)
    app.run(port=8089, host="0.0.0.0", debug=True)