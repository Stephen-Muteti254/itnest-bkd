from flask import Flask, jsonify
from .config import DevelopmentConfig, ProductionConfig
from .extensions import db, jwt, cors, bcrypt
import os
from flask_cors import CORS
import os
from app.config import Config
import re

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def create_app(config_name=None):
    app = Flask(
        __name__,
        instance_relative_config=False,
        template_folder=os.path.join(BASE_DIR, "templates")
    )

    env = os.getenv("FLASK_ENV", "development")
    if env == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    # -----------------------------
    # JWT Debug Callbacks
    # -----------------------------

    @jwt.invalid_token_loader
    def invalid_token(reason):
        print("INVALID TOKEN:", reason)
        return jsonify(msg=reason), 401

    @jwt.unauthorized_loader
    def missing_token(reason):
        print("UNAUTHORIZED:", reason)
        return jsonify(msg=reason), 401

    @jwt.revoked_token_loader
    def revoked(jwt_header, jwt_payload):
        print("REVOKED")
        return jsonify(msg="revoked"), 401

    @jwt.expired_token_loader
    def expired(jwt_header, jwt_payload):
        print("EXPIRED")
        return jsonify(msg="expired"), 401


    # parse env list for dev (localhost) and prod
    origins = [o.strip() for o in app.config["CORS_ORIGINS"].split(",")]

    origins.extend([
        "https://itnest.org",
    ])

    # Subdomains (regex)
    origins.append(re.compile(r"https://.*\.itnest\.org"))

    CORS(
        app,
        resources={r"/api/*": {"origins": origins}},
        supports_credentials=True,
        allow_headers=[
            "Content-Type",
            "Authorization",
        ],
        methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    )

    bcrypt.init_app(app)
    # limiter.init_app(app)

    # register blueprints
    from app.routes.career_routes import bp as career_bp
    from app.routes.assessment_routes import bp as assessment_bp

    app.register_blueprint(career_bp)
    app.register_blueprint(assessment_bp)

    # error handlers to match required error format
    from app.utils.response_formatter import error_response

    @app.errorhandler(400)
    def bad_request(e):
        return error_response("BAD_REQUEST", str(e), status=400)

    @app.errorhandler(401)
    def unauthorized(e):
        return error_response("UNAUTHORIZED", str(e), status=401)

    @app.errorhandler(404)
    def not_found(e):
        return error_response("NOT_FOUND", "Resource not found", status=404)

    @app.errorhandler(500)
    def server_error(e):
        return error_response("SERVER_ERROR", "Internal server error", status=500)

    return app
