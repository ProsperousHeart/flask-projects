from flask import Flask
# from flask_restful import Resource, Api, reqparse
from flask_restful import Api
# RESOURCE:  represents an item an API can return or create
#   usually mapped into DB tables as well

from flask_jwt import JWT
from security import authenticate, identity

# from user import UserRegister
from resources.user import UserRegister
# from item import Item, ItemList
from resources.item import Item, ItemList

# Flask will be our apps, and app will be root of route
app = Flask(__name__)

# S6L84 - specify a configuration property
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # turns of flask_SQLAlchemy tracker (not SQLAlchemy)

# S6L85 - tell SQLAlchemy where to find db.py file
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"

# create key for authentication - this should NEVER be stored publicly!
# this is only for demonstration purposes ... use a DB or something
app.secret_key = 'jose'

# allows us to easily add resources to the API
api = Api(app)

# Use JWT for authentication using app
#   1 - creates new endpoint:   \auth
#   2 - uses functions from security.py to take in username/password
#   3 - find correct user object with that username
#   4 - comparew it's PW to the one received through /auth
#   5 - if matched, return user auth JWT token (to be sent with next request to make)
jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
# EXAMPLE:  http://127.0.0.1:5000/item/<string:name>
# replaces need for @app.route('/item/<string:name>') as part of Item class
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register') # calls the POST method

# To ensure if this file is imported, we don't call it
if __name__ == '__main__':  # else imported from elsewhere

    # import the SQLAlchemy item - only needed if run this way so
    # imported here instead of at the top - avoiding circular import
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)  # Flask allows a good way to see error messages
    # debug=True allows you to receive an HTML page
