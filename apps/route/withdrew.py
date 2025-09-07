from apps import *
from apps.db import dbconnection
import os

@app.route('/auth/withdrew', methods=['POST','GET'])
def authwithdrew():
    if request.method == "POST":
        token = request.form['token']
        id = request.form['id']
        amount = request.form['amount']
        toid = request.form['toid']

        if re.search("['^£$%&*()}{@#~?><>.+|=_¬-]", id):
            return jsonify({"error":"Invalid Coin"})
        if re.search("['^£$%&*()}{@#~?><>+|=_¬-]", amount):
            return jsonify({"error":"Invalid Amount"})
        if re.search("['^£$%&*()}{@#~?><>.+|=_¬-]", toid):
            return jsonify({"error":"Invalid Address"})      
        print(len(toid))
        if len(toid)<42:
            return jsonify({"error":"Invalid Address"})
        print(toid)
        mysql = dbconnection()
        cur = mysql.cursor(dictionary=True,buffered=True)
        cur.execute("SELECT * FROM coin WHERE id=%s",[id])
        coin = cur.fetchone()
        fee = coin["fee"]
        fee_coin = coin["fee_coin"]
        withdrew = coin["withdrew"]
        if withdrew=="0":
            return jsonify({"error":"Currently Withdrawal disabled"})         
        try:            
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["user_id"]
            cur.execute("SELECT * FROM wallet WHERE uid=%s and coin_id=%s",[uid,id])
            wallet = cur.fetchone()
            bal = wallet["balance"]
            
            if id==fee_coin or fee_coin=="" or fee_coin==None:
                totalamount =float(fee)+float(amount)
                if float(bal)>=float(totalamount):
                    try:
                        mysql.autocommit = True
                        mysql.start_transaction()
                        cur.execute("UPDATE wallet SET balance=balance - %s WHERE uid=%s and coin_id=%s",(totalamount ,uid,id))
                        cur.execute("INSERT INTO payments (uid,coin_id,type,amount,status,toid)" "VALUES(%s,%s,%s,%s,%s,%s)",(uid,id,"Withdrew",amount,"Pending",toid ))
                        mysql.commit()
                        return jsonify({"success":"Your withdrew request successfully submitted"})
                    except mysql.connector.Error as error:
                        mysql.rollback()  
                        cur.close()
                        mysql.close()
                        return jsonify({"success":"Oh Something went wrong"})
                else:
                    print(bal)
                    return jsonify({"error":"Balance not enough"})    
            else:
                cur.execute("SELECT * FROM wallet WHERE uid=%s and coin_id=%s",[uid,fee_coin])
                wallet1 = cur.fetchone()
                feebal = wallet1["balance"]
                if float(feebal)>=float(fee) and float(bal)>=float(amount):
                    try:
                        mysql.autocommit = True
                        mysql.start_transaction()
                        cur.execute("UPDATE wallet SET balance=balance - %s WHERE uid=%s and coin_id=%s",(amount ,uid,id))
                        cur.execute("UPDATE wallet SET balance=balance - %s WHERE uid=%s and coin_id=%s",(fee ,uid,fee_coin))
                        cur.execute("INSERT INTO payments (uid,coin_id,type,amount,status,toid)" "VALUES(%s,%s,%s,%s,%s,%s)",(uid,id,"Withdrew",amount,"Pending",toid ))
                        mysql.commit()
                        return jsonify({"success":"Your withdrew request successfully submitted"})
                    except mysql.connector.Error as error:
                        mysql.rollback()  
                        cur.close()
                        mysql.close()
                        return jsonify({"success":"Oh Something went wrong"})
                else:
                    return jsonify({"error":"Balance not enough"})    
        except:
            return jsonify({"error":"Invalid Token"})
    else:
        return jsonify({"error":"Get method not allow"})
    

@app.route('/withdrew/confirm', methods=['POST','GET'])
def confirmwithdrew():
    if request.method == "POST":
        token = request.form['token']
        id = request.form['id']
        status = request.form['status']
        fromid = request.form['fromid']
        trx = request.form['trx']

        mysql = dbconnection()
        cur = mysql.cursor(dictionary=True,buffered=True)
        cur.execute("SELECT * FROM payments WHERE id=%s",[id])
        pay = cur.fetchone()
        coin_id = pay["coin_id"]
        uuid = pay["uid"]
        amount = pay["amount"]
        statuses = pay["status"]
        type = pay["type"]

        cur.execute("SELECT * FROM coin WHERE id=%s",[coin_id])
        coin = cur.fetchone()
        fee = coin["fee"]
        fee_coin = coin["fee_coin"]
        
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["user_id"]
            cur.execute("SELECT * FROM keystore WHERE id=%s",[uid])
            user = cur.fetchone()
            if user["type"]=="Admin":
                if statuses=="Pending" and type=="Withdrew":
                    if status=="Pending":
                        return jsonify({"error":"Change your status"}) 
                    if status=="Success":
                        try:
                            mysql.autocommit = True
                            mysql.start_transaction()
                            query=( "Success",fromid,trx,id)
                            cur.execute("UPDATE payments SET status=%s,fromid=%s,trx=%s WHERE id=%s",query)
                            mysql.commit()
                            return jsonify({"success":"Payment status successfully updated"}) 
                        except mysql.connector.Error as error:
                            mysql.rollback() 
                            cur.close()
                            mysql.close()  
                            return jsonify({"success":"Payment status not updated"})
                    if status=="Rejected":
                        if coin_id==fee_coin or fee_coin=="" or fee_coin==None:
                            try:
                                mysql.autocommit = True
                                mysql.start_transaction()
                                total = float(amount)+float(fee)
                                cur.execute("UPDATE wallet SET balance=balance + %s WHERE uid=%s and coin_id=%s",(total ,uuid,coin_id))
                                query=( "Rejected",fromid,trx,id)
                                cur.execute("UPDATE payments SET status=%s,fromid=%s,trx=%s WHERE id=%s",query)
                                mysql.commit()
                                return jsonify({"success":"Payment status successfully updated"})
                            except mysql.connector.Error as error:
                                mysql.rollback()  
                                cur.close()
                                mysql.close()   
                                return jsonify({"success":"Payment status not updated"})
                        else:
                            try:
                                mysql.autocommit = True
                                mysql.start_transaction()
                                cur.execute("UPDATE wallet SET balance=balance + %s WHERE uid=%s and coin_id=%s",(amount ,uuid,coin_id))
                                cur.execute("UPDATE wallet SET balance=balance + %s WHERE uid=%s and coin_id=%s",(fee ,uuid,fee_coin))
                                query=( "Rejected",fromid,trx,id)
                                cur.execute("UPDATE payments SET status=%s,fromid=%s,trx=%s WHERE id=%s",query)
                                mysql.commit()
                                return jsonify({"success":"Payment status successfully updated"})
                            except mysql.connector.Error as error:
                                mysql.rollback()   
                                cur.close()
                                mysql.close()  
                                return jsonify({"success":"Payment status not updated"})
                else:
                    return jsonify({"error":"Pending Status changable"})    
            else:
                return jsonify({"error":"Admin access only"})    
        except:
            return jsonify({"error":"Invalid Token"})
    else:
        return jsonify({"error":"Get method not allow"})    
    
   
@app.route('/admin/balanceadjust', methods=['POST','GET'])
def balanceadjust():
    if request.method == "POST":
        token = request.form['token']
        amount = request.form['amount']
        id = request.form['id']
        coin_id = request.form['coin_id']
        type = request.form['type']
        trx = request.form['trx']
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["user_id"]
            mysql = dbconnection()
            cur = mysql.cursor(dictionary=True,buffered=True)
            cur.execute("SELECT * FROM keystore WHERE id=%s",[uid])
            user = cur.fetchone()
            if user["type"]=="Admin":
                if type=="Increment":
                    try:
                        mysql.autocommit = True
                        mysql.start_transaction()
                        cur.execute("UPDATE wallet SET balance=balance + %s WHERE uid=%s and coin_id=%s",(amount ,id,coin_id))
                        if trx!="":
                            cur.execute("INSERT INTO payments (uid,coin_id,type,amount,status,trx)" "VALUES(%s,%s,%s,%s,%s,%s)",(id,coin_id,"Deposit",amount,"Success",trx ))
                            mysql.commit()
                        mysql.commit()
                        return jsonify({"success":"Balance updated Successfully"})
                    except mysql.connector.Error as error:
                        mysql.rollback()
                        cur.close()
                        mysql.close()
                        return jsonify({"success":"Something went wrong"})
                if type=="Decrement":
                    try:
                        mysql.autocommit = True
                        mysql.start_transaction()
                        cur.execute("UPDATE wallet SET balance=balance - %s WHERE uid=%s and coin_id=%s",(amount ,id,coin_id))
                        if trx!="":
                            cur.execute("INSERT INTO payments (uid,coin_id,type,amount,status,trx)" "VALUES(%s,%s,%s,%s,%s,%s)",(id,coin_id,"Withdrew",amount,"Success",trx ))
                            mysql.commit()
                        mysql.commit()    
                        return jsonify({"success":"Balance updated Successfully"})
                    except mysql.connector.Error as error:
                        mysql.rollback()
                        cur.close()
                        mysql.close()
                        return jsonify({"success":"Something went wrong"})
                return jsonify({"error":"Balance Adjust Type is required"}) 
            else:
                return jsonify({"error":"Admin access only"}) 

        except:
            return jsonify({"error":"Invalid Token"})
    else:
        return jsonify({"error":"Get method not allow"})     