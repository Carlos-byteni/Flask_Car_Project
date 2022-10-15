from modelo.user import UserModel


def authenticate(username, password):
    user = UserModel.get_username(username)
    if user and user.password == password:
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.get_id(user_id)
