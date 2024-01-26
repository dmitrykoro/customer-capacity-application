import uuid
import datetime

from typing import Any

from .database_utils import DatabaseUtils

SESSION_EXPIRY_TIME = 1  # hours


class Account:
    def __init__(
            self,
            db_utils: DatabaseUtils,
    ) -> None:
        self.table_name = 'account'
        self.db_utils = db_utils

    def create_one(
            self,
            name: str = None,
            role: str = None,
            username: str = None,
            password_hash: str = None,
            facility_id: str = None,
            session_key: str = None,
            session_expires_at: datetime.datetime = None
    ) -> str:
        """
        Create an account. Creates empty account with UID only.
        :return: UID of a created account
        """

        db_uuid = str(uuid.uuid4())

        sql = f'''
            INSERT INTO {self.table_name} (uuid) VALUES  ('{db_uuid}');
        '''
        self.db_utils.exec_commit(sql)

        self._update_one(
            account_id=db_uuid,
            name=name,
            role=role,
            username=username,
            password_hash=password_hash,
            facility_id=facility_id,
            session_key=session_key,
            session_expires_at=session_expires_at
        )

        return db_uuid

    def _update_one(
            self,
            account_id: str,
            name: str = None,
            role: str = None,
            username: str = None,
            password_hash: str = None,
            facility_id: str = None,
            session_key: str = None,
            session_expires_at: datetime.datetime = None
    ) -> dict:
        """
        Update an account. All the arguments except account_id are optional,
        therefore only those passed will be updated for specified account.
        If nothing's passed nothing will be updated.
        :return: list with a tuple containing updated account rows
        """

        arg_dict = locals().copy()
        self.db_utils.update_partial(account_id, table_name=self.table_name, fields=arg_dict)

        return self.get_one(account_id)  # return all account fields of the updated account

    def get_one(
            self,
            account_id: str,
            *args
    ) -> dict or None:
        """
        Get all rows for a specific account record identified by UID
        :param account_id: account UID
        :param args: fields to fetch, if empty, all fields will be fetched
        :return: dict of fields in the following format:
            {'account_id': '123-456', ...}
        """

        sql = f'''
            SELECT * FROM {self.table_name} WHERE uuid = '{account_id}'
        '''
        result = self.db_utils.exec_get_one(sql)

        return dict(
            account_id=result[0],   # return python dict with all account rows. result contains list of table rows
            name=result[1],
            role=result[2],
            username=result[3],
            password_hash=result[4],
            facility_id=result[5],
            session_key=result[6],
            session_expires_at=result[7]
        ) if result else None

    def get_for_login(
            self,
            username: str,
            *args
    ) -> Any:
        """
        Get all rows for a specific account record identified by UID
        :param username: account name
        :param args: fields to fetch, if empty, all fields will be fetched
        :return: dict of fields in the following format:
            {'username': 'johndoe', ...}
        """

        sql = f'''
            SELECT * FROM {self.table_name} WHERE username = '{username}'
        '''
        result = self.db_utils.exec_get_one(sql)

        return dict(
            account_id=result[0],
            name=result[1],
            role=result[2],
            username=result[3],
            password_hash=result[4],
            facility_id=result[5],
            session_key=result[6],
            session_expires_at=result[7]
        ) if result else None

    def update_session_key(
            self,
            account_id: str,
            session_key: str,
            *args
    ) -> dict:
        """
        Store session_key for login
        :param account_id: account id
        :param session_key: a new session key to store
        :param args: fields to fetch, if empty, all fields will be fetched
        :return: dict of fields in the following format:
            {'username': 'johndoe', ...}
        """

        # the current login session expires in SESSION_EXPIRY_TIME hours
        expiry_time = datetime.datetime.now() + datetime.timedelta(hours=SESSION_EXPIRY_TIME)

        result = self._update_one(
            account_id=account_id,
            session_key=session_key,
            session_expires_at=expiry_time
        )
        return result

    def get_session_key(
            self,
            account_id: str
    ) -> str:
        """
        Get session key for the account
        :return: session key or None
        """
        return self.get_one(account_id)['session_key']
