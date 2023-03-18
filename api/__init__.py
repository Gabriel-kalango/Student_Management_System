from flask import Flask,jsonify
from flask_migrate import Migrate
from .utils.utils import db
from .config.config import config_dict
from flask_jwt_extended import JWTManager
from flask_restx import Api
from .student import student_namespace,reg_course_namespace
from .admin import admin_namespace
from .course import course_namespace
from .model import Admin,BlockliskModel



def create_app(config=config_dict["dev"]):
    app=Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    migrate=Migrate(app,db)
    jwt=JWTManager(app)
    api=Api(app)
    api.add_namespace(student_namespace)
    api.add_namespace(admin_namespace)
    api.add_namespace(course_namespace)
    api.add_namespace(reg_course_namespace)
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return  BlockliskModel.query.filter_by(jwt=jwt_payload["jti"] ).first()

 
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    @jwt.additional_claims_loader
    def add_additional_claims(identity):
        admin=Admin.query.filter(Admin.email==identity).first()
        if admin:
            return {"is_admin":True}
        {"is_admin":False}
        
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
        jsonify({"message": "The token has expired.", "error": "token_expired"}),
        401,
    )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )
    return app