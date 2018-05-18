from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    """
    Extends the Resource class into new class Store.
    This allows for GET, POST, and DELETE inputs.

    """

    # parser = reqparse.RequestParser()
    # parser.add_argument('name',
    #     type=float,
    #     required=True,
    #     help="This field cannot be left blank and must be a float!"
    # )
    # parser.add_argument('store_id',
    #     type=int,
    #     required=True,
    #     help="Every item requires a store ID as an integer!"
    # )

    def get(self, name):
        """
        Returns a specific store.

        """

        # return None or a StoreModel object
        store = StoreModel.find_by_name(name)

        if store:
            return store.json(), 200 # also rtns the items

        return {'message': "Store '{}' not found.".format(name)}, 404

    def post(self, name):
        """
        Add new store if not already created.

        """

        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': "An error occurred while creating the store."}, 500

        return store.json(), 201

    def delete(self, name):
        """
        If store exists, remove from DB.

        """

        store = StoreModel.find_by_name(name)
        if store:
            store.del_from_db()
            return {'message':  "Store '{}' deleted from DB.".format(name)}, 201
        return {'message':  "Store '{}' not in DB."}, 200


class StoreList(Resource):
    """
    Return a dict of stores where each store is it's own JSON.

    """

    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
