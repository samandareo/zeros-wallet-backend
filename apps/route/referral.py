from apps import *
from apps.db import dbconnection

@app.route('/myreferral', methods=['POST','GET'])
def myreferral():
    mysql = dbconnection()
    cur = mysql.cursor(dictionary=True,buffered=True)
    if request.method == "POST":
        token = request.form['token']
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["uid"]
            uid = uid[:32]
            user_id = decoded["user_id"]

            cur.execute("SELECT * FROM keystore WHERE id=%s",[user_id])
            myid = cur.fetchone()
            refer_by = myid["refer_by"]
            
            return jsonify({"success":"success","refer_by":refer_by})

        except:
            return jsonify({"error":"Invalid Token"})
    else:
        return jsonify({"error":"Get method not allow"})

@app.route('/addreferral', methods=['POST','GET'])
def addreferral():
    mysql = dbconnection()
    cur = mysql.cursor(dictionary=True,buffered=True)
    cur.execute("SELECT * FROM settings WHERE id=1")
    data = cur.fetchone()
    referralbonus = data["referralbonus"]
    coin_raw_id = data["coin_raw_id"]
    if request.method == "POST":
        token = request.form['token']
        refcode = request.form['refcode']
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["uid"]
            uid = uid[:32]
            user_id = decoded["user_id"]

            cur.execute("SELECT * FROM keystore WHERE id=%s",[user_id])
            myid = cur.fetchone()
            refer_by = myid["refer_by"]
            cur.execute("SELECT * FROM keystore WHERE refcode=%s",[refcode])
            refid = cur.fetchone()
            referid = refid["id"]

            if refer_by=="":
                cur.execute("UPDATE keystore SET refer_by=%s WHERE id=%s",(refcode,user_id))
                cur.execute("UPDATE wallet SET balance=balance + %s WHERE uid=%s and coin_id=%s",(referralbonus ,referid,coin_raw_id))
                if float(referralbonus)>0:
                   cur.execute("INSERT INTO payments (uid,coin_id,type,amount)" "VALUES(%s,%s,%s,%s)",(referid,coin_raw_id,"Referral Bonus",referralbonus ))
                mysql.commit()
                cur.close()
                mysql.close()
                return jsonify({"success":"Referral Added Successfully"}) 
            else:
                return jsonify({"success":"Referral already added"}) 
        except:
            return jsonify({"error":"Invalid Token"})
    else:
        return jsonify({"error":"Get method not allow"})