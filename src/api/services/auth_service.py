import hashlib
import secrets


class AuthenticationService:
    def __init__(
            self,
            dbapi
    ) -> None:
        self.dbapi = dbapi

    @staticmethod
    def calculate_password_hash(password: str) -> str:
        """
        Calculate SHA512 hash for a given password.
        :param password: password
        :return: password hash
        """
        return hashlib.sha512(password.encode('utf-8')).hexdigest()

    @staticmethod
    def generate_session_token():
        """
        Generate a token.
        :return: token
        """
        return secrets.token_hex(32)

    def check_session_key(
            self,
            account_id: str,
            session_key: str
    ) -> bool:
        """
        Check session key provided in the request.
        :param account_id: account id to check its session key
        :param session_key: provided session key
        :return: True if the key is valid, False otherwise
        """
        stored_session_key = self.dbapi.account.get_session_key(account_id)

        success = True

        if not account_id or not session_key or not stored_session_key or stored_session_key == '':
            success = False
        if stored_session_key != session_key:
            success = False

        return success

    def try_to_authorize(
            self,
            username: str,
            password: str
    ) -> dict:
        """
        Try to authorize the user.
        :param username: provided username
        :param password: provided password
        :return:
            If username is not found, return dict:
                (error='account-not-found')
            If password is incorrect, return dict:
                (error='wrong-password')
            Otherwise, return all account fields.
        """
        account_fields = self.dbapi.account.get_for_login(
            username=username
        )

        if not account_fields:
            return dict(error='account-not-found')

        stored_password_hash = account_fields['password_hash']
        provided_password_hash = self.calculate_password_hash(password)

        if stored_password_hash != provided_password_hash:
            return dict(error='wrong-password')

        new_session_token = self.generate_session_token()
        self.dbapi.account.update_session_key(
            account_id=account_fields['account_id'],
            session_key=new_session_token
        )

        return self.dbapi.account.get_one(account_id=account_fields['account_id'])

    def log_out(
            self,
            account_id: str
    ) -> None:
        """
        Erase session key for the account.
        :param account_id: ID of the account
        :return:
        """
        self.dbapi.account.update_session_key(
            account_id=account_id,
            session_key=''
        )
