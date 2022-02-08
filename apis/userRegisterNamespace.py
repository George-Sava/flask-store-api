from flask_restx import Resource, reqparse, Namespace, Resource, fields
from core.tools.functions import  hash, check_email
from core.models.userModel import UserModel

api = Namespace('register', description='User Registration Endpoint', validate=True)

userRegisterModel = api.model('UserRegister', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
})

@api.route('/')
class UserRegister(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)

    parser.add_argument('email',type=str,required=True, help="This field cannot be left blank!")
    parser.add_argument('password',type=str,required=True, help="This field cannot be left blank!")

    @api.doc(responses={
        201: 'Created',
        400: 'Validation Error'
    })
    @api.expect(userRegisterModel, code=201)
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

class UserList(Resource):
    def get(self):
        return UserModel.get_all_users()
    