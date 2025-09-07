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
            currenttime = datetime.now()
            #cur.execute("UPDATE keystore SET task=%s,nexttask=%s WHERE nexttask <%s",("No","No" ,currenttime))
            #mysql.commit()

            cur.execute("""SELECT staketrx.*
                FROM staketrx WHERE status=%s and enddate <%s""",["Ongoing",currenttime])
            data = cur.fetchall() 
    
            cur.execute("SELECT * FROM settings WHERE id=1")
            datav = cur.fetchone()
            commission = float(datav["commission"])
            coin_raw_id = datav["coin_raw_id"]
            for data in data:
                print(data)
                uid = data["uid"]
                cur.execute("SELECT * FROM keystore WHERE id=%s",[uid])
                myid = cur.fetchone()
                refer_by = myid["refer_by"]
                refid = ""
                if refer_by !="":
                    cur.execute("SELECT * FROM keystore WHERE refcode=%s",[refer_by])
                    ref = cur.fetchone()
                    refid = ref["id"]
                coin_raw_id = data["coin_raw_id"]
                profit_coin = data["profit_coin"]
                amount = data["amount"]
                ftotal = data["ftotal"]
                id = data["id"]
                status = "Closed"
                ramount = str(float(ftotal)*float(commission)/100)
                cur.execute("UPDATE wallet SET balance=balance + %s WHERE uid=%s and coin_id=%s",(amount ,uid,coin_raw_id))
                cur.execute("UPDATE wallet SET balance=balance + %s WHERE uid=%s and coin_id=%s",(ftotal ,uid,profit_coin))
                cur.execute("UPDATE staketrx SET status=%s WHERE id=%s",(status,id))
                if refid!="":
                    cur.execute("UPDATE wallet SET balance=balance + %s WHERE uid=%s and coin_id=%s",(ramount ,refid,coin_raw_id))
                    cur.execute("INSERT INTO payments (uid,coin_id,type,amount)" "VALUES(%s,%s,%s,%s)",(refid,coin_raw_id,"Referral Bonus",ramount ))
                mysql.commit()

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
        print("All Users Finally")

MiningSystem() 