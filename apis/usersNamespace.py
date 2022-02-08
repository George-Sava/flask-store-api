from flask_jwt import jwt_required, current_identity
from flask_restx import Resource, reqparse, Namespace, Resource, fields
from core.tools.functions import cleanNullTerms
from core.models.userModel import UserModel

api = Namespace('users', description='Users Resource Endpoint', validate=True)

userUpdate = api.model('UserRegister', {
    'email': fields.String(required=False, description='User email'),
    'role': fields.String(required=False, description='User role'),
    'is_active': fields.Boolean(required=False, description='User status'),
})

@api.route('/<int:id>')    
class User(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)

    @api.doc(responses={
        200: 'Success',
        404: 'Not Found'
    })
    def get(self,id):
        user = UserModel.find_by_id(id)
        if not user:
            return {'message': 'User with ID:{}, does not exist!'.format(id)},404
        return user.to_json()
    

    # @jwt_required()
    # def delete(self, id):
    #     user = UserModel.find_by_id(id)
    #     current_user = current_identity
        
    #     if not user:
    #         return {'message': 'User with ID:{}, does not exist!'.format(id)
    #     },404
        
    #     if user.id == current_user.id or current_user.role == 'admin':
    #         result = user.remove_user()
    #         return {"message": result}, 202
        
    #     return { "message": "You do not have permission!" },202

    @api.doc(responses={
        202: 'Entry Updated',
        401: 'Request does not contain an access token',
        403: 'Access Denied',
        422: 'Invalid Request'
    },security='basicAuth')
    @api.expect(userUpdate, code=202)
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
