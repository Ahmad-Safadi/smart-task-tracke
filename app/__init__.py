#__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.secret_key = 'YourSecretKey'
    db.init_app(app)

    from .routes import index_routes, home_routes, task_routes,edit
    app.register_blueprint(index_routes.bp)
    app.register_blueprint(home_routes.bp)
    app.register_blueprint(task_routes.bp)
    app.register_blueprint(edit.bp)
    return app
