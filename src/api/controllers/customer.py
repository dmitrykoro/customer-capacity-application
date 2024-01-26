from flask_restful import Resource, reqparse, abort

from api.services.customer_service import CustomerService


class Customer(Resource):
    def __init__(
            self,
            dbapi,
            auth_service
    ):
        self.customer_service = CustomerService(dbapi)
        self.auth_service = auth_service

        self.parser = reqparse.RequestParser()

        self.parser.add_argument('account_id', type=str)
        self.parser.add_argument('session_key', type=str)
        self.parser.add_argument('facility_id', type=str)
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('document_id', type=str)
        self.parser.add_argument('age', type=int)
        self.parser.add_argument('charge', type=float)

    def post(self, action: str):
        args = self.parser.parse_args()

        account_id = args['account_id']
        session_key = args['session_key']
        facility_id = args['facility_id']
        name = args['name']
        document_id = args['document_id']
        age = args['age']

        if not self.auth_service.check_session_key(account_id, session_key):
            return {'error': 'invalid-session-key'}, 401

        if action == 'checkin':
            can_be_checked_in = self.customer_service.ensure_can_be_checked_in(document_id, facility_id)

            if 'error' in can_be_checked_in:
                return {'error': can_be_checked_in['error']}, 400

            check_in_result = self.customer_service.do_check_in(facility_id, name, document_id, age)
            if 'error' in check_in_result:
                return {'error': check_in_result['error']}, 500

            return {'success': 'true'}, 200

        if action == 'checkout':
            can_be_checked_out = self.customer_service.ensure_can_be_checked_out(document_id)

            if 'error' in can_be_checked_out:
                return {'error': can_be_checked_out['error']}, 400

            check_out_result = self.customer_service.do_check_out(
                document_id=document_id, charge=args['charge']
            )
            if 'error' in check_out_result:
                return {'error': check_out_result['error']}, 500

            return {'success': 'true'}, 200

        else:
            abort(404)
