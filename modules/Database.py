from mysql import connector


class Database:
    def __init__(self, username, password, db_name, host="localhost"):
        self._db_name = db_name
        self.__username = username
        self.__password = password
        self.host = host
        self.connection = None
    
    def connect(self):
        self.connection = connector.connect(
            host=self.host,
            database=self._db_name,
            user=self.__username,
            password=self.__password)
        self.cursor = self.connection.cursor()
        print("Database connection established!")

    def execute(self, sql):
        self.cursor.execute(sql)
        self.connection.commit()

    def close(self):
        if self.connection.is_connected():
            self.connection.close()
            self.cursor.close()
            print("Database conection closed!")


class Executor:
    def __init__(self, database):
        self.db = database
        self.db.connect()

    # Saves the given state and timestamp to the database.
    def saveState(self, state:bool):
        self.db.execute("INSERT INTO states(state) VALUES(" + str(state) + ")")

    def close(self):
        self.db.close()