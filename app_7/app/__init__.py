from flask import Flask, jsonify
import os

def test():
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'instance_1', 'my_database.db')
    return basedir

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    config_type = os.getenv("CONFIG_TYPE", default="app.config.Config")
    app.config.from_object(config_type)

    @app.route("/")
    def home():
        """
        Вітає користувача на головній сторінці
        ---
        tags:
            - домашня сторінка
        produces:
            - application/json
        responses:
            200:
                description: Привітання
                schema:
                    $ref: '#/definitions/Hello'
        """
        return jsonify(message="Привіт, я твій додаток для контролю витрат!")

    from app.swagger_utils import build_swagger
    from app.swagger_bp import swagger_ui_blueprint, SWAGGER_API_URL

    @app.route(SWAGGER_API_URL)
    def spec():
        return jsonify(build_swagger(app))

    from app.db import db
    from app.migrate import migrate
    from app.jwt import jwt

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    jwt.init_app(app)

    from app import expense
    from app import user

    app.register_blueprint(expense.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(swagger_ui_blueprint)

    @app.errorhandler(404)
    def handle_404(e):
        return str(e), 404

    return app
