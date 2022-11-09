import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import stores

blp = Blueprint("stores", __name__, description="Operation on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(404, message= "Stores not found!")
    
    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted."}
        except KeyError:
            abort(404, message="Store not found")

@blp.route("/store")
class StoreList(MethodView):
    def get(self):
        return {'stores':list(stores.values())}
    
    def post(self):
        store_data = request.get_json()

        store_id = uuid.uuid4().hex

        new_store = {"id": store_id, **store_data}

        stores[store_id] = new_store

        return new_store, 201