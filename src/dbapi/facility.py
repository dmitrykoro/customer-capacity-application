import uuid

from .database_utils import DatabaseUtils


class Facility:
    def __init__(
            self,
            db_utils: DatabaseUtils
    ) -> None:
        self.table_name = 'facility'
        self.db_utils = db_utils

    def create_one(
            self,
            name: str = None,
            city: str = None,
            max_capacity: int = None,
            notes: str = None
    ) -> str:
        """
        Create a new facility.
        :return: ID in of the created facility
        """

        db_uuid = str(uuid.uuid4())

        sql = f'''
                INSERT INTO {self.table_name} (uuid) VALUES  ('{db_uuid}');
        '''
        self.db_utils.exec_commit(sql)

        self._update_one(
            facility_id=db_uuid,
            name=name,
            city=city,
            max_capacity=max_capacity,
            notes=notes
        )

        return db_uuid

    def _update_one(
            self,
            facility_id: str,
            name: str = None,
            city: str = None,
            max_capacity: int = None,
            notes: str = None
    ) -> dict:

        arg_dict = locals().copy()
        self.db_utils.update_partial(facility_id, table_name=self.table_name, fields=arg_dict)

        return self.get_one(facility_id)

    def get_one(
            self,
            facility_id: str
    ) -> dict:
        """
        Get the facility dict
        :param facility_id: ID of the facility to fetch
        :return: dict
        """

        sql = f'''
            SELECT * FROM {self.table_name} WHERE uuid = '{facility_id}'
        '''
        result = self.db_utils.exec_get_one(sql)

        return dict(
            facility_id=result[0],
            name=result[1],
            city=result[2],
            max_capacity=result[3],
            notes=result[4]
        ) if result else None

    def exists(
            self,
            name: str,
            city: str
    ) -> bool:
        """
        Check if a facility exists. This is determined by the
        name - city combination.
        :return: True if facility exists, False otherwise
        """
        sql = f'''
            SELECT * FROM {self.table_name} WHERE name = '{name}' AND city = '{city}';
        '''
        result = self.db_utils.exec_get_one(sql)

        return result is not None

    def is_full(
            self,
            facility_id: str
    ) -> bool:
        """
        Check if the facility can accept a customer.
        :param facility_id: ID
        :return: True if it can otherwise false
        """

        sql = f'''
            SELECT count(facility_id) FROM customer_visit WHERE facility_id = '{facility_id}' AND checked_out_at IS NULL;
        '''
        current_occupancy = self.db_utils.exec_get_one(sql)[0]

        sql = f'''
            SELECT max_capacity FROM {self.table_name} WHERE uuid = '{facility_id}';
        '''
        max_occupancy = self.db_utils.exec_get_one(sql)[0]

        return True if current_occupancy >= max_occupancy else False

    def delete(
            self,
            facility_id: str
    ) -> None:
        """
        Deletes a facility with a given facility_id
        :param facility_id: ID
        """
        sql = f'''
                    UPDATE facility SET is_active = FALSE WHERE uuid = '{facility_id}';
              '''
        self.db_utils.exec_commit(sql)
