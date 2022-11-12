import os
import secrets

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from db import db

from models import BlocklistModel

from resources.item import blp as itembp
from resources.store import blp as storebp
from resources.tag import blp as tagbp
from resources.user import blp as userbp

def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui/"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL","sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
    
    db.init_app(app)
    
    api = Api(app)
    
    app.config["JWT_SECRET_KEY"] = "252521098153987410488268509302296153434"
    jwt = JWTManager(app)
    
    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({
                "message": "Token has expired.",
                "error": "token_expired"
            }),
            401
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify({
                "message": f"Signature verification failed. {error}",
                "error": "invalid_token"
            }),
            401
        )
    
    @jwt.unauthorized_loader
    def unatuhorized_loader(error):
        return (
            jsonify({
                "message": f"Request does not contain an access token. {error}",
                "error": "authorization_required"
            }),
            401
        )
    
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        token = jwt_payload["jti"]
        
        return BlocklistModel.query.filter(token == BlocklistModel.revoked_token).first()
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )
    
    with app.app_context():
        db.create_all()

    api.register_blueprint(itembp)
    api.register_blueprint(storebp)
    api.register_blueprint(tagbp)
    api.register_blueprint(userbp)
    
    return app