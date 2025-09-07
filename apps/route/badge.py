from apps import *
from apps.db import dbconnection
import os

@app.route("/addbadge", methods=['GET', 'POST'])
def addbadge():
    if request.method == "POST":
        token = request.form['token']
        amount = request.form['amount']
        coin_id = request.form['coin_id']
        mysql = dbconnection()
        cur = mysql.cursor(dictionary=True,buffered=True)
        if coin_id=="":
             return jsonify({"error":"Coin is required"})
        if amount=="":
             return jsonify({"error":"Amount is required"})       
        if float(amount)<1:
             return jsonify({"error":"Minimum amount is $1"})     
        if float(amount)>500:
             return jsonify({"error":"Maximum amount is $500"}) 
        cur.execute("SELECT * FROM coin WHERE id=%s",[coin_id])
        data = cur.fetchone()
        price = float(data["price"])
        name = data["coin_symbol"]
        aa = 1/price
        eth = float(amount)*aa
        print(price)
        print(aa)
        print(eth)

        bonus = float(amount)*200
        print(bonus)
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["user_id"]
            cur.execute("SELECT * FROM wallet WHERE uid=%s and coin_id=%s",[uid,coin_id])
            wallet = cur.fetchone()
            bal = wallet["balance"] 
            cur.execute("SELECT * FROM keystore WHERE id=%s",[uid])
            user = cur.fetchone()
            address = user["ethaddress"]
            if user["badge"]=="Yes":
                return jsonify({"error":"You are already premium user"}) 

            if float(bal)>=float(eth):
                amount = float(amount)
                try:     
                    mysql.autocommit = True
                    mysql.start_transaction()
                    cur.execute("UPDATE wallet SET balance=balance - %s WHERE uid=%s and coin_id=%s",(eth ,uid,coin_id))
                    cur.execute("UPDATE wallet SET balance=balance + %s WHERE uid=%s and coin_id=%s",(bonus ,uid,"5"))
                    cur.execute("UPDATE keystore SET badge=%s WHERE id=%s",("Yes" ,uid))
                    cur.execute("INSERT INTO badgetrx (uid,address,amount,xzeros)" 
                                 "VALUES(%s,%s,%s,%s)",
                                 (uid,address,amount,bonus))
                    mysql.commit()
                    cur.close()
                    mysql.close()
                    return jsonify({"success":"Premium Badge Added successfully"}) 
                except:
                    mysql.rollback()
                    return jsonify({"error":"Premium Badge not success try again"})
            else:
                return jsonify({"error":name+" Balance not enough"}) 
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"})    

@app.route("/mybadge", methods=['GET', 'POST'])
def mybadge():
    if request.method == "POST":
        token = request.form['token']
        mysql = dbconnection()
        cur = mysql.cursor(dictionary=True,buffered=True)
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["user_id"]
            cur.execute("SELECT * FROM keystore WHERE id=%s",[uid])
            user = cur.fetchone()
            if user["badge"]=="Yes":
                return jsonify({"error":"Success","badge":"Yes"}) 
            else:
                return jsonify({"error":"Success","badge":"No"}) 

        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"})        
    
@app.route("/mybadgetrx", methods=['GET', 'POST'])
def mybadgetrx():
    if request.method == "POST":
        token = request.form['token']
        mysql = dbconnection()
        cur = mysql.cursor(dictionary=True,buffered=True)
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["user_id"]
            cur.execute("SELECT * FROM badgetrx WHERE uid=%s",[uid])
            trx = cur.fetchall()
            if trx:
                return jsonify({"success":"Query Success","trx":trx}) 
            else:
                return jsonify({"error":"Query Success","trx":[]}) 

        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"}) 
    
@app.route("/all-badge", methods=['GET', 'POST'])
def allbadge():   
    mysql = dbconnection()
    cur = mysql.cursor(dictionary=True,buffered=True)
    cur.execute("SELECT * FROM badgetrx ORDER BY amount DESC LIMIT 10")
    badge = cur.fetchall()
    cur.close()
    mysql.close()
    if badge:
        return jsonify({"success":"ok","data":badge})
    else:
        return({"error":"ok","data":[]})     