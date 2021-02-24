import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity     # created in security.py file
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False                 # DATABASE_URL" - is a variable defined in
app.config['PROPAGATE_EXCEPTIONS'] = True                            # Haroku, which refer to postgres Haroku database
                                                                     # second argument is a local database
app.secret_key = "jose"
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth ; Every restart the JWS will update

api.add_resource(Store, "/store/<string:name>")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(StoreList, "/stores")

api.add_resource(UserRegister, "/register")


if __name__ == "__main__":     # to prevent running app, when importing anything from this file
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
