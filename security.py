from werkzeug.security import safe_str_cmp
from core.models.userModel import UserModel
from core.tools.functions import verify


def authenticate(email, password):
    user = UserModel.find_by_email(email)
    if user and verify(password, user.password):
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)