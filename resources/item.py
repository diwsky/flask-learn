import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel

from schemas import ItemUpdateSchema, ItemSchema

blp = Blueprint("Items", __name__, description="Operation on Items")

@blp.route("/item/<string:item_id>")
class Item(MethodView):
    
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        
        return item
    
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        
        raise NotImplementedError("Delete not yet implemented")
    
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)
        
        db.session.add(item)
        db.session.commit()
        
        return item


@blp.route("/item")
class ItemList(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        item = ItemModel.query.get_or_404()
        
        raise NotImplementedError("Delete not yet implemented")
    
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):

        item = ItemModel(**item_data)
        
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="There's error when saving DB!")

        return item