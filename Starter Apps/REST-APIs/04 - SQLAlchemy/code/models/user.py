import sqlite3

class UserModel:
    """
    This is not a resource because the API cannot receive data into this class
    or send as a JSON representation. It is a helper used to store data about
    the user & contains methods to retrieve user objects from a DB.

    """

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    # def find_by_username(self, username):
    def find_by_username(cls, username):
        """
        This function takes in a username string and will search the database.
        If found, returns user otherwise None.

        """

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        # WHERE limits the selection to only be rows that match
        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(query, (username,))
        row = result.fetchone() # returns None if not found
        if row:
            # each element of row should match the init method input items
            # user = User(row[0], row[1], row[2])
            # user = cls(row[0], row[1], row[2])    # use curr. class vs hard code
            user = cls(*row)    # use curr. class vs hard code - pass in *args
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        """
        This function takes in a username string and will search the database.
        If found, returns user otherwise None.

        """

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        # WHERE limits the selection to only be rows that match
        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(query, (_id,))
        row = result.fetchone() # returns None if not found
        if row:
            # each element of row should match the init method input items
            user = cls(*row)    # use curr. class vs hard code - pass in *args
        else:
            user = None

        connection.close()
        return user
