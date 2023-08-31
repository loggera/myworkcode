import pymysql


class MySQLHelper:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.password = 'root'
        self.database = 'amazon_work'
        self.connection = None

    def connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Connected to MySQL database")
        except pymysql.Error as e:
            print(f"Error connecting to MySQL database: {e}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Disconnected from MySQL database")

    def execute_query(self, query):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return result
        except pymysql.Error as e:
            print(f"Error executing query: {e}")
            return None



    def execute_update(self, query):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
            self.connection.commit()
            print("Query executed successfully")
        except pymysql.Error as e:
            print(f"Error executing query: {e}")

    def execute_batch_create(self, sql, value):
        try:
            with self.connection.cursor() as cursor:
                cursor.executemany(sql, value)
            self.connection.commit()
            print("Query executed successfully")
        except pymysql.Error as e:
            print(f"Error executing query: {e}")
