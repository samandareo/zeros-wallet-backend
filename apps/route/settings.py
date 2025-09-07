from apps import *
from apps.db import dbconnection

@app.route("/settings/get", methods=['GET', 'POST'])
def settingsget():
    mysql = dbconnection()
    cur = mysql.cursor(dictionary=True,buffered=True)
    cur.execute("SELECT * FROM settings WHERE id=1")
    data = cur.fetchone()
    cur.close()
    mysql.close()
    if data:
        return jsonify(data)
    else:
        return jsonify({})

@app.route("/settings", methods=['GET', 'POST'])
def settings():
    if request.method == "POST":
        token = request.form['token']
        registerbonus = request.form['registerbonus']
        referralbonus = request.form['referralbonus']
        coin_raw_id = request.form['coin_raw_id']
        miningbonus = request.form['miningbonus']
        maxswap = request.form['maxswap']
        commission = request.form['commission']
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["uid"]
            uid = uid[:32]
            mysql = dbconnection()
            cur = mysql.cursor(dictionary=True,buffered=True)
            cur.execute("SELECT * FROM keystore WHERE uuid=%s",[uid])
            user = cur.fetchone()
            if user["type"]=="Admin":
                query=( registerbonus,referralbonus,miningbonus,coin_raw_id,maxswap,commission)
                cur.execute("UPDATE settings SET registerbonus=%s,referralbonus=%s,miningbonus=%s,coin_raw_id=%s,maxswap=%s,commission=%s WHERE id=1",query)
                mysql.commit()
                cur.close()
                mysql.close()
                return jsonify({"success":"Settings changed successfully"}) 
            else:
                return jsonify({"error":"Admin access only"})   
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"}) 