from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from database import db, ma
from security import authenticate, identity
from resources.user import UserRegister, User, UserList
from resources.stores import Stores, StoreList
from resources.items import Items, ItemList
from resources.home import Home

application = Flask(__name__)
application.config.from_object('config.DevConfig')

api = Api(application)
jwt = JWT(application, authenticate, identity) # /auth

api.add_resource(Home, '/')
api.add_resource(User,"/users/<int:id>")
api.add_resource(UserRegister,'/register')
api.add_resource(UserList, "/users/")
api.add_resource(Stores, "/stores/")
api.add_resource(StoreList, "/stores/all")
api.add_resource(Items, '/items/')
api.add_resource(ItemList, '/items/all')




