from apps import *
from apps.db import dbconnection

@app.route("/addstake", methods=['GET', 'POST'])
def stakeadd():
    if request.method == "POST":
        token = request.form['token']
        coin_raw_id = request.form['coin_raw_id']
        profit_coin = request.form['profit_coin']
        days = request.form['days']
        profit = request.form['profit']
        status = request.form['status']
        min_invest = request.form['min_invest']
        rate = request.form['rate']
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["uid"]
            uid = uid[:32]
            mysql = dbconnection()
            cur = mysql.cursor(dictionary=True,buffered=True)
            cur.execute("SELECT * FROM keystore WHERE uuid=%s",[uid])
            user = cur.fetchone()
            if user["type"]=="Admin":
                    cur.execute("INSERT INTO stakecoin (coin_raw_id,profit_coin,rate,days,profit,status,min_invest)" 
                                 "VALUES(%s,%s,%s,%s,%s,%s,%s)",
                                 (coin_raw_id,profit_coin,rate,days,profit,status,min_invest))
                    mysql.commit()
                    cur.close()
                    mysql.close()
                    return jsonify({"success":"stake Added Successfully"})                       
            else:
                return jsonify({"error":"Admin access only"})   
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"})
    
@app.route("/updatestake", methods=['GET', 'POST'])
def stakeupdate():
    if request.method == "POST":
        token = request.form['token']
        coin_raw_id = request.form['coin_raw_id']
        profit_coin = request.form['profit_coin']
        rate = request.form['rate']
        days = request.form['days']
        profit = request.form['profit']
        status = request.form['status']
        min_invest = request.form['min_invest']
        id = request.form['id']
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["uid"]
            uid = uid[:32]
            mysql = dbconnection()
            cur = mysql.cursor(dictionary=True,buffered=True)
            cur.execute("SELECT * FROM keystore WHERE uuid=%s",[uid])
            user = cur.fetchone()
            if user["type"]=="Admin":
                    cur.execute("UPDATE stakecoin SET coin_raw_id=%s,profit_coin=%s,rate=%s,days=%s,profit=%s,status=%s,min_invest=%s WHERE id=%s", 
                                (coin_raw_id,profit_coin,rate,days,profit,status,min_invest,id ))
                    mysql.commit()
                    cur.close()
                    mysql.close()
                    return jsonify({"success":"stake Updated Successfully "}) 
            else:
                return jsonify({"error":"Admin access only"})   
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"})    

@app.route("/deletestake", methods=['GET', 'POST'])
def deletestake():
    if request.method == "POST":
        token = request.form['token']
        id = request.form['id']
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["uid"]
            uid = uid[:32]
            mysql = dbconnection()
            cur = mysql.cursor(dictionary=True,buffered=True)
            cur.execute("SELECT * FROM keystore WHERE uuid=%s",[uid])
            user = cur.fetchone()
            if user["type"]=="Admin":
                cur.execute("DELETE FROM stakecoin WHERE id=%s", [id ])
                cur.execute("DELETE FROM staketrx WHERE coin_raw_id=%s", [id])

                mysql.commit()
                cur.close()
                mysql.close()
                return jsonify({"success":"stake Deleted Successfully"})
            else:
                return jsonify({"error":"Admin access only"})   
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"})    
    
@app.route("/allstake", methods=['GET', 'POST'])
def allstake():
    mysql = dbconnection()
    cur = mysql.cursor(dictionary=True,buffered=True)
    cur.execute("""SELECT stakecoin.*,coin.coin_name,coin.coin_symbol,
                profit.coin_symbol as profitsymbol,coin.logo,coin.price
                FROM stakecoin
                LEFT JOIN coin ON stakecoin.coin_raw_id=coin.id 
                LEFT JOIN coin as profit ON stakecoin.profit_coin=profit.id 
                 ORDER BY stakecoin.id ASC""")
    stake = cur.fetchall()
    cur.close()
    mysql.close()
    if stake:
        #print(len(stake))
        return jsonify(stake)
    else:
        return({"error":"Query Failed"})

@app.route("/stake/<id>", methods=['GET', 'POST'])
def oneistake(id):
    mysql = dbconnection()
    cur = mysql.cursor(dictionary=True,buffered=True)
    cur.execute("""SELECT stakecoin.*,coin.coin_name,coin.coin_symbol,
                profit.coin_symbol as profitsymbol ,coin.logo,coin.price
                FROM stakecoin
                LEFT JOIN coin ON stakecoin.coin_raw_id=coin.id 
                LEFT JOIN coin as profit ON stakecoin.profit_coin=profit.id 
                 WHERE stakecoin.id=%s""",[id])
    stake = cur.fetchall()
    cur.close()
    mysql.close()
    if stake:
        print(len(stake))
        return jsonify(stake)
    else:
        return({"error":"Query Failed"})