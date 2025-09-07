from apps import *
from apps.db import dbconnection

@app.route("/addstaketrx", methods=['GET', 'POST'])
def stakestxadd():
    if request.method == "POST":
        token = request.form['token']
        stakeid = request.form['stakeid']
        amount = request.form['amount']
        days = request.form['days']
        if days=="":
             return jsonify({"success":"Staking day is required"})         
        mysql = dbconnection()
        cur = mysql.cursor(dictionary=True,buffered=True)
        cur.execute("SELECT * FROM stakecoin WHERE id=%s",[stakeid])
        data = cur.fetchone()
        coin_raw_id = data["coin_raw_id"]
        profit_coin = data["profit_coin"]
        min_invest = data["min_invest"]
        percent = request.form['percent']
        rate = data["rate"]
        #print(data)
        enddate = datetime.now() + timedelta(days=int(days))
        ftotal = float(amount)*float(rate)
        ftotal = ftotal*float(days)

        if float(min_invest)>float(amount):
             return jsonify({"success":"Minimum Stake is : "+min_invest}) 

        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["user_id"]
            cur.execute("SELECT * FROM wallet WHERE uid=%s and coin_id=%s",[uid,coin_raw_id])
            wallet = cur.fetchone()
            bal = wallet["balance"]   

            if float(bal)>=float(amount):
                cur.execute("UPDATE wallet SET balance=balance - %s WHERE uid=%s and coin_id=%s",(amount ,uid,coin_raw_id))
                cur.execute("INSERT INTO staketrx (uid,coin_raw_id,profit_coin,amount,days,enddate,ftotal,status)" 
                                 "VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",
                                 (uid,coin_raw_id,profit_coin,amount,days,enddate,ftotal,"Ongoing"))
                mysql.commit()
                cur.close()
                mysql.close()
                return jsonify({"success":"Stake created successfully"}) 
            else:
                return jsonify({"error":"Balance not enough"}) 
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"})
    

@app.route("/mystake/<uid>/<limit>", methods=['GET', 'POST'])
def mytrxstake(uid,limit): 
    currenttime = datetime.now()
    mysql = dbconnection()
    cur = mysql.cursor(dictionary=True,buffered=True)
    '''
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
    '''
    cur.execute("""SELECT staketrx.*,coin_raw_id.coin_symbol as name,profit_coin.coin_symbol as profit_coin,
                                coin_raw_id.logo
                                 FROM staketrx 
                                 LEFT JOIN coin as coin_raw_id ON staketrx.coin_raw_id=coin_raw_id.id 
                                 LEFT JOIN coin as profit_coin ON staketrx.profit_coin=profit_coin.id 
                                 WHERE staketrx.uid=%s ORDER BY staketrx.id DESC LIMIT %s""",[uid,int(limit)])
    trx = cur.fetchall() 
    cur.close() 
    if trx:
        print(len(trx))
        return jsonify(trx)
    else:
        return({"error":"Query Failed"})   
    
@app.route("/allstakes/<limit>", methods=['GET', 'POST'])
def alltrxstake(limit): 
    mysql = dbconnection()
    cur = mysql.cursor(dictionary=True,buffered=True)
    cur.execute("""SELECT staketrx.*,coin_raw_id.coin_symbol as name,profit_coin.coin_symbol as profit_coin
                                 FROM staketrx 
                                 LEFT JOIN coin as coin_raw_id ON staketrx.coin_raw_id=coin_raw_id.id 
                                 LEFT JOIN coin as profit_coin ON staketrx.profit_coin=profit_coin.id 
                                 ORDER BY staketrx.id DESC LIMIT %s""",[int(limit)])
    trx = cur.fetchall() 
    cur.close() 
    if trx:
        print(len(trx))
        return jsonify(trx)
    else:
        return({"error":"Query Failed"})      