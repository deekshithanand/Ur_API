from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager

mongo = PyMongo()
lm = LoginManager()


def create_app():
    app = Flask(__name__)

    # load app configs
    app.config.from_object('config.Config')

    #initialize sqlalchemy
    mongo.init_app(app)
    lm.init_app(app)
   

    with app.app_context():
        # import and register blueprint here.
        from .api import api_bp
        app.register_blueprint(api_bp)

        from .user_manager import user_manager_bp
        app.register_blueprint(user_manager_bp)



    return app
