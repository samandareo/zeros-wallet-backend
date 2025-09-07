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

def withdrawAutoBase():
        key = os.getenv('WALLET_PRIVATE_KEY', '')
        mysql = dbconnection()
        cur = mysql.cursor(dictionary=True,buffered=True)

        cur.execute("""SELECT payments.*,coin.coin_name,coin.coin_symbol,coin.coin_type,coin.platform,
                     coin.contract,coin.explorer,coin.logo,coin.coin_decimal
                     FROM payments LEFT JOIN coin ON payments.coin_id=coin.id 
                     WHERE payments.type=%s and payments.status=%s""",["Withdrew","Pending"])
        pay = cur.fetchall()
        for i in pay:
            platform = i["platform"]
            #toid = i["toid"]
            type = i["coin_type"]
            symbol = i["coin_symbol"]
            contract = i["contract"]
            coin_decimal = i["coin_decimal"] 
            amount = float(i["amount"])
            coin_id=i["coin_id"]
            cur.execute("SELECT * FROM coin WHERE id=%s",[coin_id])
            coin = cur.fetchone()
            fee = coin["fee"]
            fee_coin = coin["fee_coin"]

            id = i["id"]
            rpc =""
            address = i["toid"].lower()
            toid = blocksmith.EthereumWallet.checksum_address(address)
            if platform=="Base":
                web3 = Web3(Web3.HTTPProvider("https://mainnet.base.org/", request_kwargs={'timeout': 60}))
                account = web3.eth.account.from_key(key)
                nonce = web3.eth.get_transaction_count(account.address)
                gasprice = web3.eth.gas_price
                fromid = account.address    
                #bal=float(web3.eth.get_balance(account.address))/1000000000000000000
                try:
                    if type=="Coin":
                       transaction = {
                       'from': fromid,
                       'to': toid,
                       'value':web3.to_wei(amount,'ether'),
                       'nonce': nonce,
                       'chainId': 8453,
                       'gas': 21000,
                       'gasPrice': gasprice,
                       }
                       signed_tx = web3.eth.account.sign_transaction(transaction,key)
                       tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
                       hash = web3.to_hex(tx_hash)
                       query=(hash,"Success",fromid,id )
                       cur.execute("UPDATE payments SET trx=%s,status=%s,fromid=%s WHERE id=%s",query)
                       mysql.commit()
                       print("Withdraw success")
                       return "success"
                    if type=="Token":
                        mul ="1"
                        for m in range(int(coin_decimal)):
                            mul=mul+"0"
                        amountt = int(float(amount)*float(mul))
                        token = web3.eth.contract(address=blocksmith.EthereumWallet.checksum_address(contract.lower()), abi=token_abi)  
                        token_balance = web3.from_wei(token.functions.balanceOf(fromid).call(),'ether') 
                        print(token_balance)
                        transaction = token.functions.transfer(toid,amountt).build_transaction({
                           'gas': 200000,
                           'gasPrice':gasprice,
                           'nonce': nonce,
                        })
                        signed_txn = web3.eth.account.sign_transaction(transaction, key)
                        tx_greeting_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
                        hash = web3.to_hex(tx_greeting_hash)

                        print("Withdraw success")
                except:
                    if coin_id==fee_coin or fee_coin=="" or fee_coin==None:
                        total = float(amount)+float(fee)
                        query=("","Rejected","",id )
                        cur.execute("UPDATE payments SET trx=%s,status=%s,fromid=%s WHERE id=%s",query)
                        cur.execute("UPDATE wallet SET balance=balance + %s WHERE uid=%s and coin_id=%s",(total ,i["uid"],i["coin_id"]))
                        mysql.commit()
                    else:
                        query=("","Rejected","",id )
                        cur.execute("UPDATE payments SET trx=%s,status=%s,fromid=%s WHERE id=%s",query)
                        cur.execute("UPDATE wallet SET balance=balance + %s WHERE uid=%s and coin_id=%s",(amount ,i["uid"],i["coin_id"]))
                        cur.execute("UPDATE wallet SET balance=balance + %s WHERE uid=%s and coin_id=%s",(fee ,i["uid"],fee_coin))
                        mysql.commit()
   
        cur.close()    
        mysql.close()    


def WithdrawSystem(): 
    while True: 
        try:      
            try:
                withdrawAutoBase()  
            except Exception as e:
                print("Withdraw error ",e)      
 
        except KeyboardInterrupt:
           print("Shutdown...")
           stop_threads=True
           break
        except BaseException as e:
           print("Connection Error")
           print(str(e))    
           pass
        print("All Users Finally")

WithdrawSystem() 