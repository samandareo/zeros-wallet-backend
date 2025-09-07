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

def depositCheck(uid,key):
    trxlist=[]
    mysql = dbconnection()
    cur = mysql.cursor(dictionary=True,buffered=True)
    cur.execute("""SELECT wallet.*,coin.coin_name,coin.coin_symbol,coin.coin_type,coin.platform,
                         coin.contract,coin.explorer,coin.logo,coin.price,coin.day_change,
                         coin.deposit,coin.withdrew,coin.fee,coin.fee_coin,coin.fund_address,coin.coin_decimal
                         FROM wallet LEFT JOIN coin ON wallet.coin_id=coin.id WHERE wallet.uid=%s""",[uid])
    wallet = cur.fetchall() 
    cur.execute("SELECT * FROM acc WHERE user_id=%s",[uid])
    user = cur.fetchone()   
    for i in wallet:
        #print(i)
        platform = i["platform"]
        address = i["address"]
        type = i["coin_type"]
        coin_id = i["coin_id"]
        symbol = i["coin_symbol"]
        contract = i["contract"]
        coin_decimal=i["coin_decimal"]
        deposit = i["deposit"]
        if platform=="Base":
            if type=="Coin":
                url = "https://api.basescan.org/api?module=account&action=txlist&address="+address+"&startblock=0&endblock=9999999999&page=1&offset=100&sort=desc&apikey="+os.getenv('BASESCAN_API_KEY', '')
                response = requests.get(url)
                data = response.json()
                for d in data["result"]:
                    hash = d['hash']
                    value = float(d['value'])/ 1000000000000000000
                    fromadd = d['from']
                    toadd = d['to']
                    if toadd.lower()==address.lower():
                        cur.execute("SELECT * FROM payments WHERE status=%s and trx=%s",["Success",hash])
                        resultv = cur.fetchall()    
                        if len(resultv)==0:
                            if deposit=="1" and float(value)>0.000001:
                                try:
                                    mysql.autocommit = True 
                                    mysql.start_transaction()
                                    cur.execute("UPDATE wallet SET balance=balance + %s WHERE uid=%s and coin_id=%s",(value ,uid,coin_id))  
                                    cur.execute("INSERT INTO payments (uid,coin_id,type,amount,trx,status,fromid,toid)" "VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",
                                    (uid,coin_id,"Deposit",value,hash,"Success",fromadd,toadd ))
                                    cur.execute("DELETE FROM payments WHERE status=%s and trx=%s", ["Pending",hash])
                                    mysql.commit()  
                                except mysql.connector.Error as error:
                                    mysql.rollback()    
                                    print("Deposit RollBack")   
                                    pass 
                            else:
                                print("Deposit False or Amount less")              
                        else:
                            print("Trx Exits : ",hash) 
                            cur.execute("DELETE FROM payments WHERE status=%s and trx=%s", ["Pending",hash])
                            mysql.commit()
                            if len(resultv)>1:
                                exv = resultv[-1]
                                tid = exv["id"]
                                cid = exv["coin_id"]
                                amount = exv["amount"]
                                print(amount)
                                print(len(resultv))   
                                try:
                                    mysql.autocommit = True
                                    mysql.start_transaction()  
                                    cur.execute("DELETE FROM payments WHERE id=%s", [tid ])
                                    cur.execute("UPDATE wallet SET balance=balance - %s WHERE uid=%s and coin_id=%s",(amount ,uid,cid))
                                    mysql.commit()     
                                    print("Deleted : ",tid)  
                                except mysql.connector.Error as error:
                                    mysql.rollback()    
                                    print("Trx Deleted RollBack") 
                                    pass

        if platform=="Binance":
            if type=="Coin":
                url = "https://api.bscscan.com/api?module=account&action=txlist&address="+address+"&startblock=0&endblock=9999999999&page=1&offset=100&sort=desc&apikey="+os.getenv('BSCSCAN_API_KEY', '')
                response = requests.get(url)
                data = response.json()
                for d in data["result"]:
                    hash = d['hash']
                    value = float(d['value'])/ 1000000000000000000
                    fromadd = d['from']
                    toadd = d['to']
                    if toadd.lower()==address.lower():
                        cur.execute("SELECT * FROM payments WHERE status=%s and trx=%s",["Success",hash])
                        resultv = cur.fetchall()    
                        if len(resultv)==0:
                            if deposit=="1" and float(value)>0.000001:
                                try:
                                    mysql.autocommit = True 
                                    mysql.start_transaction()
                                    cur.execute("UPDATE wallet SET balance=balance + %s WHERE uid=%s and coin_id=%s",(value ,uid,coin_id))  
                                    cur.execute("INSERT INTO payments (uid,coin_id,type,amount,trx,status,fromid,toid)" "VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",
                                    (uid,coin_id,"Deposit",value,hash,"Success",fromadd,toadd ))
                                    cur.execute("DELETE FROM payments WHERE status=%s and trx=%s", ["Pending",hash])
                                    mysql.commit()  
                                except mysql.connector.Error as error:
                                    mysql.rollback()    
                                    print("Deposit RollBack")   
                                    pass 
                            else:
                                print("Deposit False or Amount less")              
                        else:
                            print("Trx Exits : ",hash) 
                            cur.execute("DELETE FROM payments WHERE status=%s and trx=%s", ["Pending",hash])
                            mysql.commit()
                            if len(resultv)>1:
                                exv = resultv[-1]
                                tid = exv["id"]
                                cid = exv["coin_id"]
                                amount = exv["amount"]
                                print(amount)
                                print(len(resultv))   
                                try:
                                    mysql.autocommit = True
                                    mysql.start_transaction()  
                                    cur.execute("DELETE FROM payments WHERE id=%s", [tid ])
                                    cur.execute("UPDATE wallet SET balance=balance - %s WHERE uid=%s and coin_id=%s",(amount ,uid,cid))
                                    mysql.commit()     
                                    print("Deleted : ",tid)  
                                except mysql.connector.Error as error:
                                    mysql.rollback()    
                                    print("Trx Deleted RollBack") 
                                    pass


def fundTransferBase(uid,key):
    mysql = dbconnection()
    cur = mysql.cursor(dictionary=True,buffered=True)
    cur.execute("""SELECT wallet.*,coin.coin_name,coin.coin_symbol,coin.coin_type,coin.platform,
                         coin.contract,coin.explorer,coin.logo,coin.price,coin.day_change,
                         coin.deposit,coin.withdrew,coin.fee,coin.fee_coin,coin.fund_address,coin.coin_decimal
                         FROM wallet LEFT JOIN coin ON wallet.coin_id=coin.id WHERE wallet.uid=%s""",[uid])
    wallet = cur.fetchall()  
    for i in wallet:
        platform = i["platform"]
        address = i["address"]
        type = i["coin_type"]
        symbol = i["coin_symbol"]
        contract = i["contract"]
        coin_decimal=i["coin_decimal"]
        fund_address = i["fund_address"]   
        if platform=="Fantom":
            web3 = Web3(Web3.HTTPProvider("https://mainnet.base.org/", request_kwargs={'timeout': 60}))
            nonce = web3.eth.get_transaction_count(address)
            gasprice = web3.eth.gas_price
            account = web3.eth.account.from_key(key)
            if type=="Coin":
                bal=float(web3.eth.get_balance(address))/1000000000000000000
                gasfee = ((21000*float(gasprice))/1000000000000000000)+0.00000001
                zbal = bal-0.00000045 #gasfee
                if float(bal)>0.005:
                    transaction = {
                        'from': account.address,
                        'to': fund_address,
                        'value':web3.to_wei(zbal,'ether'),
                        'nonce': nonce,
                        'chainId': 8453,
                        'gas': 21000,
                        'gasPrice': gasprice,
                    }
                    signed_tx = web3.eth.account.sign_transaction(transaction,key)
                    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
                    print(web3.to_hex(tx_hash))               
            if type=="Token":
                gasfee = ((21000*float(gasprice))/1000000000000000000)+0.00001
                bal=float(web3.eth.get_balance(address))/1000000000000000000
                token = web3.eth.contract(address=blocksmith.EthereumWallet.checksum_address(contract.lower()), abi=token_abi)  
                token_balance = web3.from_wei(token.functions.balanceOf(address).call(),'ether') 
                print("Token ",token_balance)
                transaction = token.functions.transfer(fund_address,web3.to_wei(str(token_balance),'ether')).build_transaction({
                           'gas': 200000,
                           'gasPrice':gasprice,
                           'nonce': nonce,
                        })
                if float(token_balance)>0:
                    signed_txn = web3.eth.account.sign_transaction(transaction, key)
                    tx_greeting_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
                    hash = web3.to_hex(tx_greeting_hash)     
                    print("Token Transfered") 


def DepositSystem(): 
    while True: 
        try:   
            mysql = dbconnection()
            cur = mysql.cursor(dictionary=True,buffered=True)
            cur.execute("""
                        SELECT payments.*,coin.coin_name,coin.coin_symbol,coin.coin_type,coin.platform,
                        coin.contract,coin.explorer,coin.logo,acc.ethkey FROM payments 
                        LEFT JOIN coin ON payments.coin_id=coin.id 
                        LEFT JOIN acc ON payments.uid=acc.user_id
                        WHERE payments.type=%s and payments.status=%s ORDER by payments.id DESC LIMIT %s 
                        """,["Deposit","Pending",30])
            data = cur.fetchall()
            for i in data:
                try:
                    uid = i["uid"]
                    key=key = cryptocode.decrypt(i["ethkey"],"mxbvcsjjhgf9872881")
                    print(key)
                    depositCheck(uid,key)
                    #fundTransferBase(uid,key)
                    print("UID : ", uid)
                    #print(i)
                except KeyboardInterrupt:
                    print("Shutdown...")
                    break   
                except:
                    pass   
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

DepositSystem() 