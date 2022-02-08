from flask_restx import Api, Namespace

api = Api() 

homeNS = Namespace('home', api = api)
usersNS = Namespace('users', api = api)
storesNS = Namespace('stores', api = api)
itemsNS = Namespace('items', api = api)