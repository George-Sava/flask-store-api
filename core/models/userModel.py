# from time import strftime
from core.models.storeModel import StoreModel
from database import db


class UserModel(db.Model):
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key= True, nullable= False)
    is_active = db.Column(db.Boolean, nullable= False,server_default='TRUE')
    email = db.Column(db.String, nullable= False, unique= True)
    password = db.Column(db.String, nullable= False)
    role = db.Column(db.String, nullable= False, server_default='user')
    created_at = db.Column(db.TIMESTAMP(timezone= True), nullable= False, server_default=db.text('now()'))
    stores = db.relationship('StoreModel', overlaps='owner')
    
        
    def to_json(self):
        time = self.created_at
        return { 'id': self.id, 'email': self.email, 'is_active': self.is_active, 'role': self.role , 'created_at': time.strftime('%m.%d.%Y / %H:%M:%S')
        } # 'stores': [store.to_json() for store in self.stores] --> if want to attach store model to user
        
    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
        
    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def get_all_users(cls):
        userList = []
        result = cls.query.all()
        for user in result:
            userList.append(user.to_json())
        return userList
    
    def add_user(self):
        db.session.add(self)
        db.session.commit()
        
    def remove_user(self):
        db.session.delete(self)
        db.session.commit()
        return "Record deleted!"
    
    def get_stores(self,id):
        return StoreModel.get_stores(id)
    
    def update(self, **kwargs):
        for k,v in kwargs.items():
            self.__setattr__(k, v)
        db.session.commit()
        return self
            