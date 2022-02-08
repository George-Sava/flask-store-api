from flask_restx import Api

from .homeNamespace import api as homeNS
from .userRegisterNamespace import api as userRegisterNS
from .usersNamespace import api as usersNS
# from .namespace2 import api as ns2
# # ...
# from .namespaceX import api as nsX

api = Api(
    title='Store Chain API',
    version='1.1',
    description='Store Chain API using python Flask-RESTx',
    # All API metadatas
)

api.add_namespace(homeNS)
api.add_namespace(userRegisterNS)
api.add_namespace(usersNS)
# api.add_namespace(ns2)
# # ...
# api.add_namespace(nsX)