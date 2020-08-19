from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()



def create_app():
    app = Flask(__name__)

    # load app configs
    app.config.from_object('config.Config')

    #initialize sqlalchemy
    mongo.init_app(app)

    with app.app_context():
        # import and register blueprint here.
        from .api import api_bp
        app.register_blueprint(api_bp)


    return app
