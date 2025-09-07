from apps import *
from apps.db import dbconnection
from apps.route import tokenabi
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

token_abi = tokenabi

def depositCheck(uid,key,solkey):
    trxlist=[]
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
                        cur.execute("SELECT * FROM payments WHERE coin_id=%s and trx=%s",[coin_id,hash])
                        resultv = cur.fetchall()    
                        if len(resultv)==0:
                            if deposit=="1" and float(value)>0.000001:
                                try:
                                    mysql.autocommit = True 
                                    mysql.start_transaction() 
                                    cur.execute("INSERT INTO payments (uid,coin_id,type,amount,trx,status,fromid,toid)" "VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",
                                    (uid,coin_id,"Deposit",value,hash,"Pending",fromadd,toadd ))
                                    mysql.commit()  
                                except mysql.connector.Error as error:
                                    mysql.rollback()    
                                    print("Deposit RollBack")   
                                    pass 
                        else:
                            print("Deposit False or Amount less")              

            if type=="Token":
                if deposit=="1":
                    mul ="1"
                    for m in range(int(coin_decimal)):
                        mul=mul+"0"
                    url = "https://api.basescan.org/api?module=account&action=tokentx&contractaddress="+contract+"&address="+address+"&page=1&offset=100&startblock=0&endblock=2007025780&sort=desc&apikey="+os.getenv('BASESCAN_API_KEY', '')
                    response = requests.get(url)
                    data = response.json()
                    for d in data["result"]:
                        hash = d['hash']
                        value = float(d['value'])/float(mul)
                        fromadd = d['from']
                        toadd = d['to']
                        if toadd.lower()==address.lower():
                            cur.execute("SELECT * FROM payments WHERE coin_id=%s and trx=%s",[coin_id,hash])
                            resultv = cur.fetchall()    
                            if len(resultv)==0:
                                try:
                                    mysql.autocommit = True 
                                    mysql.start_transaction()
                                    cur.execute("INSERT INTO payments (uid,coin_id,type,amount,trx,status,fromid,toid)" "VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",
                                    (uid,coin_id,"Deposit",value,hash,"Pending",fromadd,toadd,hash ))
                                    mysql.commit()  
                                except mysql.connector.Error as error:
                                    mysql.rollback()    
                                    print("Deposit RollBack")   
                                    pass 
                else:
                    print("Deposit False or Amount less")  


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
                        cur.execute("SELECT * FROM payments WHERE coin_id=%s and trx=%s",[coin_id,hash])
                        resultv = cur.fetchall()    
                        if len(resultv)==0:
                            if deposit=="1" and float(value)>0.000001:
                                try:
                                    mysql.autocommit = True 
                                    mysql.start_transaction() 
                                    cur.execute("INSERT INTO payments (uid,coin_id,type,amount,trx,status,fromid,toid)" "VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",
                                    (uid,coin_id,"Deposit",value,hash,"Pending",fromadd,toadd ))
                                    mysql.commit()  
                                except mysql.connector.Error as error:
                                    mysql.rollback()    
                                    print("Deposit RollBack")   
                                    pass 
                        else:
                            print("Deposit False or Amount less")              



    cur.close()
    mysql.close()          

def Base(uid,key):
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
        if platform=="Base":
            web3 = Web3(Web3.HTTPProvider("https://mainnet.base.org", request_kwargs={'timeout': 60}))
            nonce = web3.eth.get_transaction_count(address)
            gasprice = web3.eth.gas_price
            account = web3.eth.account.from_key(key)
            if type=="Coin":
                bal=float(web3.eth.get_balance(address))/1000000000000000000
                gasfee = ((21000*float(gasprice))/1000000000000000000)+0.00000044
                zbal = bal-0.00000045 #gasfee
                print(zbal,"zbal")
                print(gasfee,"Gas Fee")
                if float(bal)>0.00001:
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
                    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
                    print(web3.to_hex(tx_hash)) 
  

def fundTransferBbnb(uid,key):
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
        if platform=="Binance":
            web3 = Web3(Web3.HTTPProvider("https://bsc-dataseed.binance.org/", request_kwargs={'timeout': 60}))
            nonce = web3.eth.get_transaction_count(address)
            gasprice = web3.eth.gas_price
            account = web3.eth.account.from_key(key)
            if type=="Coin":
                bal=float(web3.eth.get_balance(address))/1000000000000000000
                gasfee = ((21000*float(gasprice))/1000000000000000000)+0.00000001
                zbal = bal-gasfee
                if float(bal)>0.00001:
                    transaction = {
                        'from': account.address,
                        'to': fund_address,
                        'value':web3.to_wei(zbal,'ether'),
                        'nonce': nonce,
                        'chainId': 56,
                        'gas': 21000,
                        'gasPrice': gasprice,
                    }
                    signed_tx = web3.eth.account.sign_transaction(transaction,key)
                    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
                    print(web3.to_hex(tx_hash)) 


def walletcreate(uid):
    mysql = dbconnection()
    cur = mysql.cursor(dictionary=True,buffered=True)
    cur.execute("SELECT * FROM acc WHERE user_id=%s",[uid])
    user = cur.fetchone()
    key = cryptocode.decrypt(user["ethkey"],privatepass)
    soladdress = user["sol_address"]
    address = blocksmith.EthereumWallet.generate_address(key)
    checksum_address = blocksmith.EthereumWallet.checksum_address(address)
    #print(checksum_address)
    btcaddress = blocksmith.BitcoinWallet.generate_address(key)
    #print(btcaddress)
    cur.execute("SELECT * FROM settings WHERE id=%s",[1])
    data = cur.fetchone()
    rbonus=data["registerbonus"]
    coin_raw_id=data["coin_raw_id"]
    data = cur.execute("SELECT * FROM coin ORDER BY id DESC")
    coin = cur.fetchall()
    cur.close()
    for i in coin:
        platform=i["platform"]
        id=i["id"]
        #print(i["id"])
        mysql = dbconnection()
        cur = mysql.cursor(dictionary=True,buffered=True)
        cur.execute("SELECT * FROM wallet WHERE uid=%s and coin_id=%s",[uid,i["id"]])
        all = cur.fetchall()
        if all:
            print("wallet lenght ",len(all))
            if len(all)>1:
                cur.execute("DELETE FROM wallet WHERE uid=%s and coin_id=%s and balance=%s",[uid,i["id"],"0"])
                mysql.commit() 
                print("Deleted Wallet")    
            cur.close()
        else:
            if platform=="Ethereum" or platform=="Binance" or platform=="Fantom" or platform=="Polygon" or platform=="Avalance" or platform=="Base":
                if id==4 and float(rbonus)>0:
                    mysql = dbconnection()
                    cur = mysql.cursor(dictionary=True,buffered=True)
                    cur.execute("INSERT INTO wallet (uid,coin_id,address,balance)" "VALUES(%s,%s,%s,%s)",(uid,id,checksum_address,rbonus ))
                    mysql.commit() 
                    cur.execute("INSERT INTO payments (uid,coin_id,type,amount)" "VALUES(%s,%s,%s,%s)",(uid,id,"Register Bonus",rbonus ))
                    mysql.commit() 
                    cur.close()
                    print("okk1")
                else:
                    mysql = dbconnection()
                    cur = mysql.cursor(dictionary=True,buffered=True)
                    cur.execute("INSERT INTO wallet (uid,coin_id,address)" "VALUES(%s,%s,%s)",(uid,id,checksum_address))
                    mysql.commit()  
                    cur.close()  
                    print("okk 2")
            if platform=="Solana":
                if id==4 and float(rbonus)>0:
                    mysql = dbconnection()
                    cur = mysql.cursor(dictionary=True,buffered=True)
                    cur.execute("INSERT INTO wallet (uid,coin_id,address,balance)" "VALUES(%s,%s,%s,%s)",(uid,id,soladdress,rbonus))
                    mysql.commit()    
                    cur.execute("INSERT INTO payments (uid,coin_id,type,amount)" "VALUES(%s,%s,%s,%s)",(uid,id,"Register Bonus",rbonus ))
                    mysql.commit() 
                    cur.close()
                else:
                    mysql = dbconnection()
                    cur = mysql.cursor(dictionary=True,buffered=True)
                    cur.execute("INSERT INTO wallet (uid,coin_id,address)" "VALUES(%s,%s,%s)",(uid,id,soladdress))
                    mysql.commit() 

@app.route('/auth/deposit', methods=['POST','GET'])
def mydeposit():
    if request.method == "POST":
        token = request.form['token']
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["user_id"]
            mysql = dbconnection()
            cur = mysql.cursor(dictionary=True,buffered=True)
            cur.execute("SELECT * FROM acc WHERE user_id=%s",[uid])
            user = cur.fetchone() 
            key = cryptocode.decrypt(user["ethkey"],privatepass)
            solkey = cryptocode.decrypt(user["solkey"],privatepass)
            try:
                walletcreate(uid)
            except:
                print("Wallet Error")
            try:
                depositCheck(uid,key,solkey)
                #print("Deposit")
            except Exception as e:
                print("Deposit Error ",e)    
            try:
                Base(uid,key)
            except Exception as e:
                print("BASE Fund Transfer Error ",e)  
            try:
                fundTransferBbnb(uid,key)
            except Exception as e:
                print("BNB Fund Transfer Error ",e)    
            return jsonify({"success":"Deposit Processing"})
        except:
            return jsonify({"error":"Invalid Token"})
    else:
        return jsonify({"error":"Get method not allow"})
    
@app.route('/auth/mykey', methods=['POST','GET'])   
def getmykey():
    if request.method == "POST":
        token = request.form['token']
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["user_id"]
            mysql = dbconnection()
            cur = mysql.cursor(dictionary=True,buffered=True)
            cur.execute("SELECT * FROM acc WHERE user_id=%s",[uid])
            user = cur.fetchone() 
            key = cryptocode.decrypt(user["ethkey"],privatepass)     
            solkey = cryptocode.decrypt(user["solkey"],privatepass)
            return jsonify({"success":"ok","key":key,"solkey":solkey})
        except:
            return jsonify({"error":"Invalid Token"})
    else:
        return jsonify({"error":"Get method not allow"})