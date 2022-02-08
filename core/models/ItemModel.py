from __future__ import annotations
from database import db
from sqlalchemy.sql import expression


class ItemModel(db.Model):
    __tablename__ = 'items'
    
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String, nullable=False)
    item_price = db.Column(db.Float(precision=2), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    on_discount = db.Column(db.Boolean, nullable=False, server_default=expression.false() )
    item_stock = db.Column(db.Integer, nullable=False, server_default='1')
    # store = db.relationship('StoreModel')

    def to_json(self):
        return { 'id': self.id, 'item_name': self.item_name, 'item_price': self.item_price, 'store_id': self.store_id, 'on_discount': self.on_discount, 'item_stock': self.item_stock}
    
    @classmethod
    def find_by_id(cls, id) ->ItemModel:
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def get_item_by_name_and_price(cls, store_id, item_name, item_price) -> ItemModel:
        return cls.query.filter_by(store_id=store_id, item_name=item_name, item_price=str(item_price)).first()
    
    @classmethod
    def get_all_items(cls):
        return list(item.to_json() for item in cls.query.all())
    
    def add_item(self):
        result = self.get_item_by_name_and_price(self.store_id,self.item_name,self.item_price)
            
        if result and result.item_price == self.item_price:
            self = result
            self.item_stock =self.item_stock + 1
        else:
            db.session.add(self)
        
        db.session.commit()
        
        return self
    
    def remove_item(self):
        db.session.delete(self)
        db.session.commit()
        return "Record deleted!"
    
    def update(self, **kwargs):
        for k,v in kwargs.items():
            self.__setattr__(k, v)
        db.session.commit()
        return self
    
    @classmethod
    def get_items_from_store(cls,_store_id) :
        return cls.query.filter_by(store_id=_store_id).all()