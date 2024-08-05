import psycopg2
from faker import Faker
from datetime import datetime


fake = Faker()
create_table_queries = [
        """
        CREATE TABLE IF NOT EXISTS table1 (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            surname VARCHAR(255),
            date_of_birth DATE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS table2 (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255),
            age INTEGER
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS table3 (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            age VARCHAR(255),
            date_of_birth VARCHAR(255)

        );
        """
    ]


class Postgres:
    def __init__(self):
        #postgresql connection
        try:
                self.db_postgres = psycopg2.connect(
                    database = "db_postgres",
                    user = "root",
                    password = "root",
                    host = "host_postgres",
                    port = "5432"
                )
                print("POSTGRES BAGLANDI")
        except psycopg2.Error as e:
                print(f"failed to connect to database: {e}")
        

    #clear tables in both databases
    def clear_tables(self):
        with self.db_postgres.cursor() as postgres_cursor:
            try:
                #clear postgresql tables
                postgres_cursor.execute('TRUNCATE TABLE table1')
                postgres_cursor.execute('TRUNCATE TABLE table2')
                postgres_cursor.execute('TRUNCATE TABLE table3')
                self.db_postgres.commit()
            except (psycopg2.Error) as e:
                print(f"error clearing tables: {e}")
                self.db_postgres.rollback()

    #create tables for postgresql database
    def create_tables(self):
        with self.db_postgres.cursor() as cursor:
            for query in create_table_queries:
                try:
                    cursor.execute(query)
                    print("creating table in postgreSQL database")
                    self.db_postgres.commit()
                except psycopg2.Error as e:
                    print(f"error while creating tables for POSTGRESQL database: {e}")



    #POSTGRES INSERTION
    def insert_db(self):
        #dummy data
        name_list = [fake.first_name() for _ in range(10)]
        surname_list = [fake.last_name() for _ in range(10)]
        email_list = [fake.email() for _ in range(10)]
        date_of_birth_list = [str(fake.date_of_birth(minimum_age=18, maximum_age=90)) for _ in range(10)]
        age_list = [2024 - datetime.strptime(date_of_birth_list[i], "%Y-%m-%d").year for i in range(10)]

        with self.db_postgres.cursor() as cursor:
            try:
                for i in range(10):
                    cursor.execute('''INSERT INTO table1 (name, surname, date_of_birth) VALUES (%s, %s, %s)                
                        ''',(name_list[i], surname_list[i], date_of_birth_list[i]))
                    cursor.execute('''INSERT INTO table2 (email, age) VALUES (%s, %s)                
                        ''',(email_list[i], age_list[i]))
                    cursor.execute('''INSERT INTO table3 (name, age, date_of_birth) VALUES (%s, %s, %s)                
                        ''',(name_list[i], age_list[i], date_of_birth_list[i]))
                self.db_postgres.commit()
            except psycopg2.Error as e:
                self.db_postgres.rollback()
                print(f"DATABASE ERROR: {e} ")
