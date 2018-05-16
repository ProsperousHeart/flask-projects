import sqlite3
from flask_restful import Resource, reqparse

class User:
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
		row = result.fetchone()	# returns None if not found
		if row:
			# each element of row should match the init method input items
			# user = User(row[0], row[1], row[2])
			# user = cls(row[0], row[1], row[2])	# use curr. class vs hard code
			user = cls(*row)	# use curr. class vs hard code - pass in *args
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
		row = result.fetchone()	# returns None if not found
		if row:
			# each element of row should match the init method input items
			user = cls(*row)	# use curr. class vs hard code - pass in *args
		else:
			user = None

		connection.close()
		return user

class UserRegister(Resource):
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
		if User.find_by_username(data['username']) is not None:
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
