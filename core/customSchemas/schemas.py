from run import api
from flask_restx import fields

user = api.model('User', {
    'email': fields.String,
    'password': fields.String
})