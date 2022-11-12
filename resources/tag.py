from flask.views import MethodView

from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import TagModel, StoreModel, ItemModel

from schemas import TagSchema, ItemTagSchema

blp = Blueprint("Tags", "tags", description="Operation on tags")

@blp.route("/store/<int:store_id>/tag")
class TagInStore(MethodView):
    
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        
        return store.tags.all()
    
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        is_tag_exist_in_store_id = TagModel.query.filter(TagModel.store_id == store_id).first()
    
        if is_tag_exist_in_store_id:
            abort(400, "Tag already exist in that store id!")
        
        tag = TagModel(**tag_data, store_id = store_id)
        
        try: 
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))
        
        return tag
    

@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        
        return tag

@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkItemsToTags(MethodView):
    
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        
        item.tags.append(tag)
        
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=f"Error insert db: {e}")
        
        return tag

    @blp.response(200,ItemTagSchema)
    def delete(self,item_id,tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        
        item.tags.remove(tag)
        
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=f"Error insert db: {e}")
        
        return {"message": "Item removed from tag","item": item, "tag":tag}