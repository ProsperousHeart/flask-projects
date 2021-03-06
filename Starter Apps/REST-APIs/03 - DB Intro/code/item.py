import sqlite3
from flask import request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

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

        # # setup connection to database
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        #
        # query = "SELECT * FROM items WHERE name=?"
        # result = cursor.execute(query, (name,))
        # row = result.fetchone() # there should only be 1
        # connection.close()
        # # return {'item': item}, 200 if row else 404
        # if row:
        #     return {'item': row[0], 'price': row[1]}

        item = self.find_by_name(name)
        if item:
            return item

        return {"message": "Item '{}' not found.".format(name)}, 404

    @classmethod
    def find_by_name(cls, name):
        """
        This function acts like the GET method - will return information
        from the database.

        """

        # setup connection to database
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone() # there should only be 1
        connection.close()
        # return {'item': item}, 200 if row else 404
        if row:
            return {'item': row[0], 'price': row[1]}
        # return {"message": "Item '{}' not found.".format(name)}, 404

    @jwt_required()
    def post(self, name):
        """
        This will add a new item - currently does not check for duplicates.
        Returns the updated set of items, and 201 code (202 is ACCEPTED)

        """
        # if next(filter(lambda x: x['name'] == name, items), None) is not None:
            # """
            # If None is not returned, we do not want to create a new item.
            # Returns the item information & 400 (Bad Request).
            # ~ PUT would update!
            #
            # """
            #
            # return {'message': "An item with name '{}' already exists!".format(name)}, 400
        # since no longer built-in, must use updated GET method
        # in order to check if already there
        # - required creation of classmethod find_by_name(cls, name)

        if self.find_by_name(name): # could also call Item.find_by_name()
            return {'message': "An item with name '{}' already exists!".format(name)}, 400

        # data = request.get_json()   # will give an error if improper type or content
        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}

        # items.append(item)
        # Since writing to a DB now ...

        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        # query = "INSERT INTO items VALUES (?, ?)"
        # cursor.execute(query, (item['name'], item['price']))
        #
        # connection.commit()
        # connection.close()
        try:
            self.insert(item)   # able to do this after creating classmethod insert
        except:
            # should never be this - WAY too general!!!!!
            return {'message': "An error occurred calling insert()"}, 500   # internal server error

        # return items, 201    # tells app like POSTMAN that successful, 201 - CREATED
        return item, 201    # tells app like POSTMAN that successful, 201 - CREATED
        # 202 - ACCEPTED (when delaying the creation ... such as if it takes a long time)

    @classmethod
    def insert(cls, item):
        """
        Takes the connection & insertion using sqlite from post into this
        function. Takes in an item, if there updates item. Otherwise, inserts.

        """

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES(?, ?)"
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    @jwt_required()
    def delete(self, name):
        # global items
        # items = list(filter(lambda x: x['name'] != name, items))
        # if len(items) > 0:
        #     return {'message':  "Item '{}' deleted.".format(name)}, 200
        # return {'message': "Unable to locate '{}'".format(name)}, 404

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': "Confirmed item '{}' deleted.".format(name)}

    @jwt_required()
    def put(self, name):

        # global items
        # item = next(filter(lambda x: x['name'] == name, items), None)

        # data = request.get_json()
        data = Item.parser.parse_args()

        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}

        if item is None:
            # item = {'name': name, 'price': data['price']}
            # items.append(item)
            try:
                self.insert(updated_item)
            except:
                # too general
                return {'message': 'An error occurred inserting the item.'}, 500
        else:
            # item.update(data)
            try:
                self.update(updated_item)
            except:
                # too general
                return {'message': 'An error occurred inserting the item.'}, 500
        # return item
        return updated_item

    @classmethod
    def update(cls, item):
        """
        Takes in a JSON item to insert or update to items table.

        """

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

class ItemList(Resource):
    def get(self):
        """
        Returns dictionary/JSON of items.

        """

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        rows = cursor.execute(query)
        # to_rtn = {'items': list(rows)}
        items = []
        for row in rows:
            items.append({'name': row[0], 'price': row[1]})

        connection.close()

        # return {'items': list(rows)}, 200
        # return to_rtn, 200
        return {'items': items}
