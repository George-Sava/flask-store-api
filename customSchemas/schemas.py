from database import ma
from models.userModel import UserModel

class User(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserModel
        include_relationships = True

class UserOut(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel
        include_relationships = True

    id = ma.auto_field()
    email = ma.auto_field()
    role = ma.auto_field()
    created_at = ma.auto_field()
    stores = ma.auto_field()
    
