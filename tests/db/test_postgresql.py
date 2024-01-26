import datetime
import hashlib
import unittest
import uuid

from tests.test_utils import *

from src.dbapi.capacity_database_api import CapacityDatabaseAPI


class TestPostgreSQL(unittest.TestCase):

    def test_can_connect(self):
        version = get_rest_call(self, 'http://127.0.0.1:4999/manage/version')
        self.assertTrue(version[0].startswith('PostgreSQL'))

    def test_create_account(self) -> None:
        """
        Verify creation of an account.
        :return: None
        """

        dbapi = CapacityDatabaseAPI()

        account_id = dbapi.account.create_one()
        created_account_id = dbapi.account.get_one(account_id=account_id)['account_id']

        self.assertEqual(account_id, created_account_id)

    def test_fetch_account(self) -> None:
        """
        Verify fetching of account info
        :return: None
        """

        dbapi = CapacityDatabaseAPI(reinitialize_schema=True)
        facility_uuid = dbapi.db_utils.get_all_rows(table_name='facility')[0][0]

        db_uuid = str(uuid.uuid4())
        name = 'Alex'
        role = 'bouncer'
        username = 'alex2000'
        password = "alex"
        password_hash = hashlib.sha512(password.encode('utf-8')).hexdigest()
        session_key = uuid.uuid4()
        timestamp = datetime.datetime.now()

        # manually insert account data
        sql = f'''
            INSERT INTO account(
                uuid, name, role, username, password_hash, facility_id, session_key, session_expires_at
            ) 
            VALUES (
                '{db_uuid}', '{name}', '{role}', '{username}', '{password_hash}', '{facility_uuid}', '{session_key}', '{timestamp}'
            );
        '''

        dbapi.db_utils.exec_commit(sql)

        # verify insertion
        actual_account_data = dbapi.account.get_one(account_id=db_uuid)

        self.assertEqual(password_hash, actual_account_data['password_hash'])
        self.assertEqual(timestamp, actual_account_data['session_expires_at'])
