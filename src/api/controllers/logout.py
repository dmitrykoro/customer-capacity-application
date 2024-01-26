from flask_restful import Resource, fields, marshal_with, reqparse


class Logout(Resource):
    def __init__(
            self,
            dbapi,
            auth_service
    ):
        self.auth_service = auth_service
        self.parser = reqparse.RequestParser()

        self.parser.add_argument('session_key', type=str)
        self.parser.add_argument('account_id', type=str)

    def post(self):
        """
        Reset the session key for the account.
        :return:
        """
        args = self.parser.parse_args()

        provided_session_key = args['session_key']
        provided_account_id = args['account_id']

        if not self.auth_service.check_session_key(provided_account_id, provided_session_key):
            return {'error': 'invalid-session-key'}, 401

        self.auth_service.log_out(account_id=provided_account_id)
        return {'success': True}, 200
