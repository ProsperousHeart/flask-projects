# This is a basic flask.Flask app for "Hello World"
from flask import Flask

app = Flask(__name__)

# homepage of the site
@app.route('/')
def home():
    return "Hello world!"

app.run(port=5000)
