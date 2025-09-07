from datetime import datetime, timedelta, timezone
import mysql.connector
from threading import Thread
import requests
from web3 import Web3
import blocksmith
import cryptocode
import time
import os
from dotenv import load_dotenv
from tokenabi import token_abi

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



def MiningSystem(): 
    while True: 
        try:   
            mysql = dbconnection()
            cur = mysql.cursor(dictionary=True,buffered=True)
            cur.execute("""SELECT *
                FROM airdropparticipate WHERE airdrop_id=%s and status=%s ORDER BY id ASC LIMIT %s""",["16","Unpaid",10])
            data = cur.fetchall() 

            for d in data:
                #print(data)
                uid = d["uid"]
                id = d["id"]
                status = "Paid"
                amount = "3.15"
                cur.execute("UPDATE wallet SET balance=balance + %s WHERE uid=%s and coin_id=%s",(amount ,uid,"4"))
                cur.execute("UPDATE airdropparticipate SET status=%s WHERE id=%s",(status,id))
                cur.execute("INSERT INTO payments (uid,coin_id,type,amount)" "VALUES(%s,%s,%s,%s)",
                            (uid,"4","Airdrop Distribution",amount ))
                mysql.commit()
                print("Airdrop Paid ",id)
            cur.close()
            mysql.close() 
        except KeyboardInterrupt:
           print("Shutdown...")
           stop_threads=True
           break
        except BaseException as e:
           print("Connection Error")
           print(str(e))    
           pass
        print("All Airdrop Finally")

MiningSystem() 