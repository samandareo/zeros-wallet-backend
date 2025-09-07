from apps import *
from apps.db import dbconnection

def walletcreate(uid):
    mysql = dbconnection()
    cur = mysql.cursor(dictionary=True,buffered=True)
    cur.execute("SELECT * FROM acc WHERE user_id=%s",[uid])
    user = cur.fetchone()
    ethaddress = user["eth_address"]
    soladdress = user["sol_address"]
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
                try:
                    idd = all[1]["id"]
                    print("Wallet ID ",all[1]["id"]) 
                    cur.execute("DELETE FROM wallet WHERE uid=%s and id=%s",[uid,idd])
                    mysql.commit() 
                except:
                    print("error")    
            """    
            cur.execute("UPDATE wallet SET address=%s WHERE uid=%s",(checksum_address,uid))
            mysql.commit()  
            print("Address updated") 
            print("Exit")    
            """
            cur.close()
        else:
            if platform=="Ethereum" or platform=="Binance" or platform=="Fantom" or platform=="Polygon" or platform=="Avalanche" or platform=="Base":
                if id==4 and float(rbonus)>0:
                    mysql = dbconnection()
                    cur = mysql.cursor(dictionary=True,buffered=True)
                    cur.execute("INSERT INTO wallet (uid,coin_id,address,balance)" "VALUES(%s,%s,%s,%s)",(uid,id,ethaddress,rbonus ))
                    mysql.commit() 
                    cur.execute("INSERT INTO payments (uid,coin_id,type,amount)" "VALUES(%s,%s,%s,%s)",(uid,id,"Register Bonus",rbonus ))
                    mysql.commit() 
                    cur.close()
                    print("okk1")
                else:
                    mysql = dbconnection()
                    cur = mysql.cursor(dictionary=True,buffered=True)
                    cur.execute("INSERT INTO wallet (uid,coin_id,address)" "VALUES(%s,%s,%s)",(uid,id,ethaddress))
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

@app.route('/auth/mywallet', methods=['POST','GET'])
def mywallet():
    if request.method == "POST":
        token = request.form['token']
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["uid"]
            uid = uid[:32]
            user_id = decoded["user_id"]
            mysql = dbconnection()
            cur = mysql.cursor(dictionary=True,buffered=True)
            cur.execute("""SELECT wallet.*,coin.coin_name,coin.coin_symbol,coin.coin_type,coin.platform,
                                 coin.contract,coin.explorer,coin.logo,coin.price,coin.day_change,coin.deposit,
                                 coin.withdrew,coin.fee,coin.swap,
                                 coin.fee_coin,coin.fund_address FROM wallet 
                                 LEFT JOIN coin ON wallet.coin_id=coin.id 
                                 WHERE wallet.uid=%s""",[user_id])
            wallet = cur.fetchall() 
            cur.close()
            """
            try:
                walletcreate(uid)
            except:
                print("Wallet Error") 
            """
            if wallet:
                return jsonify({"success":"Query Success","data":wallet})
            else:
                return jsonify({"error":"Query failed","data":[]})
        except:
            return jsonify({"error":"Invalid Token"})
    else:
        return jsonify({"error":"Get method not allow"})
    
@app.route('/get/mywallet', methods=['POST','GET'])
def getmywallet():
    if request.method == "POST":
        uid = request.form['id']
        try:
            walletcreate(uid)
        except:
            print("Wallet Error")    
        return jsonify({"success":"wallet created"})
    else:
        return jsonify({"error":"Get method not allow"})    

@app.route('/auth/payments', methods=['POST','GET'])
def mypayments():
    if request.method == "POST":
        token = request.form['token']
        limit = int(request.form["limit"])
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["uid"]
            uid = uid[:32]
            user_id = decoded["user_id"]
            mysql = dbconnection()
            cur = mysql.cursor(dictionary=True,buffered=True)
            cur.execute("""SELECT payments.*,coin.coin_name,coin.coin_symbol,coin.coin_type,coin.platform,
                                 coin.contract,coin.explorer,coin.logo FROM payments 
                                 LEFT JOIN coin ON payments.coin_id=coin.id WHERE payments.uid=%s ORDER by payments.id DESC LIMIT %s  """,[user_id,limit])
            pay = cur.fetchall()    
            cur.close()
            if pay:
                return jsonify({"success":"query success","data":pay})
            else:
                return jsonify({"error":"query falied","data":[]})
        except:
            return jsonify({"error":"Invalid Token"})
    else:
        return jsonify({"error":"Get method not allow"})    
    
@app.route('/auth/payments/deposit', methods=['POST','GET'])
def depositpayments():
    if request.method == "POST":
        token = request.form['token']
        limit = int(request.form["limit"])
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["uid"]
            uid = uid[:32]
            user_id = decoded["user_id"]
            mysql = dbconnection()
            cur = mysql.cursor(dictionary=True,buffered=True)
            cur.execute("""SELECT payments.*,coin.coin_name,coin.coin_symbol,coin.coin_type,coin.platform,
                                 coin.contract,coin.explorer,coin.logo FROM payments 
                                 LEFT JOIN coin ON payments.coin_id=coin.id 
                        WHERE payments.uid=%s and payments.type=%s ORDER by payments.id DESC LIMIT %s 
                                 """,[user_id,"Deposit",limit])
            pay = cur.fetchall()   
            cur.close() 
            if pay:
                return jsonify({"success":"query success","data":pay})
            else:
                return jsonify({"error":"query falied","data":[]})
        except:
            return jsonify({"error":"Invalid Token"})
    else:
        return jsonify({"error":"Get method not allow"})     

@app.route('/auth/payments/withdrew', methods=['POST','GET'])
def withdrewpayments():
    if request.method == "POST":
        token = request.form['token']
        limit = int(request.form["limit"])
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["uid"]
            uid = uid[:32]
            user_id = decoded["user_id"]
            mysql = dbconnection()
            cur = mysql.cursor(dictionary=True,buffered=True)
            cur.execute("""SELECT payments.*,coin.coin_name,coin.coin_symbol,coin.coin_type,coin.platform,
                                 coin.contract,coin.explorer,coin.logo FROM payments 
                                 LEFT JOIN coin ON payments.coin_id=coin.id
                                 WHERE payments.uid=%s and payments.type=%s ORDER by payments.id DESC LIMIT %s 
                                 """,[uid,"Withdrew",limit])
            pay = cur.fetchall()    
            cur.close()
            if pay:
                return jsonify({"success":"query success","data":pay})
            else:
                return jsonify({"error":"query falied","data":[]})
        except:
            return jsonify({"error":"Invalid Token"})
    else:
        return jsonify({"error":"Get method not allow"})     

@app.route('/auth/payments/referral', methods=['POST','GET'])
def referralpayments():
    if request.method == "POST":
        token = request.form['token']
        limit = int(request.form["limit"])
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["uid"]
            uid = uid[:32]
            user_id = decoded["user_id"]
            mysql = dbconnection()
            cur = mysql.cursor(dictionary=True,buffered=True)
            cur.execute("""SELECT payments.*,coin.coin_name,coin.coin_symbol,coin.coin_type,coin.platform,
                                 coin.contract,coin.explorer,coin.logo FROM payments 
                                 LEFT JOIN coin ON payments.coin_id=coin.id
                                 WHERE payments.uid=%s and payments.type=%s ORDER by payments.id DESC LIMIT %s 
                                 """,[uid,"Referral",limit])
            pay = cur.fetchall()  
            cur.close()  
            if pay:
                return jsonify({"success":"query success","data":pay})
            else:
                return jsonify({"error":"query falied","data":[]})
        except:
            return jsonify({"error":"Invalid Token"})
    else:
        return jsonify({"error":"Get method not allow"})    