from flask import Flask, jsonify
from flask_restful import Api
from dotenv import load_dotenv
from flask_cors import CORS

# 추가!
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from marshmallow import ValidationError

# 추가!
from .db import db
from .ma import ma
from .models import user, post, comment
from .resources.post import PostList, Post
from .resources.user import UserRegister


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"*": {"origins": "*"}})
    load_dotenv(".env", verbose=True)
    app.config.from_object("config.dev")
    app.config.from_envvar("APPLICATION_SETTINGS")
    app.config.update(RESTFUL_JSON=dict(ensure_ascii=False))
    api = Api(app)

    # 추가!
    jwt = JWTManager(app)
    migrate = Migrate(app, db)

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    # 추가!
    @app.before_first_request
    def create_tables():
        db.create_all()

    # 추가!
    @app.errorhandler(ValidationError)
    def handle_marshmallow_validation(err):
        return jsonify(err.messages), 400

    api.add_resource(PostList, "/posts/")
    api.add_resource(Post, "/posts/<int:id>")
    api.add_resource(UserRegister, "/register/")

    return app
