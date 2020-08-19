#define blueprint here

from flask import Blueprint
from flask_restful import Api
from .resources import Details

#define blueprint
api_bp = Blueprint('api',__name__)

api = Api(api_bp)

#resource routing
api.add_resource(Details,'/v1/details')

