import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def dbconnection():
    connection=None
    try:
        connection = mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'user'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'zeros'),
        charset='utf8mb4'
        )
        print("Connection to MySQL DB successful ")
    except:
        connection.reconnect()
        print("Db Connection Error")
        #mysql.cursor(dictionary=True,buffered=True) 
    return connection 