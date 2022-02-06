from app import application
from database import db,ma

db.init_app(application)
ma.init_app(application)

@application.before_first_request()
def create_tables():
    db.create_all(app=application)