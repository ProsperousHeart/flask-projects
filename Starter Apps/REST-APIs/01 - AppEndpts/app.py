# This is a basic flask.Flask app for "Hello World"
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# later will do object oriented programming (OOP)
# or using databases ... this is just to get feet wet
stores = [
    {
        'name': 'My Wonderful Store',
        'items': [
            {
            'name': 'My Item',
            'price': 15.99
            }
        ]
    }
]

# render_template HTML for home page
# this automatically looks in templates folder
@app.route('/')
def home():
	return render_template('index.html')

# This is acting like a web server
# REST API will use the following (opposite from browser)
#	POST - used to receive data
#	GET - used to send data back only

# This script is the beginning of a store ...

# POST /store data: {name:}
# @app.route('/store') - by default this is a GET request
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()  # request made to endpoint
    new_store = {
        'name': request_data['name'],
    'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)

# GET /store/<string:name>
@app.route('/store/<string:name>', methods=['GET']) # 'http://127.0.0.1:5000/some_name'
def get_store_name(name):
	# iterate over stores - return if matching else return error message
    req_store = [store for store in stores if store['name'] == name]
    if len(req_store) > 0:
        return jsonify(req_store[0])
    else:
        return jsonify({'message': 'store not found'})

# GET /store
@app.route('/store', methods=['GET'])
def get_stores():
	return jsonify({'stores': stores})

# POST /store/<string:name>/item {name:, price:}
@app.route('/store/<string:name>/item', methods=['POST'])
def create_store_item(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)    # could also return store
    return jsonify({'message': 'store not found'})

# GET /store/<string:name>/item
@app.route('/store/<string:name>/item', methods=['GET'])
def get_store_items(name):
	# iterate over items in store - return if matching else return error message

    for store in stores:
        if store['name'] == name:
            return jsonify[store['items']]
    return jsonify({'message': 'store not found'})

app.run(port=5000)
