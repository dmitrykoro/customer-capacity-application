import datetime
import uuid

from .database_utils import DatabaseUtils
from typing import Optional


class CustomerVisit:
    def __init__(
            self,
            db_utils: DatabaseUtils
    ) -> None:
        self.table_name = 'customer_visit'
        self.db_utils = db_utils

    def create_one(
            self,
            name: Optional[str] = None,
            document_id: Optional[str] = None,
            age: Optional[int] = None,
            facility_id: Optional[str] = None,
            checked_in_at: Optional[datetime.datetime] = None,
            checked_out_at: Optional[datetime.datetime] = None,
            charge: Optional[float] = None
    ) -> str:
        """
        Create a customer entry.
        :return: UID of a created entry
        """

        db_uuid = str(uuid.uuid4())

        sql = f'''
                INSERT INTO {self.table_name} (uuid) VALUES  ('{db_uuid}');
        '''
        self.db_utils.exec_commit(sql)

        self._update_one(
            customer_id=db_uuid,
            name=name,
            document_id=document_id,
            age=age,
            facility_id=facility_id,
            checked_in_at=checked_in_at,
            checked_out_at=checked_out_at,
            charge=charge
        )

        return db_uuid

    def _update_one(
            self,
            customer_id: str,
            name: Optional[str] = None,
            document_id: Optional[str] = None,
            age: Optional[int] = None,
            facility_id: Optional[str] = None,
            checked_in_at: Optional[datetime.datetime] = None,
            checked_out_at: Optional[datetime.datetime] = None,
            charge: Optional[float] = None
    ) -> None:

        arg_dict = locals().copy()
        self.db_utils.update_partial(customer_id, table_name=self.table_name, fields=arg_dict)

    def is_open(
            self,
            document_id: str
    ) -> bool:
        """
        Check if a customer visit is open.
        If in the DB there's a record with NULL checked_out_at for the provided document_id,
        it means that this customer hasn't been checked out, and their visit is still in progress.
        :param document_id: document id to check the customer
        :return: True if there's an open visit, False otherwise
        """
        sql = f'''
            SELECT * FROM customer_visit WHERE document_id LIKE '{document_id}' AND checked_out_at IS NULL;
        '''
        result = self.db_utils.exec_get_one(sql)

        return True if result else False

    def check_out(
            self,
            document_id: str,
            charge: float
    ) -> None:
        """
        End customer visit by setting checked_out_at to now() and setting charge amount.
        :param charge: charge amount
        :param document_id: ID of the customer document
        :return: None
        """

        sql = f'''
            UPDATE {self.table_name} 
                SET checked_out_at = '{datetime.datetime.now()}', charge = '{charge}' 
                WHERE document_id = '{document_id}' AND checked_out_at IS NULL
        '''
        self.db_utils.exec_commit(sql)

    def get_filtered_facility_entries(
            self,
            filter_by: str,
            filter_criteria: str,
            filter_amount: str
    ) -> list[dict] or None:
        """
        Get filtered facility entries.
        :param filter_by: 'total_population' or 'total_income'
        :param filter_criteria: '=', '>' or '<'
        :param filter_amount: number to filter by
        :return: dict of matching nightfacilities
        """
        sql = f'''
                WITH t1 AS (
                SELECT facility_id, c.name, sum(charge) AS total_income, count(facility_id) AS total_population
                    FROM customer_visit
                    JOIN facility c ON c.uuid = customer_visit.facility_id
                    WHERE checked_out_at IS NOT NULL
                    GROUP BY c.name, facility_id
                ),
                
                t2 AS (
                SELECT facility_id, count(facility_id) AS occupancy 
                    FROM customer_visit
                    WHERE checked_out_at IS NULL
                    GROUP BY facility_id
                )
                
                SELECT t1.facility_id, t1.name, t1.total_income, total_population, occupancy 
                    FROM t1 
                    JOIN t2 t22 ON t1.facility_id = t22.facility_id
        '''

        if filter_by:
            sql += f' WHERE {filter_by} {filter_criteria} {filter_amount};'
        res = self.db_utils.exec_get_all(sql)

        return [
            dict(
                facility_id=result[0],
                name=result[1],
                income=result[2],
                population=result[3],
                occupancy=result[4]
            ) for result in res
        ]

    def get_all_facilities_with_visits(self) -> list[dict] or None:
        """
        Get all facilities with additional info.
        :return: all facility entries in the database
        """
        return self.get_filtered_facility_entries(
            filter_by=None,
            filter_criteria=None,
            filter_amount=None
        )
