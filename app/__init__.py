from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from app.database import db


def create_app(config):
    _app = Flask(__name__)
    _app.config.from_object(config)
    _app.secret_key = config.secret_key
    CORS(_app, resources={r"/apply": {"origins": "*"}})

    from app.views.library import library
    from app.views.admin import admin
    from app.views.verify import verify
    _app.register_blueprint(library, url_prefix="/library")
    _app.register_blueprint(admin, url_prefix="/admin")
    _app.register_blueprint(verify, url_prefix="/verify")

    from app.v1.controllers.libraries import libraries_api
    from app.v1.controllers.maps import maps_api
    from app.v1.controllers.users import users_api
    from app.v1.controllers.admin import admin_api
    from app.v1.controllers.signin import signin_api

    _app.register_blueprint(libraries_api, url_prefix='/api/v1/library')
    _app.register_blueprint(maps_api, url_prefix='/api/v1/map')
    _app.register_blueprint(users_api, url_prefix='/api/v1/user')
    _app.register_blueprint(admin_api, url_prefix="/api/v1/admin")
    _app.register_blueprint(signin_api, url_prefix='/api/v1/signin')

    db.init_app(_app)
    Migrate(_app, db)

    return _app
