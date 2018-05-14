from flask import Flask, request
from flask_restful import Resource, Api, reqparse
# RESOURCE:  represents an item an API can return or create
#   usually mapped into DB tables as well

from flask_jwt import JWT, jwt_required
from security import authenticate, identity

# Flask will be our apps, and app will be root of route
app = Flask(__name__)

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

items = []

# API works with resources, & every resource has to be a class
class Item(Resource): # Item inherits from class Resource (flask_restful)

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank and must be a float!"
    )
    
    @jwt_required()
    def get(self, name):
        """
        This function returns the information of a requested item.
        If not found, returns a dictionary with None and code 404
        
        """

        # =================================================================
        # This was the first step of learning ...
        # =================================================================
        #    item_list = [item for item in items if item['name'] == name]
        #    if len(item_list) > 0:
        #        return item_list[0], 200

        #   # return {'message': "{} not found".format(name.upper())}
        #   # when returning 2 items, the 2nd is the return code (otherwise 200)
        #   # 404 - Not Found
        #   return {"item": None}, 404

        # =================================================================
        # It transitioned to using filter - next step in improvement
        # =================================================================
        # item = filter(lambda x: x['name'] == name, items)   # returns a filter object
        # item = list(filter(lambda x: x['name'] == name, items))
        item = next(filter(lambda x: x['name'] == name, items), None)
        return {'item': item}, 200 if item else 404

    @jwt_required()
    def post(self, name):
        """
        This will add a new item - currently does not check for duplicates.
        Returns the updated set of items, and 201 code (202 is ACCEPTED)

        """
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            """
            If None is not returned, we do not want to create a new item.
            Returns the item information & 400 (Bad Request).
            ~ PUT would update!

            """
            return {'message': "An item with name '{}' already exists!".format(name)}, 400

        # data = request.get_json()   # will give an error if improper type or content
        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}
        items.append(item)
        return items, 201    # tells app liek POSTMAN that successful, 201 - CREATED
        # 202 - ACCEPTED (when delaying the creation ... such as if it takes a long time)

    @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message':  "Item '{}' deleted.".format(name)}

    @jwt_required()
    def put(self, name):
        
        global items
        item = next(filter(lambda x: x['name'] == name, items), None)
        
        # data = request.get_json()
        data = Item.parser.parse_args()

        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

class ItemList(Resource):
    def get(self):
        """
        Returns dictionary/JSON of items.

        """

        return {'items': items}, 200

api.add_resource(Item, '/item/<string:name>')
# EXAMPLE:  http://127.0.0.1:5000/item/<string:name>
# replaces need for @app.route('/item/<string:name>') as part of Item class
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)  # Flask allows a good way to see error messages
# debug=True allows you to receive an HTML page