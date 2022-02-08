from flask_restx import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from core.models.storeModel import StoreModel
from core.models.ItemModel import ItemModel
from core.tools.functions import cleanNullTerms



class Items(Resource):
    parser = reqparse.RequestParser(bundle_errors=True)
    
    def get(self):
        get_parser = Items.parser.copy()
        get_parser.add_argument('item_id',type=int,required=True, help="This field cannot be left blank!")
        
        data = get_parser.parse_args()
        item = ItemModel.find_by_id(data['item_id'])

        if not item:
            return {'message':'Invalid with ID:{}, does not exist!'.format(data['item_id'])}

        return item.to_json()

    @jwt_required()
    def post(self):
        post_parser = Items.parser.copy()
        post_parser.add_argument('item_name',type=str,required=True, help="This field cannot be left blank!")
        post_parser.add_argument('item_price',type=float,required=True, help="This field cannot be left blank!")
        post_parser.add_argument('store_id',type=int,required=True, help="This field cannot be left blank!")

        data = post_parser.parse_args()
        user = current_identity
        store = StoreModel.find_by_id(data['store_id'])

        if user.id != store.owner_id:
            return {'message':'You do not have permission!'}
        
        item = ItemModel(**data)
        
        item = item.add_item()
        
        return item.to_json(),201
        
    
    @jwt_required()
    def delete(self):
        delete_parser = Items.parser.copy()

        delete_parser.add_argument('item_id',type=int,required=True, help="This field cannot be left blank!")
        delete_parser.add_argument('store_id',type=int,required=True, help="This field cannot be left blank!")

        data = delete_parser.parse_args()
        item = ItemModel.find_by_id(data['item_id'])
        current_user = current_identity

        store = StoreModel.find_by_id(data['store_id'])

        if not store:
            return {'message': 'Store with ID:{}, does not exist!'.format(data['store_id'])}

        if not item:
            return {'message': 'Item with ID:{} , does not exist!'.format(data['item_id'])}

        if store.owner_id != current_user.id:
            return {'message': 'You do not have permission!'}
        
        if item.store_id == data['store_id'] or current_user.role == 'admin':
            result = item.remove_item()
            return {"message": result}, 202

        return { "message": "You do not have permission!" },202

        
    @jwt_required()
    def put(self):
        update_parser = Items.parser.copy()

        update_parser.add_argument('item_id',type=int,required=True, help="This field cannot be left blank!")
        update_parser.add_argument('item_name',type=str,required=False, help="This field cannot be left blank!")
        update_parser.add_argument('item_price',type=float,required=False, help="This field cannot be left blank!")
        update_parser.add_argument('on_discount',type=bool,required=False, help="This field cannot be left blank!")


        data =cleanNullTerms(update_parser.parse_args())

        item = ItemModel.find_by_id(data['item_id'])

        current_user = current_identity

        store = StoreModel.find_by_id(item.store_id)
        
        if not item:
            return {'message': 'Item with ID:{}, does not exist!'.format(data['store_id'])
        },404

        if not store:
            return {'message': "Ups something is wrong with the store"
        },404
        
        if item.store_id != store.id and current_user.role != 'admin' :
            return {"message": "You do not have permission!"}, 403
        
        if not data:
            return {'error': 'No data added in request!'},422
        
        item.update(**data)
        
        return item.to_json(),202
    
class ItemList(Resource):
    def get(self):
        return ItemModel.get_all_items()