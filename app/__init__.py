from flask import Flask
from .extensions import db, migrate

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    # simple config - change DB path as needed
    app.config.from_mapping(
        SECRET_KEY="devkey",
        SQLALCHEMY_DATABASE_URI="sqlite:///instance/students.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # register blueprints
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
