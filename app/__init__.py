import os
from flask import Flask
from .extensions import db, migrate

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Get absolute path for the instance folder
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, '..', 'instance', 'students.db')

    # Flask configuration
    app.config.from_mapping(
        SECRET_KEY="devkey",
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{db_path}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register routes
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
