from flask import url_for, current_app, jsonify


class TestPage(object):
    def test_login_page(self, client):
        """ Home page should respond with a success 200. """
        response = client.get(url_for('user.login'))
        current_app.logger.debug("Testing login page")
        assert response.status_code == 200

    def test_login(self, client):
        """ Attempt login of a user"""
        input = {'username' : 'Abhishek',
                 'password' : 'foobar'}
        data = jsonify(input)
        response = client.post(url_for('AuthView:post'), data=data)
        current_app.logger('Got response {0}'.format(response))
        assert response.status_code == 200
