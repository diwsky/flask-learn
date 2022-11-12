from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt

from db import db
from models import UserModel, BlocklistModel
from schemas import UserSchema

blp = Blueprint("Users", "users", description="Operations on users")

@blp.route("/register")
class UserRegister(MethodView):
    
    @blp.arguments(UserSchema)
    def post(self,user_data):
        
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="User already exists!")
        
        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"]))
        
        try:    
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Error on adding user")
        
        return {"message":f"User created."}
    

@blp.route("/user/<int:user_id>")
class TestUser(MethodView):
    
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        
        return user
    
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        
        db.session.delete(user)
        db.session.commit()
        
        return {"message": f"User deleted: {user}"}
    
@blp.route("/login")
class Login(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()
        
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token}
        
        abort(401, message="Invalid credentials.")

@blp.route("/logout")
class Logout(MethodView):
    
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        
        blocklist = BlocklistModel(revoked_token=jti)
        
        db.session.add(blocklist)
        db.session.commit()
        
        return {"message": "Successfully logged out!"}, 200