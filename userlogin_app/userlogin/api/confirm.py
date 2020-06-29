from flask import jsonify, request, current_app
from flask_classful import FlaskView, route
from flask_jwt_extended import create_access_token, set_access_cookies
from marshmallow import ValidationError

from userlogin.blueprints.user.models import User
from userlogin.blueprints.user.schemas import confirm_schema

class ConfirmView(FlaskView):
    route_prefix = '/api/'

    def post(self):
        current_app.logger.debug(request)
        try:
            json_data = request.get_json(force=True)
        except Exception as e:
            current_app.logger.debug(e)
            raise(e)

        current_app.logger.debug("Got API call with json object {0}".format(json_data))
        try:
            if json_data is None:
                token = request.args.get('token', default=None, type=str)
            else:
                token = confirm_schema.load(json_data)['token']
        except ValidationError as e:
            response = {'error' : 'Invalid request'}
            return jsonify(response), 422

        current_app.logger.debug("Confirming token: {0}".format(token))

        # Let's find the user from the token.
        user = User.deserialize_token(token)
        if user is None:
            response = {'error' : 'Invalid token'}
            return jsonify(response), 422

        user.activate()
        current_app.logger.debug("Activating user {0}".format(user))
        return jsonify({'message' : 'Account activated successfully'}), 200
