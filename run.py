from flask_jwt import JWT
from security import authenticate, identity
from app import application
from database import db
from apis import api

jwt = JWT(application, authenticate, identity) # /auth

# api.add_resource(User,"/users/<int:id>")
# api.add_resource(UserRegister,'/register')
# api.add_resource(UserList, "/users/")
# api.add_resource(Stores, "/stores/")
# api.add_resource(StoreList, "/stores/all")
# api.add_resource(Items, '/items/')
# api.add_resource(ItemList, '/items/all')

db.init_app(application)
api.init_app(application)

@application.before_first_request
def create_all():
    db.create_all(app=application)

if __name__ == "__main__":
      
    application.run(port=5000,debug=True)