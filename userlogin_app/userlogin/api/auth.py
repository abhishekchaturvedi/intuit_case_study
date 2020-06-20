from flask import jsonify, request, current_app
from flask_classful import FlaskView, route

class AuthView(FlaskView):
    route_prefix = '/api/'

    def post(self):
        json_data = request.get_json()
        current_app.logger.debug("Got API call with json object {0}".format(json_data))
        response = jsonify({
            'data': {}
        })
        return response, 200
