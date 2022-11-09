import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items

blp = Blueprint("Items", __name__, description="Operation on Items")

@blp.route("/item/<string:store_id>")
class Item(MethodView):
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message= "Stores not found!")
    
    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted."}
        except KeyError:
            abort(404, message="Item not found")
    
    def put(self, item_id):
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


@blp.route("/item")
class ItemList(MethodView):
    def get(self):
        return {"items": list(items.values())}
    
    def post(self):
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

        item_id = uuid.uuid4().hex

        new_item = {**item_data, "id": item_id}

        items[item_id] = new_item

        return new_item, 201