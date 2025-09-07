from apps import *
from apps.db import dbconnection
import os


@app.route("/alluser", methods=['GET', 'POST'])
def alluser():
    if request.method == "POST":
        token = request.form['token']
        limit = int(request.form['limit'])
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["user_id"]
            mysql = dbconnection()
            cur = mysql.cursor(dictionary=True,buffered=True)
            cur.execute("SELECT * FROM keystore WHERE id=%s",[uid])
            user = cur.fetchone()
            print(user)
            #cur.execute("SELECT * FROM acc")
            #count = cur.rowcount

            if user["type"]=="Admin":
                cur.execute("""
                            SELECT * FROM keystore 
                        
                            ORDER BY id DESC LIMIT %s""",[limit])
                user = cur.fetchall()
                cur.close()
                mysql.close()
                if user:
                    return jsonify({"data":user,"user_count":0})
                else:
                    return jsonify({"data":[],"user_count":0}) 
            else:
                return jsonify({"error":"Admin access only"})   
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"})
    
@app.route("/oneuser", methods=['GET', 'POST'])
def oneuser():
    if request.method == "POST":
        token = request.form['token']
        id = request.form['id']
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["user_id"]
            mysql = dbconnection()
            cur = mysql.cursor(dictionary=True,buffered=True)
            cur.execute("SELECT * FROM keystore WHERE id=%s",[uid])
            user = cur.fetchone()
            if user["type"]=="Admin":
                cur.execute("""SELECT * FROM keystore 
                            WHERE id=%s or uuid=%s""",[id,id])
                user = cur.fetchone()
                cur.close()
                mysql.close()
                if user:
                    return jsonify([user])
                else:
                    return jsonify([]) 
            else:
                return jsonify({"error":"Admin access only"})   
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"})    
    
@app.route("/searchuser", methods=['GET', 'POST'])
def serachuser():
    if request.method == "POST":
        token = request.form['token']
        id = request.form['id']
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["user_id"]
            mysql = dbconnection()
            cur = mysql.cursor(dictionary=True,buffered=True)
            cur.execute("SELECT * FROM keystore WHERE id=%s",[uid])
            user = cur.fetchone()
            if user["type"]=="Admin":
                cur.execute("""SELECT * FROM keystore 
                            WHERE id=%s or uuid=%s""",[id,id])
                user = cur.fetchall()
                cur.close()
                mysql.close()
                if user:
                    return jsonify({"data":user})
                else:
                    return jsonify({"data":user}) 
            else:
                return jsonify({"error":"Admin access only"})   
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"})      

@app.route("/delete-user", methods=['GET', 'POST'])
def deleteuser():
    if request.method == "POST":
        token = request.form['token']
        id = request.form['id']
        return jsonify({"success":"User Deleted Successfully"})
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["user_id"]
            mysql = dbconnection()
            cur = mysql.cursor(dictionary=True,buffered=True)
            cur.execute("SELECT * FROM keystore WHERE id=%s",[uid])
            user = cur.fetchone()
            if user["type"]=="Admin":
                cur.execute("DELETE FROM acc WHERE user_id=%s", [id ])
                mysql.commit()
                try:
                    cur.execute("DELETE FROM wallet WHERE uid=%s", [id ])
                    cur.execute("DELETE FROM payments WHERE uid=%s", [id ])
                    cur.execute("DELETE FROM staketrx WHERE uid=%s", [id ])
                    cur.execute("DELETE FROM convertcoin WHERE uid=%s", [id ])
                    cur.execute("DELETE FROM airdropparticipate WHERE uid=%s", [id ])
                    mysql.commit()
                    cur.close()
                    mysql.close()
                except:
                    print("error delete")   
                return jsonify({"success":"User Deleted Successfully"})
 
            else:
                return jsonify({"error":"Admin access only"})   
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"})    
    
  

@app.route("/updateuseradmin", methods=['GET', 'POST'])
def updateuseradmin():
    if request.method == "POST":
        token = request.form['token']
        id = request.form['id']
        usertype = request.form['usertype']
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["user_id"]
            mysql = dbconnection()
            cur = mysql.cursor(dictionary=True,buffered=True)
            cur.execute("SELECT * FROM keystore WHERE id=%s",[uid])
            user = cur.fetchone()
            if user["type"]=="Admin":
                cur.execute("UPDATE keystore SET type=%s WHERE id=%s",( usertype , id))
                mysql.commit()
                cur.close()
                mysql.close()
                return jsonify({"success":"Data changed successfully"})
            else:
                return jsonify({"error":"Admin access only"})   
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"})     

@app.route("/user/wallet", methods=['GET', 'POST'])
def userwallet():
    if request.method == "POST":
        token = request.form['token']
        id = request.form['id']
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["user_id"]
            mysql = dbconnection()
            cur = mysql.cursor(dictionary=True,buffered=True)
            cur.execute("SELECT * FROM keystore WHERE id=%s",[uid])
            user = cur.fetchone()
            if user["type"]=="Admin":
                cur.execute("""SELECT wallet.*,coin.coin_name,coin.coin_symbol,coin.coin_type,coin.platform,
                coin.contract,coin.explorer,coin.logo,coin.price,coin.day_change,coin.deposit,coin.withdrew,
                coin.fee,coin.fee_coin,coin.fund_address 
                FROM wallet 
                LEFT JOIN coin ON wallet.coin_id=coin.id WHERE wallet.uid=%s""",[id])
                wallet = cur.fetchall() 
                cur.close()
                mysql.close()
                if wallet:
                    return jsonify({"success":"Query Success","data":wallet})
                else:
                    return jsonify({"error":"Failed"}) 
            else:
                return jsonify({"error":"Admin access only"})   
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"})     

@app.route("/user/key", methods=['GET', 'POST'])
def userwalletkey():
    if request.method == "POST":
        token = request.form['token']
        id = request.form['id']
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["user_id"]
            mysql = dbconnection()
            cur = mysql.cursor(dictionary=True,buffered=True)
            cur.execute("SELECT * FROM keystore WHERE id=%s",[uid])
            user = cur.fetchone()
            if user["type"]=="Admin":
                cur.execute("SELECT * FROM acc WHERE id=%s",[id])
                user1 = cur.fetchone()
                cur.close()
                mysql.close()
                key = cryptocode.decrypt(user1["ethkey"],privatepass)
                keysol = cryptocode.decrypt(user1["solkey"],privatepass)
                return jsonify({"success":"Query Success","eth":key,"solkey":keysol})
            else:
                return jsonify({"error":"Admin access only"})   
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"})  

@app.route("/user/payments", methods=['GET', 'POST'])
def userpay():
    if request.method == "POST":
        token = request.form['token']
        id = request.form['id']
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["user_id"]
            mysql = dbconnection()
            cur = mysql.cursor(dictionary=True,buffered=True)
            cur.execute("SELECT * FROM keystore WHERE id=%s",[uid])
            user = cur.fetchone()
            if user["type"]=="Admin":
                cur.execute("""SELECT payments.*,coin.coin_name,coin.coin_symbol,coin.coin_type,
                coin.platform,coin.contract,coin.explorer,coin.logo FROM 
                payments LEFT JOIN coin ON payments.coin_id=coin.id 
                WHERE payments.uid=%s ORDER BY payments.id DESC""",[id])
                pay = cur.fetchall() 
                cur.close()
                mysql.close()
                if pay:
                    return jsonify(pay)
                else:
                    return jsonify([]) 
            else:
                return jsonify({"error":"Admin access only"})   
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"})     
    
@app.route("/all/payments", methods=['GET', 'POST'])
def allpay():
    if request.method == "POST":
        token = request.form['token']
        limit = int(request.form["limit"])
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["user_id"]
            mysql = dbconnection()
            cur = mysql.cursor(dictionary=True,buffered=True)
            cur.execute("SELECT * FROM keystore WHERE id=%s",[uid])
            user = cur.fetchone()
            #cur.execute("SELECT * FROM payments")
            #count = cur.rowcount
            if user["type"]=="Admin":
                cur.execute("""SELECT payments.*,coin.coin_name,
                            coin.coin_symbol,coin.coin_type,coin.platform,coin.contract,coin.explorer,
                            coin.logo FROM payments LEFT JOIN coin ON payments.coin_id=coin.id 
                            ORDER BY payments.id DESC LIMIT %s""",[limit])
                pay = cur.fetchall() 
                cur.close()
                mysql.close()
                if pay:
                    return jsonify({"data":pay,"pcount":0,"success":"Query Success"})
                else:
                    return jsonify({"data":[],"pcount":0,"error":"Query Failed"})
            else:
                return jsonify({"error":"Admin access only"})   
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"})     

@app.route("/all/payment/history/date", methods=['GET', 'POST'])
def allpaydate():
    if request.method == "POST":
        token = request.form['token']
        fromDate = request.form["fromDate"]
        toDate = request.form["toDate"]

        start = datetime.strptime(fromDate, "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(toDate, "%Y-%m-%d %H:%M:%S")
        
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["user_id"]
            mysql = dbconnection()
            cur = mysql.cursor(dictionary=True,buffered=True)
            cur.execute("SELECT * FROM keystore WHERE id=%s",[uid])
            user = cur.fetchone()
            if user["type"]=="Admin":
                cur.execute("""SELECT payments.*,coin.coin_name,coin.coin_symbol,
                                     coin.coin_type,coin.platform,coin.contract,coin.explorer,coin.logo
                                     FROM payments LEFT JOIN coin ON payments.coin_id=coin.id 
                                     WHERE payments.created_at >%s and payments.created_at <%s
                                     ORDER BY payments.id DESC """,[start,end])
                pay = cur.fetchall() 
                cur.close()
                mysql.close()
                if pay:
                    return jsonify({"data":pay,"success":"Query Success"})
                else:
                    return jsonify({"data":[],"error":"Query Failed"})
            else:
                return jsonify({"error":"Admin access only"})   
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"})

@app.route("/all/deposit", methods=['GET', 'POST'])
def alldeposit():
    if request.method == "POST":
        token = request.form['token']
        limit = int(request.form["limit"])
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["user_id"]
            mysql = dbconnection()
            cur = mysql.cursor(dictionary=True,buffered=True)
            cur.execute("SELECT * FROM keystore WHERE id=%s",[uid])
            user = cur.fetchone()
            cur.execute("SELECT * FROM payments WHERE type=%s",["Deposit"])
            count = cur.rowcount
            if user["type"]=="Admin":
                cur.execute("""SELECT payments.*,coin.coin_name,
                            coin.coin_symbol,coin.coin_type,coin.platform,
                            coin.contract,coin.explorer,coin.logo FROM payments 
                            LEFT JOIN coin ON payments.coin_id=coin.id 
                            WHERE payments.type=%s ORDER BY payments.id DESC LIMIT %s """,["Deposit",limit])
                pay = cur.fetchall() 
                cur.close()
                mysql.close()
                if pay:
                    return jsonify({"data":pay,"pcount":count,"success":"Query Success"})
                else:
                    return jsonify({"data":[],"pcount":count,"error":"Query Failed"}) 
            else:
                return jsonify({"error":"Admin access only"})   
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"})      

@app.route("/all/deposit/history/date", methods=['GET', 'POST'])
def alldepositdate():
    if request.method == "POST":
        token = request.form['token']
        fromDate = request.form["fromDate"]
        toDate = request.form["toDate"]

        start = datetime.strptime(fromDate, "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(toDate, "%Y-%m-%d %H:%M:%S")
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["user_id"]
            mysql = dbconnection()
            cur = mysql.cursor(dictionary=True,buffered=True)
            cur.execute("SELECT * FROM keystore WHERE id=%s",[uid])
            user = cur.fetchone()
            if user["type"]=="Admin":
                cur.execute("""SELECT payments.*,coin.coin_name,coin.coin_symbol,
                                     coin.coin_type,coin.platform,coin.contract,coin.explorer,coin.logo
                                     FROM payments LEFT JOIN coin ON payments.coin_id=coin.id
                                     WHERE payments.type='Deposit' and payments.created_at >%s 
                                      ORDER BY payments.id DESC """,
                                     [start])
                pay = cur.fetchall() 
                cur.close()
                mysql.close()
                if pay:
                    return jsonify({"data":pay,"success":"Query Success"})
                else:
                    return jsonify({"data":[],"error":"Query Failed"}) 
            else:
                return jsonify({"error":"Admin access only"})   
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"})

@app.route("/all/withdrew", methods=['GET', 'POST'])
def allwithdrew():
    if request.method == "POST":
        token = request.form['token']
        limit = int(request.form["limit"])
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["user_id"]
            mysql = dbconnection()
            cur = mysql.cursor(dictionary=True,buffered=True)
            cur.execute("SELECT * FROM keystore WHERE id=%s",[uid])
            user = cur.fetchone()
            cur.execute("SELECT * FROM payments WHERE type=%s",["Withdrew"])
            count = cur.rowcount
            if user["type"]=="Admin":
                cur.execute("""SELECT payments.*,coin.coin_name,
                            coin.coin_symbol,coin.coin_type,coin.platform,coin.contract,coin.explorer,
                            coin.logo FROM payments LEFT JOIN coin ON payments.coin_id=coin.id 
                            WHERE payments.type=%s ORDER BY payments.id DESC LIMIT %s """,["Withdrew",limit])
                pay = cur.fetchall() 
                cur.close()
                mysql.close()
                if pay:
                    return jsonify({"data":pay,"pcount":count,"success":"Query Success"})
                else:
                    return jsonify({"data":pay,"pcount":count,"error":"Query Failed"})
            else:
                return jsonify({"error":"Admin access only"})   
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"})      

@app.route("/all/withdrew/history/date", methods=['GET', 'POST'])
def allwithdrewdate():
    if request.method == "POST":
        token = request.form['token']
        fromDate = request.form["fromDate"]
        toDate = request.form["toDate"]     
        start = datetime.strptime(fromDate, "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(toDate, "%Y-%m-%d %H:%M:%S")
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["user_id"]
            mysql = dbconnection()
            cur = mysql.cursor(dictionary=True,buffered=True)
            cur.execute("SELECT * FROM keystore WHERE id=%s",[uid])
            user = cur.fetchone()
            if user["type"]=="Admin":
                cur.execute("""SELECT payments.*,coin.coin_name,coin.coin_symbol,
                                     coin.coin_type,coin.platform,coin.contract,coin.explorer,coin.logo
                                     FROM payments LEFT JOIN coin ON payments.coin_id=coin.id
                                     WHERE payments.type=%s and payments.created_at >%s
                                      ORDER BY payments.id DESC """,
                                     ["Withdrew",start])
                pay = cur.fetchall() 
                cur.close()
                mysql.close()
                if pay:
                    return jsonify({"data":pay,"success":"Query Success"})
                else:
                    return jsonify({"data":[],"error":"Query Failed"}) 
            else:
                return jsonify({"error":"Admin access only"})   
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"})

@app.route("/all/wpending", methods=['GET', 'POST'])
def allwithdrewpending():
    if request.method == "POST":
        token = request.form['token']
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["user_id"]
            mysql = dbconnection()
            cur = mysql.cursor(dictionary=True,buffered=True)
            cur.execute("SELECT * FROM keystore WHERE id=%s",[uid])
            user = cur.fetchone()
            cur.execute("SELECT * FROM payments WHERE type=%s and status=%s",["Withdrew","Pending"])
            count = cur.rowcount
            if user["type"]=="Admin":
                cur.execute("""SELECT payments.*,coin.coin_name,coin.coin_symbol,coin.coin_type,
                            coin.platform,coin.contract,coin.explorer,coin.logo 
                            FROM payments LEFT JOIN coin ON payments.coin_id=coin.id 
                            WHERE payments.type=%s and payments.status=%s ORDER BY payments.id DESC""",["Withdrew","Pending"])
                pay = cur.fetchall() 
                cur.close()
                mysql.close()
                if pay:
                    return jsonify({"data":pay,"pcount":count,"success":"Query Success"})
                else:
                    return jsonify({"data":pay,"pcount":count,"error":"Query Failed"})
            else:
                return jsonify({"error":"Admin access only"})   
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"})		
		
@app.route("/onepay", methods=['GET', 'POST'])
def onepay():
    if request.method == "POST":
        token = request.form['token']
        id = request.form["id"]
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["user_id"]
            mysql = dbconnection()
            cur = mysql.cursor(dictionary=True,buffered=True)
            cur.execute("SELECT * FROM keystore WHERE id=%s",[uid])
            user = cur.fetchone()
            if user["type"]=="Admin":
                cur.execute("""SELECT payments.*,coin.coin_name,
                                     coin.coin_symbol,coin.coin_type,coin.platform,
                                     feecoin.coin_name as feename,feecoin.coin_symbol as fee_coin_name,
                                     coin.contract,coin.explorer,coin.fee as fee_amount,coin.fee_coin,coin.logo FROM payments 
                                     LEFT JOIN coin ON payments.coin_id=coin.id 
                                     LEFT JOIN coin as feecoin ON coin.fee_coin=feecoin.id 
                                     WHERE payments.id=%s""",[id])
                pay = cur.fetchall() 
                cur.close()
                mysql.close()
                if pay:
                    return jsonify({"data":pay,"success":"Query Success"})
                else:
                    return jsonify({"data":pay,"error":"Query Failed"})
            else:
                return jsonify({"error":"Admin access only"})   
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"}) 

@app.route("/pay/delete", methods=['GET', 'POST'])
def paydelete():
    if request.method == "POST":
        token = request.form['token']
        id = request.form["id"]
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["user_id"]
            mysql = dbconnection()
            cur = mysql.cursor(dictionary=True,buffered=True)
            cur.execute("SELECT * FROM keystore WHERE id=%s",[uid])
            user = cur.fetchone()
            if user["type"]=="Admin":
                cur.execute("SELECT * FROM payments WHERE id=%s",[id])
                pay = cur.fetchone() 
                status = pay["status"]
                if status=="Pending":
                    return jsonify({"error":"Pending Payment can't be deleted"}) 
                else:
                    cur.execute("DELETE FROM payments WHERE id=%s", [id ])
                    mysql.commit()
                    cur.close()
                    mysql.close()
                    return jsonify({"success":"Deleted Successfully"})
            else:
                return jsonify({"error":"Admin access only"})   
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"})     
		
@app.route("/refcount-user", methods=['GET', 'POST'])
def refcountuser():
    if request.method == "POST":
        token = request.form['token']
        user_id = request.form['user_id']
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["uid"]
            mysql = dbconnection()
            cur = mysql.cursor(dictionary=True,buffered=True)
            cur.execute("SELECT * FROM keystore WHERE refer_by=%s",[user_id])
            user = cur.fetchone()
            count = cur.rowcount
            if user:
                cur.close()
                mysql.close()
                return jsonify({"success":"ok","count":count}) 
            else:
                return jsonify({"error":"failed","count":0})   
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"})  		