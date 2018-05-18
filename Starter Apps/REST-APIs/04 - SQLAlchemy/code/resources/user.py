import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    """
    This is the external representation of a resource/entity. APIs or mobile
    apps think they're interacting with resources.

    """

    # created as a Resource so we can add to User class
    # in FlaskRESTful

    # create a RequestParser that accepts a username/password
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be blank and must be a string."
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be blank and must be a string."
    )

    def post(self):

        # parse JSON data coming in from RequestParser
        data = UserRegister.parser.parse_args()

        # check if user is already in DB
        # must be done before another connection due to User class
        if UserModel.find_by_username(data['username']) is not None:
            return {"message": "User {} already exists.".format(data['username'])}, 409

        # create connection & cursor
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # create & execute insertion query of new user
        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        # commit changes
        connection.commit()

        # close connection
        connection.close()

        # return 201 (successful add/create)
        return {"message": "User {} created successfully.".format(data['username'])}, 201
