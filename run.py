from app import application
from database import db,ma

db.init_app(application)
ma.init_app(application)

@application.before_first_request
def create_all():
    db.create_all(app=application)

if __name__ == "__main__":
      
    application.run(port=5000,debug=True)