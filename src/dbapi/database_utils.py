import datetime
import random

import psycopg2
import yaml
import os
import hashlib
import uuid


class DatabaseUtils:
    def __init__(
            self,
            db_credentials: str = '../../config/db.yml'
    ) -> None:
        """
        Store database credentials in memory to prevent file parsing for each query
        :param db_credentials:
        """
        yml_path = os.path.join(os.path.dirname(__file__), db_credentials)

        with open(yml_path, 'r') as file:
            config = yaml.load(file, Loader=yaml.FullLoader)

        self.db_credentials = dict(
            database=config['database'],
            user=config['user'],
            password=config['password'],
            host=config['host'],
            port=config['port']
        )

    def install_accounts(
            self,
            install_more_visits: bool = False
    ) -> None:
        """
        Insert Administrator and Bouncer account information into the database.
        Insert sample facilities and sample visits info.
        :install_more_visits:
            if True, will install from 100 to 1000 visits per facility.
            if False, will install from 1 to 10 visits per facility. (for faster tests)
        :return: None
        """

        bouncer_facility_id = 'cbded9e5-1698-4020-bf6c-10f9ee7f0e66'
        facility_id_1 = '8d6aaa9e-4fe6-4201-ac62-154c065a1e5e'
        facility_id_2 = 'de0b7116-384c-4f8b-a8cd-022bca9ceabd'
        facility_id_3 = '93199edc-167c-455e-af44-b52527e15998'
        facility_id_4 = 'f8d6aa82-1694-4b29-9c39-c9946da98bab'

        bouncer_account_id = '3ed6ad96-859f-4ee4-a074-401a8ed2a57c'
        admin_account_id = 'c02d6f38-3303-4c08-9405-9bcc80629278'

        sql = f'''
            DELETE FROM customer_visit WHERE facility_id = '{bouncer_facility_id}'
                            OR facility_id = '{facility_id_1}'
                            OR facility_id = '{facility_id_2}'
                            OR facility_id = '{facility_id_3}'
                            OR facility_id = '{facility_id_4}';
            DELETE FROM account WHERE uuid = '{admin_account_id}' OR uuid = '{bouncer_account_id}';
            DELETE FROM facility WHERE uuid = '{bouncer_facility_id}'
                            OR uuid = '{facility_id_1}'
                            OR uuid = '{facility_id_2}'
                            OR uuid = '{facility_id_3}'
                            OR uuid = '{facility_id_4}';
            INSERT INTO facility(
                uuid, name, city, max_capacity, notes
            )
            VALUES 
                ('{bouncer_facility_id}', 'DMV', 'Los Angeles', 3, 'Fire dpt. 3'),
                ('{facility_id_1}', 'Social Security Administration', 'Halifax', 30, '-'),
                ('{facility_id_2}', 'Nightclub', 'New York', 300, 'Genre: Classic Rock'),
                ('{facility_id_3}', 'Supermarket', 'San Francisco', 150, 'Contract until 08/25'),
                ('{facility_id_4}', 'Skyscrapper Viewpoint', 'Nashville', 40, '-');
        '''
        self.exec_commit(sql)

        sql = f'''
            INSERT INTO account(
                uuid, name, role, username, password_hash, facility_id
            ) 
            VALUES 
                ('{admin_account_id}', 'Administrator', 'admin', 'a', 
                    '{hashlib.sha512('p'.encode('utf-8')).hexdigest()}', NULL),
                ('{bouncer_account_id}', 'Bouncer', 'bouncer', 'b',
                    '{hashlib.sha512('p'.encode('utf-8')).hexdigest()}', '{bouncer_facility_id}');
        '''
        self.exec_commit(sql)

        facility_ids = [facility_id_1, facility_id_2, facility_id_3, facility_id_4]

        for current_facility_id in facility_ids:
            if install_more_visits:
                min_visits = 100
                max_visits = 1000
            else:
                min_visits = 2
                max_visits = 10

            number_of_closed_visits = random.randrange(min_visits, max_visits)

            for _ in range(number_of_closed_visits):
                sql = f'''
                    INSERT INTO customer_visit(
                        uuid, name, document_id, age, facility_id, checked_in_at, checked_out_at, charge
                    )
                    VALUES 
                    ('{str(uuid.uuid4())}', 'Dima K.', '123-456-7890', 25, 
                        '{current_facility_id}', '{datetime.datetime.now()}', '{datetime.datetime.now()}', 
                        '{random.randrange(10, 100)}')
                '''
                self.exec_commit(sql)

            # insert some open visits
            for _ in range(random.randrange(1, int(0.2 * max_visits))):
                sql = f'''
                    INSERT INTO customer_visit(
                        uuid, name, document_id, age, facility_id, checked_in_at, checked_out_at, charge
                    )
                    VALUES 
                    ('{str(uuid.uuid4())}', 'Dima K.', '123-456-7890', 25, 
                        '{current_facility_id}', '{datetime.datetime.now()}', NULL, 
                        '{random.randrange(10, 100)}')
                '''
                self.exec_commit(sql)

    def connect(self) -> psycopg2.connect:
        """
        Create a database connection.
        :return: psycopg connection
        """
        return psycopg2.connect(
            database=self.db_credentials['database'],
            user=self.db_credentials['user'],
            password=self.db_credentials['password'],
            host=self.db_credentials['host'],
            port=self.db_credentials['port']
        )

    def init_schema(
            self,
            schema_path: str = 'schema.sql'
    ) -> None:
        """
        Recreate the tables to initialize the db.
        :return: None
        """
        self.exec_sql_file(schema_path)

    def get_all_rows(
            self,
            table_name: str
    ) -> list[tuple]:
        """
        Get all rows from a table.
        :param table_name: a name of table
        :return: a list of tuples in the format
            [(col1_row1_value, col2_row1_value, ...,), (col2_row1_value, col2_row2_value, ...,),]
        """
        return self.exec_get_all(f'SELECT * FROM {table_name}')

    def update_partial(
            self,
            uuid: str,
            table_name: str,
            fields: dict
    ) -> None:
        """
        Update field values of the passed fields in a specified table.
        :param uuid: id of a table record
        :param table_name: name of the table
        :param fields: dict with arguments to update
        :return: None
        """

        for item in list(fields.items())[2:]:   # iterate through caller func args except [self, uuid
            if item[1]:                         # if arg was passed update it
                sql = f'''
                    UPDATE {table_name} SET {item[0]} = '{item[1]}' WHERE uuid = '{uuid}'
                '''
                self.exec_commit(sql)

    def exec_sql_file(
            self,
            path: str
    ) -> None:

        full_path = os.path.join(os.path.dirname(__file__), f'{path}')
        conn = self.connect()
        cur = conn.cursor()

        with open(full_path, 'r') as file:
            cur.execute(file.read())

        conn.commit()
        conn.close()

    def exec_get_one(
            self,
            sql: str,
            args=None
    ) -> tuple:
        if args is None:
            args = {}

        conn = self.connect()
        cur = conn.cursor()
        cur.execute(sql, args)
        one = cur.fetchone()

        conn.close()

        return one

    def exec_get_all(
            self,
            sql: str,
            args=None
    ) -> list[tuple]:

        conn = self.connect()
        cur = conn.cursor()
        cur.execute(sql, args)
        list_of_tuples = cur.fetchall()

        conn.close()

        return list_of_tuples

    def exec_commit(
            self,
            sql,
            args=None
    ) -> tuple:

        conn = self.connect()
        cur = conn.cursor()
        result = cur.execute(sql, args)
        conn.commit()

        conn.close()

        return result
