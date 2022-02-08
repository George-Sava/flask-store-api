from flask_jwt import jwt_required, current_identity
from flask_restx import Resource, reqparse
from core.models.storeModel import StoreModel

class Stores(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    
    @jwt_required()
    def get(self):
        user  = current_identity
        result = StoreModel.get_stores(user.id)
        store_list = []
        
        for store in result:
            store_list.append(store.to_json())
            
        if not store_list:
            return {'message': 'User has no stores!'},404
        
        return store_list
    
    @jwt_required()
    def post(self):
        post_parser = Stores.parser.copy()
        post_parser.add_argument('store_name',type=str,required=True, help="This field cannot be left blank!")
        
        data = post_parser.parse_args()

        user = current_identity

        if StoreModel.get_by_name(data['store_name']):
            return {'message':'Store with name: {} allready exist!'.format(data['store_name'])}
        
        store = StoreModel(**data, owner_id = user.id).create_store()
        
        return store.to_json(),201

    @jwt_required()
    def put(self):
        put_parser = Stores.parser.copy()
        put_parser.add_argument('store_id',type=int,required=True, help="This field cannot be left blank!")
        put_parser.add_argument('store_name',type=str,required=False, help="This field cannot be left blank!")
        put_parser.add_argument('store_address',type=str,required=False, help="This field cannot be left blank!")
        
        data = put_parser.parse_args()

        store = StoreModel.find_by_id(data['store_id'])
        current_user = current_identity
        
        if not store:
            return {'message': 'Store with ID:{}, does not exist!'.format(data['store_id'])
        },404
        
        if store.owner_id != current_user.id and current_user.role != 'admin' :
            return {"message": "You do not have permission!"}, 403
        
        if not data:
            return {'error': 'No data added in request!'},422
        
        store.update(**data)
        
        return store.to_json(),202
    
    @jwt_required()
    def delete(self):
        delete_parser = Stores.parser.copy()
        delete_parser.add_argument('store_id',type=int,required=True, help="This field cannot be left blank!")

        data = delete_parser.parse_args()
        store = StoreModel.find_by_id(_id=data['store_id'])
        current_user = current_identity

        if not store:
            return {'message': 'Store with ID:{}, does not exist!'.format(data['store_id'])
        },404
        
        if store.owner_id == current_user.id or current_user.role == 'admin':
            result = store.remove_store()
            return {"message": result}, 202
        
        return { "message": "You do not have permission!" },202
        
        
class StoreList(Resource):
    def get(self):
        return StoreModel.get_all_stores()