from apps import *
from apps.db import dbconnection

@app.route('/taskup', methods=['POST','GET'])
def taskup():
    try:
        currenttime = datetime.now()
        return jsonify({"success":"Task is updated"})
    except:
        return jsonify({"error":"Task is updated"})    

@app.route('/task', methods=['POST','GET'])   
def task():
    mysql = dbconnection()
    cur = mysql.cursor(dictionary=True,buffered=True)
    cur.execute("SELECT * FROM settings WHERE id=%s",[1])
    data = cur.fetchone()
    miningbonus=data["miningbonus"]
    coin_raw_id=data["coin_raw_id"]
    currenttime = datetime.now()

    if request.method == "POST":
        token = request.form['token']
        print(currenttime)
        print(datetime.strptime(str(currenttime),"%Y-%m-%d %H:%M:%S.%f"))
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["user_id"]
            cur = mysql.cursor(dictionary=True,buffered=True)
            cur.execute("SELECT * FROM keystore WHERE id=%s",[uid])
            user = cur.fetchone()
            print(user["nexttask"])
            miningtime = datetime.now() + timedelta(hours=24)

            cur.execute("SELECT * FROM payments WHERE uid=%s and type=%s",[uid,"Task"])
            count = cur.rowcount

            if user["task"]=="No" and user["nexttask"]=="No" :
                if count==6:    
                    cur.execute("UPDATE wallet SET balance=balance + %s WHERE uid=%s and coin_id=%s",("1" ,uid,"4"))
                    cur.execute("INSERT INTO payments (uid,coin_id,type,amount)" "VALUES(%s,%s,%s,%s)",(uid,"4","Task","1" ))
                    cur.execute("UPDATE keystore SET task=%s,nexttask=%s WHERE id=%s",("Yes",miningtime ,uid))
                    mysql.commit()
                    cur.close()
                    mysql.close()
                    return jsonify({"success":"Task is successful"})
                else:    
                    cur.execute("UPDATE wallet SET balance=balance + %s WHERE uid=%s and coin_id=%s",(miningbonus ,uid,coin_raw_id))
                    cur.execute("INSERT INTO payments (uid,coin_id,type,amount)" "VALUES(%s,%s,%s,%s)",(uid,coin_raw_id,"Task",miningbonus ))
                    cur.execute("UPDATE keystore SET task=%s,nexttask=%s WHERE id=%s",("Yes",miningtime ,uid))
                    mysql.commit()
                    cur.close()
                    mysql.close()
                    return jsonify({"success":"Task is successful"})
            else:
                cur.close()
                mysql.close()
                return jsonify({"error":"Already Claimed today. wait for 24 hours"})
        except:
            cur.close()
            mysql.close()
            return jsonify({"error":"Invalid Token"})
    else:
        cur.close()
        mysql.close()
        return jsonify({"error":"Get method not allow"})
    

@app.route('/taskpay', methods=['POST','GET'])
def taskpay():
    if request.method == "POST":
        token = request.form['token']
        mysql = dbconnection()
        cur = mysql.cursor(dictionary=True,buffered=True)
        currenttime = datetime.now()
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["uid"]
            uid = uid[:32]
            user_id = decoded["user_id"]
            
            cur.execute("SELECT * FROM keystore WHERE id=%s",[user_id])
            user = cur.fetchone()
            try:
                exp =  datetime.strptime(user["nexttask"],"%Y-%m-%d %H:%M:%S.%f")
                if currenttime>=exp:
                    cur.execute("UPDATE keystore SET task=%s,nexttask=%s WHERE id=%s",("No","No" ,user_id))
                    mysql.commit()
                print("Trying")
            except:
                print("Okk")    

            cur.execute("SELECT * FROM payments WHERE uid=%s and type=%s",[user_id,"Task"])
            count = cur.rowcount
            print(count)
            if count>=7:
                cur.execute("DELETE FROM payments WHERE uid=%s and type=%s", [user_id,"Task" ])
                mysql.commit()

            cur.execute("""SELECT payments.*,coin.coin_name,coin.coin_symbol,coin.coin_type,coin.platform,
                                 coin.contract,coin.explorer,coin.logo FROM payments 
                                 LEFT JOIN coin ON payments.coin_id=coin.id WHERE payments.uid=%s and payments.type=%s ORDER by payments.id ASC 
                                 """,[user_id,"Task"])
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
    
@app.route('/mytask', methods=['POST','GET'])   
def mytask():
    mysql = dbconnection()
    cur = mysql.cursor(dictionary=True,buffered=True)
    currenttime = datetime.now()
    if request.method == "POST":
        token = request.form['token']
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["user_id"]
            cur = mysql.cursor(dictionary=True,buffered=True)
            cur.execute("SELECT * FROM keystore WHERE id=%s",[uid])
            user = cur.fetchone()
            return jsonify({"success":"Query is successful","task":user["task"]})
        except:
            cur.close()
            mysql.close()
            return jsonify({"error":"Invalid Token"})
    else:
        cur.close()
        mysql.close()
        return jsonify({"error":"Get method not allow"})
     