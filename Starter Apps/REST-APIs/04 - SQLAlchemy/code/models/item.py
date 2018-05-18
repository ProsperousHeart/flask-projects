import sqlite3
from db import db

# class ItemModel:
class ItemModel(db.Model):  # tells SQLAlchemy it's something to save/add to db

    # tell ALchemy which table items will be stored in
    __tablename__ = "items"

    # tell ALchemy which columns it will contain
    # creates an index & makes it easier to search
    id = db.Column(db.Integer, primary_key=True) # not used in prior code
    name = db.Column(db.String(80)) # can limit size of username
    price = db.Column(db.Float(precision=2)) # limit number of decimal pts

    def __init__(self, name, price):
        """
        Since internal representation, must also contain properties of an item
        as object properties.

        """
        # these items must match the columns above
        # if they're not created above, they won't be stored to the DB

        self.name = name
        self.price = price

    def json(self):
        """
        Return JSON representation of the model.

        """

        return {'name': self.name, 'price': self.price}

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
            # return {'item': row[0], 'price': row[1]}
            # return cls(row[0], row[1])
            return cls(*row) # row[0] == name, row[1] == price
        # return {"message": "Item '{}' not found.".format(name)}, 404

    # @classmethod
    # def insert(cls, item):
    def insert(self):
        """
        Takes the connection & insertion using sqlite from post into this
        function. Takes in an item, if there updates item. Otherwise, inserts.
        """

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES(?, ?)"
        # cursor.execute(query, (item['name'], item['price']))
        cursor.execute(query, (self.name, self.price))

        connection.commit()
        connection.close()

    # @classmethod
    # def update(cls, item):
    def update(self):
        """
        Takes in a JSON item to insert or update to items table.
        """

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query, (self.price, self.name))

        connection.commit()
        connection.close()
