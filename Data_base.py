import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

class DataBase:

    def __init__(self):
        self.connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )

        if self.connection.is_connected():
            print("Connexion bien établie !")

    def get_connection(self):
        return self.connection
    