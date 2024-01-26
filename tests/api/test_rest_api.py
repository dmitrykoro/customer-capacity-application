import unittest

from tests.test_utils import *

from src.dbapi.capacity_database_api import CapacityDatabaseAPI

DOMAIN = 'http://127.0.0.1:4999'


class TestExample(unittest.TestCase):

    def setUp(self):
        """Initialize DB using API call"""
        post_rest_call(self, f'{DOMAIN}/manage/init')

    def test_init_schema(self):
        post_rest_call(self, f'{DOMAIN}/manage/init')

    def test_login_success(self):
        """Test login API"""

        dbapi = CapacityDatabaseAPI(install_accounts=True)

        account_fields = requests.post(
            url=f'{DOMAIN}/login',
            json={'username': 'a', 'password': 'p'}
        ).json()

        self.assertTrue(account_fields['session_expires_at'])

    def test_login_failure(self):
        """Test login failure"""

        dbapi = CapacityDatabaseAPI(install_accounts=True)

        response = requests.post(
            url=f'{DOMAIN}/login',
            json={'username': 'a', 'password': 'pa'}
        ).json()

        self.assertEqual(response['error'], 'wrong-password')

        response = requests.post(
            url=f'{DOMAIN}/login',
            json={'username': 'aa', 'password': 'pa'}
        ).json()

        self.assertEqual(response['error'], 'account-not-found')

    def test_checkin_customer(self):
        """Test registering of a customer in a facility"""

        dbapi = CapacityDatabaseAPI(install_accounts=True)

        login_response = requests.post(
            url=f'{DOMAIN}/login',
            json={'username': 'b', 'password': 'p'}
        ).json()

        checkin_response = requests.post(
            url=f'{DOMAIN}/customer/checkin',
            json={
                'account_id': login_response['account_id'],
                'session_key': login_response['session_key'],
                'facility_id': login_response['facility_id'],
                'name': 'Dima',
                'document_id': '3',
                'age': '25'
            }
        ).json()

        self.assertTrue(checkin_response['success'])

    def test_checkout_customer(self):
        """Test checking out of a customer after checking-in"""

        dbapi = CapacityDatabaseAPI(install_accounts=True)

        login_response = requests.post(
            url=f'{DOMAIN}/login',
            json={'username': 'b', 'password': 'p'}
        ).json()

        # checkin
        requests.post(
            url=f'{DOMAIN}/customer/checkin',
            json={
                'account_id': login_response['account_id'],
                'session_key': login_response['session_key'],
                'facility_id': login_response['facility_id'],
                'name': 'Dima',
                'document_id': '3',
                'age': '25'
            }
        ).json()

        # checkout
        checkout_response = requests.post(
            url=f'{DOMAIN}/customer/checkout',
            json={
                'account_id': login_response['account_id'],
                'session_key': login_response['session_key'],
                'facility_id': login_response['facility_id'],
                'document_id': '3',
                'charge': '10'
            }
        ).json()

        self.assertTrue(checkout_response['success'])

    def test_checkin_errors(self):
        """Test checkin additional cases"""

        dbapi = CapacityDatabaseAPI(install_accounts=True)

        login_response = requests.post(
            url=f'{DOMAIN}/login',
            json={'username': 'a', 'password': 'p'}
        ).json()

        # checkin
        checkin_response = requests.post(
            url=f'{DOMAIN}/customer/checkin',
            json={
                'account_id': login_response['account_id'],
                'session_key': '123',
                'facility_id': login_response['facility_id'],
                'name': 'Dima',
                'document_id': '3',
                'age': '25'
            }
        ).json()

        self.assertTrue(checkin_response['error'])

    def test_register_facility(self):
        """Test a facility registration API"""

        dbapi = CapacityDatabaseAPI(install_accounts=True)

        login_response = requests.post(
            url=f'{DOMAIN}/login',
            json={'username': 'a', 'password': 'p'}
        ).json()

        # register a facility
        register_response = requests.post(
            url=f'{DOMAIN}/facility',
            json={
                'account_id': login_response['account_id'],
                'session_key': login_response['session_key'],
                'name': 'DMV1',
                'city': 'Los Angeles',
                'max_capacity': 100,
                'notes': 'notes'
            }
        ).json()

        self.assertTrue(register_response['facility_id'])

    def test_facility_exists(self):
        """Test the error when trying to register a facility which is already there"""

        dbapi = CapacityDatabaseAPI(install_accounts=True)

        login_response = requests.post(
            url=f'{DOMAIN}/login',
            json={'username': 'a', 'password': 'p'}
        ).json()

        # register a facility
        requests.post(
            url=f'{DOMAIN}/facility',
            json={
                'account_id': login_response['account_id'],
                'session_key': login_response['session_key'],
                'name': 'DMV',
                'city': 'Los Angeles',
                'max_capacity': 100,
                'notes': '-'
            }
        ).json()

        # try to register again
        register_response = requests.post(
            url=f'{DOMAIN}/facility',
            json={
                'account_id': login_response['account_id'],
                'session_key': login_response['session_key'],
                'name': 'DMV',
                'city': 'Los Angeles',
                'max_capacity': 100,
                'notes': '-'
            }
        ).json()

        self.assertTrue(register_response['error'])

    def test_update_facility(self):
        """Test updating of a facility info"""

        dbapi = CapacityDatabaseAPI(
            install_accounts=True,
            reinitialize_schema=True
        )

        login_response = requests.post(
            url=f'{DOMAIN}/login',
            json={'username': 'a', 'password': 'p'}
        ).json()

        # get all facilities
        all_facilities = requests.put(
            url=f'{DOMAIN}/manage-facilities/full',
            json={
                'account_id': login_response['account_id'],
                'session_key': login_response['session_key'],
            }
        ).json()

        # update a facility
        update_response = requests.put(
            url=f'{DOMAIN}/facility',
            json={
                'account_id': login_response['account_id'],
                'session_key': login_response['session_key'],
                'facility_id': all_facilities[0]['facility_id'],
                'max_capacity': 100,
                'notes': '-'
            }
        ).json()

        self.assertTrue(update_response['facility_id'] == all_facilities[0]['facility_id'])

    def test_filter_facilities(self):
        """Test getting filtered facility list"""

        dbapi = CapacityDatabaseAPI(
            install_accounts=True,
            reinitialize_schema=True
        )

        login_response = requests.post(
            url=f'{DOMAIN}/login',
            json={'username': 'a', 'password': 'p'}
        ).json()

        # get filtered facilities
        filtered = requests.put(
            url=f'{DOMAIN}/manage-facilities/filter',
            json={
                'account_id': login_response['account_id'],
                'session_key': login_response['session_key'],
                'filter_by': 'total_income',
                'filter_criteria': '<',
                'filter_amount': '0'
            }
        ).json()

        self.assertEqual(5, len(filtered))
