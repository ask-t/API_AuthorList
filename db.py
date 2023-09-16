import psycopg2, os, config, json
from psycopg2 import pool

class Database:
    def __init__(self):
        try:
            self.connection_pool = pool.SimpleConnectionPool(1, 10,
                database=os.getenv("DATABASE"),
                host=config.HOST,
                user=config.USER,
                password=config.PASSWORD,
                port=config.PORT)
            print("Connection pool established successfully")
        except Exception as error:
            print(error)

    def _get_connection(self):
        return self.connection_pool.getconn()

    def _release_connection(self, conn):
        self.connection_pool.putconn(conn)

    def create_table(self):
        conn = self._get_connection()
        with conn.cursor() as cur:
            cur.execute("""CREATE TABLE authors (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        birthdate DATE);
                        """)
            conn.commit()
        self._release_connection(conn)

    def insert_data(self, name, birthdate):
        conn = self._get_connection()
        with conn.cursor() as cur:
            cur.execute("""INSERT INTO authors (name, birthdate) VALUES (%s, %s)""", (name, birthdate))
            conn.commit()
        self._release_connection(conn)
        print("Data inserted successfully")

    def get_author_data(self):
        conn = self._get_connection()
        with conn.cursor() as cur:
            cur.execute("""SELECT id, name, birthdate FROM authors""")
            rows = cur.fetchall()
        self._release_connection(conn)
        return rows


if __name__ == "__main__":
    db = Database()

    # Uncomment if creating table for the first time
    # db.create_table()

    rows = db.get_author_data()

    array = []
    for row in rows:
        body = {
            "id": row[0],
            "author": row[1],
            "birthday": row[2]
        }
        print(body)
        array.append(body)

    json_string = json.dumps(array, default=str, indent=4)
    print(json_string)

    # Uncomment if inserting data
    # db.insert_data("John Doe", "1990-01-01")
