from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes.menu import menu_bp
    from app.routes.admin import admin_bp
    from app.routes.kitchen import kitchen_bp

    app.register_blueprint(menu_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(kitchen_bp, url_prefix='/kitchen')

    return app
