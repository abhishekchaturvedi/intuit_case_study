from flask import jsonify, request, current_app
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, current_user

from userlogin.api.v1 import V1FlaskView
from userlogin.blueprints.user.models import User
from userlogin.blueprints.user.schemas import (
    registration_schema,
    users_schema,
    user_schema,
    user_query_schema,
    user_update_schema
)


# XXX: Ideally, I should move this function to some lib/util module.
def match_current_user(username):
    """
    Utility function to match given name with current (logged in)
    user. Both username and email are matched.

    :param username: Username to match
    :return: True if matches the current logged in user.

    """
    if current_user is not None and \
       (current_user.username == username or \
        current_user.email == username):
        return True
    return False


class UsersView(V1FlaskView):
    def post(self):
        json_data = request.get_json()
        current_app.logger.debug('Got data: {0}'.format(json_data))
        if not json_data:
            response = jsonify({'error': 'Invalid input'})

            return response, 400

        try:
            data = registration_schema.load(json_data)
        except ValidationError as err:
            response = {
                'error': err.messages
            }

            return jsonify(response), 422

        user = User()
        user.email = data.get('email')
        user.username = data.get('username')
        user.password = User.encrypt_pass(data.get('password'))
        user.save()

        return jsonify(data), 200

    # The jwt required here ensures that only the user having the valid
    # token presented to them earlier will have access to this endpoint.
    # This is the functionality we get from the framework. Which would
    # mean that non-logged in users can't even get here. Rest of the
    # Permission checking logic should be in the endpoint.
    @jwt_required
    def get(self):
        json_data = request.get_json()
        current_app.logger.debug('Gotts data: {0}'.format(json_data))
        current_app.logger.debug('current user: {0}'.format(current_user.username))
        current_app.logger.debug('Request: {0}'.format(request))

        # Try to get the username from the request.
        try:
            username = request.args.get('username', default=None, type=str)
            current_app.logger.debug('Got username {0}'.format(username))
            if username is None:
                raise(AttributeError)
        except AttributeError as e:
            current_app.logger.debug('Failed to get username from request: {0}'.format(e))
            if json_data is not None:
                username = user_query_schema.load(json_data)['username']
                current_app.logger.debug('Got username {0}'.format(username))
            else:
                username = None
        except Exception as eall:
            current_app.logger.debug('Failed to load query schema: {0}'.format(eall))
            username = None

        current_app.logger.debug('Query for username {0}, current_user: {1}'
                                 ', admin: {2}'.format(
                                                    username,
                                                    current_user.username,
                                                    current_user.is_admin()))
        if username is not None and \
            (username == current_user.username or current_user.is_admin()):
            # Good request from current user self or admin for
            # a given user
            user = User.find_user(username)
            if user is not None:
                response = {'data': user_schema.dump(user)}
            else:
                response = {'error' : 'Failed to find user'}
        elif current_user.is_admin():
            ## Good request, give specific user or all users.
            users = User.query.all()
            response = {'data' : users_schema.dump(users)}
        else:
            response = {
                'error': 'Invalid request. Not authorized.'
            }

            return jsonify(response), 422

        return response, 200

    def delete(self):
        json_data = request.get_json()
        # Try to get the username from the request.
        try:
            current_app.logger.debug('Trying to get username from request: {0}'.format(request))
            username = request.args.get('username', default=None, type=str)
            current_app.logger.debug('Got username {0}'.format(username))
            if username is None:
                raise(AttributeError)
        except AttributeError as e:
            current_app.logger.debug('Failed to get username from request: {0}'.format(e))
            username = user_query_schema.load(json_data)['username']
            current_app.logger.debug('Got username {0}'.format(username))
        except Exception as eall:
            current_app.logger.debug('Failed to load query schema: {0}'.format(eall))
            username = None

        if username is not None:
            # Good request from current user self or admin for
            # a given user
            user = User.find_user(username)
            if user is not None and not user.is_admin():
                user.delete()
                response = {'message' : 'User deleted successfully'}
            else:
                return jsonify({'error' : 'failed to find user'}), 400
        else:
            return jsonify({'error' : 'Unsupported'}), 400

        return response, 200

    def patch(self):
        json_data = request.get_json()

        current_app.logger.debug('Got data: {0}'.format(json_data))
        current_app.logger.debug('type(current user): {0}'.format(type(current_user)))
        current_app.logger.debug('current user: {0}'.format(current_user))

        # Try to get the username from the request.
        try:
            current_app.logger.debug('Trying to get username from request: {0}'.format(request))
            username = request.args.get('username', default=None, type=str)
            current_app.logger.debug('Got username {0}'.format(username))
            if username is None:
                raise(AttributeError)
        except AttributeError as e:
            current_app.logger.debug('Failed to get username from request: {0}'.format(e))
            data = user_update_schema.load(json_data)
            username = data['username']
            new_username = data['new_username']
            current_app.logger.debug('Got username: {0}, new_username: {1}'.format(username, new_username))
        except Exception as eall:
            current_app.logger.debug('Failed to load query schema: {0}'.format(eall))
            username = None

        if username is not None:
            # Good request from current user self or admin for
            # a given user
            user = User.find_user(username)
            if user is not None:
                user.update_username(new_username)
                response = {'data': user_schema.dump(user)}
            else:
                response = {'error' : 'Failed to find user'}

        return response, 200
