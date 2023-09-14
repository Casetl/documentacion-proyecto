from flask_restful import Resource
from flask import request
import requests
import os
from datetime import timedelta
from datetime import datetime
from os import environ

path_user = os.getenv('USERS_PATH', 'localhost:3000') if environ.get(
    'USERS_PATH') != 'default' else 'localhost:3000'


class VistaSignUp(Resource):

    def post(self):
        try:
            username = request.json['username']
            email = request.json['email']
            userpass = request.json['password']

            newUser = {
                "username": username,
                "email": email,
                "password": userpass
            }

            try:
                response = requests.post(
                    f'http://{path_user}/users/signup', json=newUser)
                return response.json(), response.status_code

            except Exception as e:
                return {'mensaje': str(e)}, 400

        except Exception as e:
            return {'mensaje': 'Por favor ingresar todos los campos', 'error': str(e)}, 400
