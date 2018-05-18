from db import db

class StoreModel(db.Model):  # tells SQLAlchemy it's something to save/add to db

    # tell ALchemy which table items will be stored in
    __tablename__ = "stores"

    # tell ALchemy which columns it will contain
    # creates an index & makes it easier to search
    id = db.Column(db.Integer, primary_key=True) # not used in prior code
    name = db.Column(db.String(80)) # can limit size of username

    # do a back reference to the ItemModel
    # allows a store to see which items are in the items DB
    # knows it is a many-to-1 relationship (list of items)
    # items = db.relationship('ItemModel')
    items = db.relationship('ItemModel', lazy='dynamic') #don't create obj for each item in ItemModel yet
    # self.items is no longer a list of items

    def __init__(self, name):
        """
        Upon creation of StoreModel, will have attribuate "name"

        """
        # these items must match the columns above
        # if they're not created above, they won't be stored to the DB

        self.name = name

    def json(self):
        """
        Return JSON representation of the model.

        """

        # return {'name': self.name, 'items': self.items}
        # return {'name': self.name, 'items': [item.json for item in self.items]}
        # with lazy='dynamic' self.items is a query builder in items table
        # so until calling JSON method we're not looking into the table
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        """
        This function acts like the GET method - will return information
        from the database.
        """

        return cls.query.filter_by(name=name).first() # returns ItemModel obj

    def save_to_db(self):   # changed from insert once SQLAlchemy got involved
        """
        This function takes in an ItemModel object and saves it to the DB.

        """

        # this is helpful for both update and insert
        db.session.add(self) # session = coll of objs to add to DB
        db.session.commit()

    def del_from_db(self):
        """
        This function deletes an ItemModel object from the DB.

        """

        db.session.delete(self)
        db.session.commit()
