from flask import Flask, jsonify
import os




def path_file():
    basedir = os.path.abspath(os.path.dirname(__file__))
    return basedir

def create_app():
    app = Flask(__name__, instance_relative_config=True, instance_path=f"{path_file()}/instance")
    app.config.from_mapping(SECRET_KEY="dev", SQLALCHEMY_DATABASE_URI="sqlite:///store.sqlite3")

    @app.route("/")
    def home():
        return jsonify(message="Привіт, я твій додаток для магазину!")

    from app.db import db
    from app.migrate import migrate

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)


    @app.errorhandler(404)
    def handle_404(e):
        return str(e), 404

    return app
