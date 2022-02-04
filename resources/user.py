from flask_jwt import jwt_required, current_identity
from flask_restful import Resource, reqparse
from tools.functions import cleanNullTerms, hash, check_email
from models.userModel import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)

    parser.add_argument('email',type=str,required=True, help="This field cannot be left blank!")
    parser.add_argument('password',type=str,required=True, help="This field cannot be left blank!")

    def post(self):
        data=UserRegister.parser.parse_args()

        user = UserModel(**data)
        user.password = hash(user.password)

        if not check_email(user.email):
            return {"message": "Invalid email address!"}
        
        if UserModel.find_by_email(email=user.email):
            return {"message": "Username allready exists!"}, 400
        
        user.add_user()
        return user.to_json(), 201
    
class User(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)

    def get(self,id):
        user = UserModel.find_by_id(id)
        if not user:
            return {'message': 'User with ID:{}, does not exist!'.format(id)}
        return user.to_json()
    
    @jwt_required()
    def delete(self, id):
        user = UserModel.find_by_id(id)
        current_user = current_identity
        
        if not user:
            return {'message': 'User with ID:{}, does not exist!'.format(id)
        },404
        
        if user.id == current_user.id or current_user.role == 'admin':
            result = user.remove_user()
            return {"message": result}, 202
        
        return { "message": "You do not have permission!" },202

    @jwt_required()
    def put(self, id):
        User.parser.add_argument('email',type=str,required=False, help="This field cannot be left blank!")
        User.parser.add_argument('password',type=str,required=False, help="This field cannot be left blank!")
        User.parser.add_argument('is_active',type=bool,required=False, help="User State!")
        User.parser.add_argument('role',type=str,required=False, help="User role")
        
        user = UserModel.find_by_id(id)
        data = cleanNullTerms(User.parser.parse_args())
        current_user = current_identity
        
        if user.id != current_user.id and current_user.role != 'admin' :
            return {"message": "You do not have permission!"}, 403
        
        if not user:
            return {'message': 'User with ID:{}, does not exist!'.format(id)
        },404
        if not data:
            return {'error': 'No data added in request!'},422
        
        user.update(**data)
        
        return user.to_json(),202

class UserList(Resource):
    def get(self):
        return UserModel.get_all_users()
    