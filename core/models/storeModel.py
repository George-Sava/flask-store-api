from __future__ import annotations

from database import db

class StoreModel(db.Model):
    __tablename__ = 'stores'
    
    id = db.Column(db.Integer, primary_key=True, nullable= False)
    store_name = db.Column(db.String, nullable=False)
    store_address = db.Column(db.String)
    owner_id = db.Column(db.Integer,  db.ForeignKey('users.id'),
        nullable=False)
    created_at = db.Column(db.TIMESTAMP(timezone= True), nullable= False, server_default=db.text('now()'))
    owner = db.relationship('UserModel')
    # items = db.relationship('ItemModel')

        
    def to_json(self):
        return { 'id': self.id, 'storeName': self.store_name, 'owner_id': self.owner_id, 'items': [item.to_json() for item in self.items], 'item_count': self.count_items()}
        
    @classmethod
    def get_stores(cls, owner_id):
        return cls.query.filter_by(owner_id=owner_id).all()
    
    @classmethod
    def get_all_stores(cls):
        storeList = []
        result = cls.query.all()
        for store in result:
            storeList.append(store.to_json())
        return storeList
    
    
    def create_store(self):
        db.session.add(self)
        db.session.commit()
        
        return self
    
    @classmethod
    def get_by_name(cls, storeName):
        return cls.query.filter_by(store_name=storeName).first()
    
    def count_items(self):
        return len(self.items)
    
    @classmethod
    def find_by_id(cls, _id: int) -> StoreModel:
        return cls.query.filter_by(id=str(_id)).first()
    
    def update(self, **kwargs):
        for k,v in kwargs.items():
            self.__setattr__(k, v)
        db.session.commit()
        return self
        
    def remove_store(self):
        db.session.delete(self)
        db.session.commit()
        return "Record deleted!"
    
