from datetime import datetime
from flask_restful import Resource
from flask import request
import os
import boto3
from os import environ

client = boto3.resource('sqs', region_name='us-east-1',
                        aws_access_key_id=environ.get('AWS_ACCESS_KEY_ID'),
                        aws_secret_access_key=environ.get('AWS_SECRET_ACCESS_KEY'))

queue = client.get_queue_by_name(QueueName=environ.get('QUEUE_NAME'))


class VistaSignUp(Resource):

    def post(self):
        try:
            username = request.json['username']
            email = request.json['email']
            userpass = request.json['password']

            fecha = datetime.now()
            tfecha = fecha.strftime('%Y-%m-%d %H:%M:%S')

            try:
                # Send message to SQS queue
                response = queue.send_message(
                    DelaySeconds=10,
                    MessageAttributes={
                        'Title': {
                            'DataType': 'String',
                            'StringValue': 'New User'
                        },
                        'Date': {
                            'DataType': 'String',
                            'StringValue': str(tfecha)
                        },
                        'Username': {
                            'DataType': 'String',
                            'StringValue': str(username)
                        },
                        'Email': {
                            'DataType': 'String',
                            'StringValue': str(email)
                        },
                        'Password': {
                            'DataType': 'String',
                            'StringValue': str(userpass)
                        }
                    },
                    MessageBody=(
                        'New user created with username: ' + username +
                        ' and email: ' + email + ' at ' + str(tfecha) + ' .'
                    )
                )

                return ('Su solicitud de creación de usuario ha sido procesada: ' + response['MessageId'], 200)

            except Exception as e:
                return {'mensaje': str(e)}, 400

        except Exception as e:
            return {'mensaje': 'Por favor ingresar todos los campos', 'error': str(e)}, 400


class VistaPong(Resource):

    def get(self):
        return 'pong orchetartor', 200
