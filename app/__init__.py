from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint

from config import Config, Swagger

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
swagger_blueprint = get_swaggerui_blueprint(
    Swagger.SWAGGER_URL,
    Swagger.API_URL,
    config={'app_name': 'Case_1'}
)


def create_app(config_class=Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app.user import bp as user_bp
    from app.auth import bp as auth_bp
    from app.recruit import bp as req_bp
    app.register_blueprint(user_bp, url_prefix='/api/v1/user')
    app.register_blueprint(req_bp, url_prefix='/api/v1/recruit')
    app.register_blueprint(auth_bp, url_prefix='/api/v1')
    app.register_blueprint(swagger_blueprint, url_prefix=Swagger.SWAGGER_URL)

    return app


from app import models
