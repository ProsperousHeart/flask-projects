# 1st Iteration Through Security  (user setup)
# ====================================
#   # in memory table of registered users
#   users = [
#       {
#           'id': 1,
#           'username': 'bob',
#           'password': 'asdf'
#       }
#   ]
#   
#   # create an "index" on username "bob"
#   username_mapping = { 'bob': {
#       'id': 1,
#       'username': 'Bob',
#       'password': 'asdf'
#   }}
#   
#   # create an "index" on id 1
#   userid_mapping = { 1: {
#       'id': 1,
#       'username': 'Bob',
#       'password': 'asdf'
#   }}
#   
#   def authenticate(username, password):
#       """
#       This function takes in a username and password, then checks for authentication.
#   
#       """
#   
#       user = username_mapping.get(username, None) # username_mapping[username] or None
#       if user and user.password == password:
#           return user
#   
#   # unique to flask-JWT
#   # takes in contents of JWT token
#   def identity(payload):
#       user_id = payload['identity']
#       return userid_mapping.get(user_id, None)

# ==========================
# 2nd Iteration For Security (user setup)
# ==========================

from user import User
from werkzeug.security import safe_str_cmp

users = [
    User(1, 'bob', 'asdf')
]

# create an "index" on username "bob"
username_mapping = {u.username: u for u in users}   # set comprehension assigning KV pairs
userid_mapping = {u.id: u for u in users}

def authenticate(username, password):
    """
    This function takes in a username and password, then checks for authentication.

    """

    user = username_mapping.get(username, None) # username_mapping[username] or None
    # if user and user.password == password:
    if user and safe_str_cmp(user.password, password):
        return user

# unique to flask-JWT
# takes in contents of JWT token
def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)