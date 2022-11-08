from flask import Flask, request
from db import stores, items
from flask_smorest import abort
import uuid

app = Flask(__name__)

## stores

@app.get('/stores')
def get_stores():
    return {'stores':stores}

@app.post('/store')
def post_store():
    store_data = request.get_json()

    store_id = uuid.uuid4().hex

    new_store = {"id": store_id, **store_data}

    stores[store_id] = new_store

    return new_store, 201

@app.get('/store/<string:store_id>/')
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(404, message= "Stores not found!")
        
@app.delete('/store/<string:store_id>')
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message": "Store deleted."}
    except KeyError:
        abort(404, message="Store not found")
## items

@app.post('/item')
def create_item():
    item_data = request.get_json()
    
    if (
        "price" not in item_data or
        "store_id" not in item_data or
        "name" not in item_data
    ):
        abort(400, message="Bad request! Make sure the content is right!")
    
    for item in items.values():
        if (
            item_data["name"] == item["name"] and
            item_data["store_id"] == item["store_id"]
        ):
            abort(400, message=f"Item already exists!")
    
    if item_data["store_id"] not in stores:
        abort(404, message= "Stores not found!")
    
    item_id = uuid.uuid4().hex
    
    new_item = {**item_data, "id": item_id}
    
    items[item_id] = new_item
    
    return new_item, 201

@app.put('/item/<string:item_id>')
def update_item(item_id):
    
    item_data = request.get_json()
    
    if (
        "price" not in item_data or "name" not in item_data
    ):
        abort(400, message=f"Bad vibes, data not completed!")
        
    try:
        item = items[item_id]
        
        item |= item_data
        return item
    except KeyError:
        abort(404, message=f"Item not found!!")

@app.delete('/item/<string:item_id>')
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message": "Item deleted."}
    except KeyError:
        abort(404, message="Item not found")


@app.get('/item')
def get_all_item():
    return {"items": list(items.values())}

@app.get('/item/<string:item_id>')
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(404, message= "Stores not found!")