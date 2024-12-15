from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_UI_URL = "/swagger"
SWAGGER_API_URL = "/spec"

swagger_ui_blueprint = get_swaggerui_blueprint(SWAGGER_UI_URL, SWAGGER_API_URL,)
