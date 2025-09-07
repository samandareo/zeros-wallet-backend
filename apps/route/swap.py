from apps import *
from apps.db import dbconnection

@app.route('/convert', methods=['POST','GET'])   
def convert():
    mysql = dbconnection()
    cur = mysql.cursor(dictionary=True,buffered=True)
    cur.execute("SELECT * FROM settings WHERE id=1")
    data = cur.fetchone()
    commission = data["commission"]
    coin_raw_id = "3" #data["coin_raw_id"]
    maxswap = float(data["maxswap"])
    if request.method == "POST":
        fromid = request.form['fromid']
        toid = request.form['toid']
        amount = request.form['amount']
        token = request.form['token']
        if fromid=="":
            return jsonify({"error":"From Coin is Required"})
        if toid=="":
            return jsonify({"error":"To Coin is Required"})
        if amount=="" or float(amount)==0:
            return jsonify({"error":"Amount is Required"})
        cur.execute("SELECT * FROM coin WHERE id=%s",[fromid])
        fromcoin = cur.fetchone()
        fromprice =fromcoin["price"]

        cur.execute("SELECT * FROM coin WHERE id=%s",[toid])
        tocoin = cur.fetchone()
        toprice = tocoin["price"]
        print("From Price : ",fromprice)
        rate = float(fromprice)/float(toprice)*1
        print(rate)
        usd = float(amount)*float(fromprice)
        bonus = usd*30
        print("USD Amount : ",usd)
        print("Bonus : ",bonus)
        ramount = str(float(bonus)*float(commission)/100)
        print("Commission : ",ramount)
        if usd<1:
             return jsonify({"error":"Minimum swap is $1"})
        am = float(fromprice)*float(amount)
        if am>200:
             return jsonify({"error":"Maximum swap is $200"})
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["user_id"]
            totalvol=0
            cur.execute("""SELECT convertcoin.*,fromcoin.coin_symbol as fromname, fromcoin.price
                                 FROM convertcoin 
                                 LEFT JOIN coin as fromcoin ON convertcoin.fromid=fromcoin.id 
                                 WHERE convertcoin.uid=%s and  convertcoin.created_at>= NOW() - INTERVAL 1 DAY""",[uid])
            convert = cur.fetchall() 
            for i in convert:
                 print(i)
                 totalvol+=float(i["amount"])*float(i["price"])
            print("Total Volume : ",totalvol)
            totalvol+=am
            if totalvol>=maxswap:
                 return jsonify({"error":"Daily Swap Limit is $200"})
            cur.execute("SELECT * FROM keystore WHERE id=%s",[uid])
            myid = cur.fetchone()
            refer_by = myid["refer_by"]
            refid = ""
            if refer_by !="":
                cur.execute("SELECT * FROM keystore WHERE refcode=%s",[refer_by])
                ref = cur.fetchone()
                refid = ref["id"]

            cur.execute("SELECT * FROM wallet WHERE uid=%s and coin_id=%s",[uid,fromid])
            wallet = cur.fetchone()
            bal = wallet["balance"]    
            cbal = float(fromprice)/float(toprice)*float(amount)
            print("Bal : ",cbal)

            if float(amount)<=float(bal):
                    try:     
                        mysql.autocommit = True
                        mysql.start_transaction()
                        cur.execute("UPDATE wallet SET balance=balance - %s WHERE uid=%s and coin_id=%s",(amount ,uid,fromid))
                        cur.execute("UPDATE wallet SET balance=balance + %s WHERE uid=%s and coin_id=%s",(cbal ,uid,toid))
                        #cur.execute("UPDATE wallet SET balance=balance + %s WHERE uid=%s and coin_id=%s",(bonus ,uid,coin_raw_id))
                        cur.execute("INSERT INTO convertcoin (uid,fromid,toid,amount,rate,rcoin)" "VALUES(%s,%s,%s,%s,%s,%s)",(uid,fromid,toid,amount,rate,cbal))
                        #cur.execute("INSERT INTO payments (uid,coin_id,type,amount)" "VALUES(%s,%s,%s,%s)",(uid,coin_raw_id,"Swap Bonus",bonus ))
                        if refid!="":
                             cur.execute("UPDATE wallet SET balance=balance + %s WHERE uid=%s and coin_id=%s",(ramount ,refid,coin_raw_id))
                             cur.execute("INSERT INTO payments (uid,coin_id,type,amount)" "VALUES(%s,%s,%s,%s)",(refid,coin_raw_id,"Referral Bonus",ramount ))
                        mysql.commit()
                        return jsonify({"success":"Convert is successful"})
                    except:
                        mysql.rollback()
                        return jsonify({"error":"Convert not successful"})
            else:
                return jsonify({"error":"Balance not enough"})
        except:
            return jsonify({"error":"Invalid Token"})
    else:
        return jsonify({"error":"Get method not allow"})
    
@app.route('/my/convert/<uid>/<limit>', methods=['POST','GET'])
def myconvert(uid,limit):
        limit=int(limit)
        mysql = dbconnection()
        cur = mysql.cursor(dictionary=True,buffered=True)
        cur.execute("""SELECT convertcoin.*,fromcoin.coin_symbol as fromname,tocoin.coin_symbol as toname
                                 FROM convertcoin 
                                 LEFT JOIN coin as fromcoin ON convertcoin.fromid=fromcoin.id 
                                 LEFT JOIN coin as tocoin ON convertcoin.toid=tocoin.id 
                                 WHERE convertcoin.uid=%s ORDER BY convertcoin.id DESC LIMIT %s""",[uid,limit])
        convert = cur.fetchall() 
        cur.close()   
        return jsonify({"success":"Query success","data":convert})

@app.route('/all/convert/<limit>', methods=['POST','GET'])
def allconvert(limit):
        limit=int(limit)
        mysql = dbconnection()
        cur = mysql.cursor(dictionary=True,buffered=True)
        cur.execute("""SELECT convertcoin.*,fromcoin.coin_symbol as fromname,tocoin.coin_symbol as toname
                                 FROM convertcoin 
                                 LEFT JOIN coin as fromcoin ON convertcoin.fromid=fromcoin.id 
                                 LEFT JOIN coin as tocoin ON convertcoin.toid=tocoin.id 
                                 ORDER BY convertcoin.id DESC LIMIT %s""",[limit])
        convert = cur.fetchall() 
        cur.close()   
        return jsonify({"success":"All Query success","data":convert})

