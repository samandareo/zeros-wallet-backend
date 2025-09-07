from apps import *
from apps.db import dbconnection
import os

@app.route("/airdrop-join", methods=['GET', 'POST'])
def joinairdrop():
    mysql = dbconnection()
    cur = mysql.cursor(dictionary=True,buffered=True)
    if request.method == "POST":
        token = request.form['token']
        id = request.form['id']
        cur.execute("SELECT * FROM airdrop WHERE id=%s",[id])
        airdrop = cur.fetchone()
        coin_raw_id = airdrop["coin_raw_id"]
        status = airdrop["status"]
        if status=="Closed":
            return jsonify({"error":"Airdrop currently closed or disabled"})
        telegram = request.form['telegram']
        telegram2 = request.form['telegram2']
        twitter = request.form['twitter']
        twitter2 = request.form['twitter2']
        facebook = request.form['facebook']
        website = request.form['website']
        discord = request.form['discord']
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["user_id"]

            cur.execute("SELECT * FROM airdropparticipate WHERE uid=%s and airdrop_id=%s",[uid,id])
            airdropcheck = cur.rowcount
            print(airdropcheck)
            if airdropcheck>0:
                return jsonify({"success":"You have already joined in this airdrop"})
            cur.execute("UPDATE airdrop SET count=count + %s WHERE id=%s",("1",id))
            cur.execute("INSERT INTO airdropparticipate (uid,coin_raw_id,airdrop_id,telegram,telegram2,twitter,twitter2,facebook,website,discord)" 
                                 "VALUES(%s,%s, %s,%s,%s,%s,%s,%s,%s,%s)",
            (uid,coin_raw_id,id,telegram,telegram2,twitter,twitter2,facebook,website,discord))
            mysql.commit()
            cur.close()
            mysql.close()
            return jsonify({"success":"Airdrop Submitted Successfully"})               
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"})
   

@app.route("/all-airdropuser/<limit>", methods=['GET', 'POST'])
def allairdropuser(limit):   
    limit = int(limit)
    mysql = dbconnection()
    cur = mysql.cursor(dictionary=True,buffered=True)
    cur.execute("""SELECT airdropparticipate.*, airdrop.title,airdrop.des,airdrop.logo 
                FROM airdropparticipate
                LEFT JOIN airdrop ON airdropparticipate.airdrop_id=airdrop.id  
                ORDER BY airdropparticipate.id DESC LIMIT %s""",[limit])
    airdrop = cur.fetchall()
    cur.close()
    mysql.close()
    if airdrop:
        return jsonify(airdrop)
    else:
        return([])

@app.route("/airdropid/<id>/<limit>", methods=['GET', 'POST'])
def airdropid(id,limit):   
    limit = int(limit)
    id = id
    mysql = dbconnection()
    cur = mysql.cursor(dictionary=True,buffered=True)
    cur.execute("""SELECT airdropparticipate.*, airdrop.title,airdrop.des,airdrop.logo 
                FROM airdropparticipate
                LEFT JOIN airdrop ON airdropparticipate.airdrop_id=airdrop.id  
                WHERE airdropparticipate.airdrop_id=%s
                ORDER BY airdropparticipate.airdrop_id DESC LIMIT %s""",[id,limit])
    airdrop = cur.fetchall()
    cur.close()
    mysql.close()
    if airdrop:
        return jsonify(airdrop)
    else:
        return([])    

@app.route("/my-airdrop/<uid>/<limit>", methods=['GET', 'POST'])
def myairdrop(uid,limit):   
    limit = int(limit)
    uid = uid
    mysql = dbconnection()
    cur = mysql.cursor(dictionary=True,buffered=True)
    cur.execute("""SELECT airdropparticipate.*, airdrop.title,airdrop.des,airdrop.logo 
                FROM airdropparticipate
                LEFT JOIN airdrop ON airdropparticipate.airdrop_id=airdrop.id  
                WHERE airdropparticipate.uid=%s
                ORDER BY airdropparticipate.id DESC LIMIT %s""",[uid,limit])
    airdrop = cur.fetchall()
    cur.close()
    mysql.close()
    if airdrop:
        return jsonify(airdrop)
    else:
        return([])    