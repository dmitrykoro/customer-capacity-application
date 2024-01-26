from typing import Tuple, Dict, Any
from flask_restful import Resource, fields, marshal_with


account_fields = {
    'account_id': fields.String,
    'name': fields.String,
    'role': fields.String,
    'username': fields.String,
    'password_hash': fields.String,
    'facility_id': fields.String,
    'session_key': fields.String,
    'session_expires_at': fields.DateTime
}


class AccountDao(object):
    def __init__(
            self,
            account_fields_dict: dict
    ) -> None:
        self.account_id = account_fields_dict['account_id']


class Account(Resource):
    """
    Create Account or get full Account info.
    """
    def __init__(
            self,
            dbapi
    ) -> None:
        self.dbapi = dbapi

    @marshal_with(account_fields)
    def get(
            self,
            account_id: str
    ) -> AccountDao:
        """
        Get full account info
        :param account_id: ID
        :return: json int the format:
            {'account_id': '123-456', ...}
        """
        return AccountDao(self.dbapi.account.get_one(account_id=account_id))

    def put(self) -> tuple[dict[str, Any], int]:  # TODO parse account fields from the request body
        """
        Create an empty account.
        :return: json with account ID
        """
        account_id = self.dbapi.account.create_one()
        return {'account_id': account_id}, 200
