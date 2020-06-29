from flask import jsonify, request, current_app
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, current_user
from flask_jwt_extended import create_access_token, set_access_cookies

from userlogin.api.v1 import V1FlaskView
from userlogin.blueprints.user.models import User
from userlogin.blueprints.user.schemas import (
    registration_schema,
    users_schema,
    user_schema,
    user_query_schema,
    user_update_schema,
    user_schema_detailed,
    users_schema_detailed
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
            current_app.logger.debug(type(data))
            current_app.logger.debug(data)
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
        activate_token = User.initiate_activation(user)
        data.update({'message' : "Please check your email for activating the account"})
        data.update({'token' : activate_token})
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
        username = None
        try:
            data = user_query_schema.load(json_data)
            username = data['username']
            detailed = data['detailed']
            current_app.logger.debug('fetching {0} info for {1}'.\
                                     format('detailed' if detailed else 'short',
                                            username))
        except Exception as eall:
            current_app.logger.debug('Failed to load query schema: {0}'.format(eall))
            return jsonify({'error' : 'Malformed requet'}), 400

        current_app.logger.debug('Query for username {0}, current_user: {1}'
                                 ', admin: {2}'.format(
                                                    username,
                                                    current_user.username,
                                                    current_user.is_admin()))
        if username is not None and username != 'all' and \
            (username == current_user.username or current_user.is_admin()):
            # Good request from current user self or admin for
            # a given user
            user = User.find_user(username)
            if user is not None:
                current_app.logger.debug('User: {0}'.format(user))
                if user.active:
                    if detailed:
                        response = {'data': user_schema_detailed.dump(user)}
                    else:
                        response = {'data': user_schema.dump(user)}
                else:
                    response = {'error' :
                                'user is not active. acticate with /auth/activate <email>'}
            else:
                response = {'error' : 'Failed to find user'}
        elif current_user.is_admin():
            ## Good request, give specific user or all users.
            users = User.query.all()
            if detailed:
                response = {'data' : users_schema_detailed.dump(users)}
            else:
                response = {'data' : users_schema.dump(users)}
        else:
            response = {
                'error': 'Invalid request. Not authorized.'
            }

            return jsonify(response), 401

        return response, 200

    # The jwt required here ensures that only the user having the valid
    # token presented to them earlier will have access to this endpoint.
    # This is the functionality we get from the framework. Which would
    # mean that non-logged in users can't even get here. Rest of the
    # Permission checking logic should be in the endpoint.
    @jwt_required
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

        if username is not None and \
           (match_current_user(username) or current_user.is_admin()):
            # Good request from current user self or admin for
            # a given user
            user = User.find_user(username)
            # Won't let admins account be deleted (this should be fixed
            # further. It's not like we don't want to delete admins role
            # but we just don't want the last admin to be deleted in most
            # cases. Otherwise admin deletion should actually be OK.)
            if user is not None and not user.is_admin():
                user.delete()
                return jsonify({'message' : 'User deleted successfully'}), 200
            else:
                return jsonify({'error' : 'failed to find user'}), 404
        else:
            return jsonify({'error' : 'All user delete not supported'}), 400

    # The jwt required here ensures that only the user having the valid
    # token presented to them earlier will have access to this endpoint.
    # This is the functionality we get from the framework. Which would
    # mean that non-logged in users can't even get here. Rest of the
    # Permission checking logic should be in the endpoint.
    @jwt_required
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

        if username is not None and match_current_user(username):
            # Good request from current user self or admin for
            # a given user
            user = User.find_user(username)
            if user is not None:
                user.update_username(new_username)
                current_app.logger.debug('Updated successfully! {0}'.format(user))
                return jsonify({'data': user_schema.dump(user)}), 200
            else:
                return jsonify({'error' : 'failed to find user'}), 404
        else:
            return jsonify({'error' : 'All user delete not supported'}), 400
