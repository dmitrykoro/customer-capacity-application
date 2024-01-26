from typing import Tuple, Dict, Any
from flask_restful import Resource, fields, marshal_with, reqparse


class Login(Resource):
    def __init__(
            self,
            dbapi,
            auth_service
    ):
        self.auth_service = auth_service
        self.parser = reqparse.RequestParser()

        self.parser.add_argument('username', type=str)
        self.parser.add_argument('password', type=str)

    def post(self):
        args = self.parser.parse_args()

        provided_username = args['username']
        provided_password = args['password']

        authorization_response = self.auth_service.try_to_authorize(
            username=provided_username,
            password=provided_password
        )

        if 'error' in authorization_response.keys():
            return {'error': authorization_response.get('error')}, 401

        return {
            'account_id': authorization_response['account_id'],
            'name': authorization_response['name'],
            'role': authorization_response['role'],
            'facility_id': authorization_response['facility_id'],
            'session_key': authorization_response['session_key'],
            'session_expires_at': authorization_response['session_expires_at'].isoformat()
        }, 200
