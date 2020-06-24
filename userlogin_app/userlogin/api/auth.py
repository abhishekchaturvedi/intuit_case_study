from flask import jsonify, request, current_app
from flask_classful import FlaskView, route
from flask_jwt_extended import create_access_token, set_access_cookies
from marshmallow import ValidationError

from userlogin.blueprints.user.models import User
from userlogin.blueprints.user.schemas import auth_schema

class AuthView(FlaskView):
    route_prefix = '/api/'

    def post(self):
        current_app.logger.debug(request)

        try:
            json_data = request.get_json(force=True)
        except Exception as e:
            current_app.logger.debug(e)
            raise(e)

        current_app.logger.debug("Got API call with json object {0}".format(json_data))

        # Let's check for valid intput.
        if not json_data:
            current_app.logger.debug("json data is empty")
            response = {
                'error': 'Invalid input'
            }

            return jsonify(response), 400

        # Input is valid, let's try to load the data
        current_app.logger.debug("Loading data from schema")
        try:
            data = auth_schema.load(json_data)
        except ValidationError as err:
            response = {
                'error': err.messages
            }

            return jsonify(response), 422

        # Loading data into the schema is fine, let's find the user.
        user = User.find_user(data['username'])

        # User is valid and password is correct. Create access token
        # for the session and respond OK. Else return error.
        if user and user.authenticated(password=data['password']):
            access_token = create_access_token(identity=user.username)

            response = jsonify({
                'data': {
                    'access_token': access_token
                }
            })

            # Set the JWTs and the CSRF double submit protection cookies.
            set_access_cookies(response, access_token)
            current_app.logger.debug('User {0}({1}) logged in successfully!'.format(data['username'], user))
            return response, 200
        else:
            response = jsonify({
                'error': {
                    'message': 'Invalid identity or password'
                }
            })
            return response, 401
