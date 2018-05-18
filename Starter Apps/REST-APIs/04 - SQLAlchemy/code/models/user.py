import sqlite3
from db import db

# class UserModel:
class UserModel(db.Model):  # tells SQLAlchemy it's something to save/add to db
    """
    This is not a resource because the API cannot receive data into this class
    or send as a JSON representation. It is a helper used to store data about
    the user & contains methods to retrieve user objects from a DB.

    This is now an API. (Just not a REST API)
    These 2 methods are an interface into another part of the program

    """

    # tell ALchemy which table items will be stored in
    __tablename__ = "users"

    # tell ALchemy which columns it will contain
    # creates an index & makes it easier to search
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80)) # can limit size of username
    password = db.Column(db.String(80))

    # def __init__(self, _id, username, password):
    #     # these items must match the columns above
    #     # if they're not created above, they won't be stored to the DB
    #     self.id = _id
    def __init__(self, username, password):
        # these items must match the columns above
        # if they're not created above, they won't be stored to the DB
        self.username = username
        self.password = password

    @classmethod
    # def find_by_username(self, username):
    def find_by_username(cls, username):
        """
        This function takes in a username string and will search the database.
        If found, returns user otherwise None.

        """

        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        #
        # # WHERE limits the selection to only be rows that match
        # query = "SELECT * FROM users WHERE username=?"
        # result = cursor.execute(query, (username,))
        # row = result.fetchone() # returns None if not found
        # if row:
        #     # each element of row should match the init method input items
        #     # user = User(row[0], row[1], row[2])
        #     # user = cls(row[0], row[1], row[2])    # use curr. class vs hard code
        #     user = cls(*row)    # use curr. class vs hard code - pass in *args
        # else:
        #     user = None
        #
        # connection.close()
        # return user

        # this is a classmethod so cls
        # using SQLAlchemy's query builder
        #   - ability to do a DB query (SELECT * FROM users)
        # then filtered on username & returning the 1st "row" as a UserModel obj
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id):
        """
        This function takes in a username string and will search the database.
        If found, returns user otherwise None.

        """

        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        #
        # # WHERE limits the selection to only be rows that match
        # query = "SELECT * FROM users WHERE id=?"
        # result = cursor.execute(query, (_id,))
        # row = result.fetchone() # returns None if not found
        # if row:
        #     # each element of row should match the init method input items
        #     user = cls(*row)    # use curr. class vs hard code - pass in *args
        # else:
        #     user = None
        #
        # connection.close()
        # return user

        return cls.query.filter_by(id=_id).first() # no way 2 avoid id in SQLAlchemy


    def save_to_db(self):
        """
        This function takes in a UserModel object and saves it to the DB.

        """

        db.session.add(self)
        db.session.commit()


    def del_from_db(self):
        """
        This function deletes a UserModel object from the DB.

        """

        db.session.add(self)
        db.session.commit()
