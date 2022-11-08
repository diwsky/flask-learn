from flask import Flask, request
from db import stores, items
import uuid

app = Flask(__name__)



@app.get('/stores')
def get_stores():
    return {'stores':stores}

@app.post('/store')
def post_store():
    request_json = request.get_json()
    new_stores = {
        "name": request_json["name"],
        "items": request_json["items"]
    }
    stores.append(new_stores)

    return stores, 201

@app.post('/store/<string:store_id>/items')
def create_item(store_id):
    request_json = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {"name": request_json["name"], "price": request_json["price"]}
            store["items"].append(new_item)
            return new_item, 201
    return {"message": "Store not found!"}, 404

@app.get('/store/<string:name>/')
def get_store(name):
    for store in stores:
        if name == store["name"]:
            return store, 200
    return {"message": "Store not found"}, 404

@app.get('/store/<string:name>/items')
def get_store_item(name):
    for store in stores:
        if name == store["name"]:
            return store["items"], 200
    return {"message": "Store not found!"}