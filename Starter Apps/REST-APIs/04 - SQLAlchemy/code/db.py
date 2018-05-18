from flask_sqlalchemy import SQLAlchemy

# Create a SQLItem() object that will link to the Flask app
# This will allow it to look at the objects we tell it to
db = SQLAlchemy()
