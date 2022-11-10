import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from schemas import StoreSchema

from db import db
from models import StoreModel

blp = Blueprint("stores", __name__, description="Operation on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    
    @blp.arguments(StoreSchema)
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store
    
    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted."}
        except KeyError:
            abort(404, message="Store not found")

@blp.route("/store")
class StoreList(MethodView):
    
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return stores.values()
    
    @blp.arguments(StoreSchema)
    @blp.response(201,StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Store already exists!")
        except SQLAlchemyError:
            abort(500, message="Error occured when creating store!")
        
        return store