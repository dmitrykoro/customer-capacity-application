from typing import Tuple, Dict, Any
from flask_restful import Resource, fields, marshal_with, reqparse


class Facility(Resource):
    def __init__(
            self,
            dbapi,
            auth_service
    ) -> None:
        self.dbapi = dbapi

        self.auth_service = auth_service

        self.parser = reqparse.RequestParser()

        self.parser.add_argument('session_key', type=str)
        self.parser.add_argument('account_id', type=str)
        self.parser.add_argument('facility_id', type=str)
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('city', type=str)
        self.parser.add_argument('max_capacity', type=int)
        self.parser.add_argument('notes', type=str)

    def post(self) -> tuple[dict[str, Any], int]:
        """
        Crete a new facility
        :return: json with facility ID or error
        """
        args = self.parser.parse_args()

        session_key = args['session_key']
        account_id = args['account_id']

        if not self.auth_service.check_session_key(account_id, session_key):
            return {'error': 'invalid-session-key'}, 401

        name = args['name']
        city = args['city']

        if self.dbapi.facility.exists(name, city):
            return {'error': 'facility-exists'}, 400

        max_capacity = args['max_capacity']
        notes = args['notes']

        facility_id = self.dbapi.facility.create_one(
            name=name,
            city=city,
            max_capacity=max_capacity,
            notes=notes
        )

        return {'facility_id': facility_id}, 200

    def put(self) -> tuple[dict[str, Any], int]:
        """
        Update a facility info
        :return: json with facility ID or error
        """

        args = self.parser.parse_args()

        session_key = args['session_key']
        account_id = args['account_id']

        if not self.auth_service.check_session_key(account_id, session_key):
            return {'error': 'invalid-session-key'}, 401

        update_facility_id = args['facility_id']
        new_max_capacity = args['max_capacity']
        new_notes = args['notes']

        facility_dict = self.dbapi.facility._update_one(  # noqa
            facility_id=update_facility_id,
            max_capacity=new_max_capacity,
            notes=new_notes
        )

        return {'facility_id': facility_dict['facility_id']}, 200
