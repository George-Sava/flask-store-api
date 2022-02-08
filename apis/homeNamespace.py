from flask_restx import Namespace, Resource, fields

api = Namespace('home', description='Test Homepage')

# cat = api.model('Cat', {
#     'id': fields.String(required=True, description='The cat identifier'),
#     'name': fields.String(required=True, description='The cat name'),
# })

# CATS = [
#     {'id': 'felix', 'name': 'Felix'},
# ]

@api.route('/')
class Home(Resource):
    
    def get(self):
        return {"message": "App is running!"}
