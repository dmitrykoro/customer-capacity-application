from typing import Optional

from .database_utils import DatabaseUtils
from .account import Account
from .customer_visit import CustomerVisit
from .facility import Facility


class CapacityDatabaseAPI:
    def __init__(
            self,
            reinitialize_schema: Optional[bool] = False,
            install_accounts: Optional[bool] = True
    ) -> None:
        self.db_utils = DatabaseUtils()

        if reinitialize_schema:
            self.db_utils.init_schema()

        if install_accounts:
            self.db_utils.install_accounts()

        self.account = Account(
            db_utils=self.db_utils
        )

        self.customer_visit = CustomerVisit(
            db_utils=self.db_utils
        )

        self.facility = Facility(
            db_utils=self.db_utils
        )
