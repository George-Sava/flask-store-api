from flask_restx import Resource
from run import api

@api.route('/home')
class Home(Resource):

    def get(self):
        return {"message": "App is running!"}