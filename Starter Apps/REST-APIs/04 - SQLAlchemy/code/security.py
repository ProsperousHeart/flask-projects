from resources.user import User
from werkzeug.security import safe_str_cmp

# users = [
#     User(1, 'bob', 'asdf')
# ]
#
# # create an "index" on username "bob"
# username_mapping = {u.username: u for u in users}   # set comprehension assigning KV pairs
# userid_mapping = {u.id: u for u in users}

def authenticate(username, password):
    """
    This function takes in a username and password, then checks for authentication.

    """

    # user = username_mapping.get(username, None) # username_mapping[username] or None
    user = User.find_by_username(username)
    # if user and user.password == password:
    if user and safe_str_cmp(user.password, password):
        return user

# unique to flask-JWT
# takes in contents of JWT token
def identity(payload):
    user_id = payload['identity']
    # return userid_mapping.get(user_id, None)
    return User.find_by_id(user_id)
