from flask import Flask
from flask_restful import Resource, Api
# RESOURCE:  represents an item an API can return or create
#   usually mapped into DB tables as well

# Flask will be our apps, and app will be root of route
app = Flask(__name__)

# allows us to easily add resources to the API
api = Api(app)

# API works with resources, & every resource has to be a class
class Student(Resource): # Student inherits from class Resource (flask_restful)
    def get(self, name):
        return {'student': name}

api.add_resource(Student, '/student/<string:name>')
# EXAMPLE:  http://127.0.0.1:5000/student/Kassandra
# replaces need for @app.route('/student/<string:name') as part of Student class

app.run(port=5000)
