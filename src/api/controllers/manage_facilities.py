from flask_restful import Resource, fields, marshal_with, reqparse, abort


facility_entry_fields = {
    'facility_id': fields.String,
    'income': fields.String,
    'name': fields.String,
    'occupancy': fields.String,
    'population': fields.String
}


class FacilityEntryDao(object):
    def __init__(
            self,
            facility_entry_fields: dict
    ) -> None:
        self.facility_id = facility_entry_fields['facility_id']
        self.income = facility_entry_fields['income']
        self.name = facility_entry_fields['name']
        self.occupancy = facility_entry_fields['occupancy']
        self.population = facility_entry_fields['population']


class ManageFacilities(Resource):
    def __init__(
            self,
            dbapi,
            auth_service
    ) -> None:
        self.dbapi = dbapi
        self.auth_service = auth_service

        self.parser = reqparse.RequestParser()

        self.parser.add_argument('account_id', type=str)
        self.parser.add_argument('session_key', type=str)
        self.parser.add_argument('facility_id', type=str)
        self.parser.add_argument('uuid_to_show', type=str)
        self.parser.add_argument('search_date', type=str)
        self.parser.add_argument('filter_by', type=str)
        self.parser.add_argument('filter_criteria', type=str)
        self.parser.add_argument('filter_amount', type=str)

    @marshal_with(facility_entry_fields)
    def put(self, action: str) -> list[FacilityEntryDao] or tuple:
        """
        Get filtered or unfiltered facilities.
        :param action: filter if get filtered list, full otherwise
        :return: list of dicts representing facilities
        """

        args = self.parser.parse_args()

        account_id = args['account_id']
        session_key = args['session_key']

        if not self.auth_service.check_session_key(account_id, session_key):
            return {'error': 'invalid-session-key'}, 401

        if action == 'filter':
            filter_by = args['filter_by']
            filter_criteria = args['filter_criteria']
            filter_amount = args['filter_amount']

            if not (filter_by and filter_criteria and filter_amount):
                return {'error': 'wrong-filter-params'}, 400

            matching_facilities_list = self.dbapi.customer_visit.get_filtered_facility_entries(
                filter_by=filter_by,
                filter_criteria=filter_criteria,
                filter_amount=filter_amount
            )

        if action == 'full':
            matching_facilities_list = self.dbapi.customer_visit.get_all_facilities_with_visits()

        return [
            FacilityEntryDao(
                facility_entry
            ) for facility_entry in matching_facilities_list
        ] if matching_facilities_list else None

    def post(self, action: str) -> tuple:
        """
        Delete a facility.
        """

        args = self.parser.parse_args()
        facility_id = args['facility_id']
        self.dbapi.facility.delete(facility_id=facility_id)

        return {'success': True}, 200
