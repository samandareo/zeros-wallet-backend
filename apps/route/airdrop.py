from apps import *
from apps.db import dbconnection
import os

def save_images(photo):
     hash_photo = secrets.token_urlsafe(10)
     _, file_extention = os.path.splitext(photo.filename)
     photo_name = hash_photo + file_extention
     #print(file_extention)
     if file_extention=="" or file_extention==None:
         return ""
     file_path = os.path.join(current_app.root_path, 'static/images-airdrop', photo_name)
     photo.save(file_path)
     return photo_name

def check_images(photo):
     hash_photo = secrets.token_urlsafe(10)
     _, file_extention = os.path.splitext(photo.filename)
     photo_name = hash_photo + file_extention
     #print(file_extention)
     if file_extention=="" or file_extention==None:
         return ""
     return photo_name

@app.route("/add-airdrop", methods=['GET', 'POST'])
def addairdrop():
    if request.method == "POST":
        token = request.form['token']
        title = request.form['title']
        des = request.form['des']
        coin_raw_id = request.form['coin_raw_id']
        end = request.form['end']
        telegram = request.form['telegram']
        telegram2 = request.form['telegram2']
        twitter = request.form['twitter']
        twitter2 = request.form['twitter2']
        facebook = request.form['facebook']
        website = request.form['website']
        status = request.form['status']
        reward = request.form['reward']
        logo = request.form['logo']
        discord = request.form['discord']
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["uid"]
            uid = uid[:32]
            mysql = dbconnection()
            cur = mysql.cursor(dictionary=True,buffered=True)
            cur.execute("SELECT * FROM keystore WHERE uuid=%s",[uid])
            user = cur.fetchone()
            if user["type"]=="Admin":
                try:
                    cur.execute("INSERT INTO airdrop (title,des,logo,coin_raw_id,end,telegram,telegram2,twitter,twitter2,facebook,website,status,reward,discord)" 
                                 "VALUES(%s,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                 (title,des,logo,coin_raw_id,end,telegram,telegram2,twitter,twitter2,facebook,website,status,reward,discord))
                    mysql.commit()
                    cur.close()
                    mysql.close()
                    return jsonify({"success":"Airdrop Added Successfully"}) 
                except:
                    cur.execute("INSERT INTO airdrop (title,des,logo,coin_raw_id,end,telegram,telegram2,twitter,twitter2,facebook,website,status,reward,discord)" 
                                 "VALUES(%s,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                 (title,des,logo,coin_raw_id,end,telegram,telegram2,twitter,twitter2,facebook,website,status,reward,discord))
                    mysql.commit()
                    cur.close()
                    mysql.close()
                    return jsonify({"success":"Airdrop Added Successfully"})                         
            else:
                return jsonify({"error":"Admin access only"})   
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"})


@app.route("/update-airdrop", methods=['GET', 'POST'])
def updateairdrop():
    if request.method == "POST":
        token = request.form['token']
        title = request.form['title']
        des = request.form['des']
        coin_raw_id = request.form['coin_raw_id']
        end = request.form['end']
        telegram = request.form['telegram']
        telegram2 = request.form['telegram2']
        twitter = request.form['twitter']
        twitter2 = request.form['twitter2']
        facebook = request.form['facebook']
        website = request.form['website']
        status = request.form['status']
        reward = request.form['reward']
        logo = request.form['logo']
        discord = request.form['discord']
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
                try:   
                    cur.execute("UPDATE airdrop SET title=%s,des=%s,logo=%s,coin_raw_id=%s,end=%s,telegram=%s,telegram2=%s,twitter=%s,twitter2=%s,facebook=%s,website=%s,status=%s,reward=%s,discord=%s WHERE id=%s", 
                                (title,des,logo,coin_raw_id,end,telegram,telegram2,twitter,twitter2,facebook,website,status,reward,discord, id ))
                    mysql.commit()
                    cur.close()
                    mysql.close()
                    return jsonify({"success":"Airdrop Updated Successfully"}) 
                except:
                    cur.execute("UPDATE airdrop SET title=%s,des=%s,logo=%s,coin_raw_id=%s,end=%s,telegram=%s,telegram2=%s,twitter=%s,twitter2=%s,facebook=%s,website=%s,status=%s,reward=%s,discord=%s WHERE id=%s", 
                                (title,des,logo,coin_raw_id,end,telegram,telegram2,twitter,twitter2,facebook,website,status,reward,discord, id ))
                    mysql.commit()
                    cur.close()
                    mysql.close()
                    return jsonify({"success":"Airdrop Updated Successfully"})      
            else:
                return jsonify({"error":"Admin access only"})    
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"})
    
@app.route("/delete-airdrop", methods=['GET', 'POST'])    
def deleteairdrop():
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
                cur.execute("DELETE FROM airdrop WHERE id=%s", [id ])
                cur.execute("DELETE FROM airdropparticipate WHERE airdrop_id=%s", [id ])
                mysql.commit()

                cur.close() 
                mysql.close()
                return jsonify({"success":"Airdrop Deleted Successfully"}) 
            else:
                return jsonify({"error":"Admin access only"})   
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"})    
    

@app.route("/all-airdrop", methods=['GET', 'POST'])
def allairdrop():   
    mysql = dbconnection()
    cur = mysql.cursor(dictionary=True,buffered=True)
    cur.execute("SELECT * FROM airdrop ORDER BY id DESC")
    airdrop = cur.fetchall()
    cur.close()
    mysql.close()
    if airdrop:
        return jsonify(airdrop)
    else:
        return([])

@app.route("/airdrop/ongoing", methods=['GET', 'POST'])
def ongoingairdrop():
    mysql = dbconnection()
    cur = mysql.cursor(dictionary=True,buffered=True)
    cur.execute("SELECT * FROM airdrop WHERE status=%s",["Ongoing"])
    airdrop = cur.fetchall()
    cur.close()
    mysql.close()
    if airdrop:
        return jsonify(airdrop)
    else:
        return([])

@app.route("/airdrop/closed", methods=['GET', 'POST'])
def closedairdrop():
    mysql = dbconnection()
    cur = mysql.cursor(dictionary=True,buffered=True)
    cur.execute("SELECT * FROM airdrop WHERE status=%s",["Closed"])
    airdrop = cur.fetchall()
    cur.close()
    mysql.close()
    if airdrop:
        return jsonify(airdrop)
    else:
        return([])

@app.route("/airdrop/<id>", methods=['GET', 'POST'])
def oneairdrop(id):
    mysql = dbconnection()
    cur = mysql.cursor(dictionary=True,buffered=True)
    cur.execute("SELECT * FROM airdrop WHERE id=%s",[id])
    airdrop = cur.fetchall()
    cur.close()
    mysql.close()
    if airdrop:
        return jsonify(airdrop)
    else:
        return([])