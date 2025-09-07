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
     file_path = os.path.join(current_app.root_path, 'static/images-coin', photo_name)
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


@app.route("/add-ccoin", methods=['GET', 'POST'])
def ccoinadd():
    if request.method == "POST":
        token = request.form['token']
        coin_name = request.form['coin_name']
        coin_symbol = request.form['coin_symbol']
        code = request.form['code']
        coin_type = request.form['coin_type']
        platform = request.form['platform']
        contract = request.form['contract']
        coin_decimal = request.form['coin_decimal']
        explorer = request.form['explorer']
        price = request.form['price']
        deposit = request.form['deposit']
        withdrew = request.form['withdrew']
        status = request.form['status']
        swap = request.form['swap']
        fee = request.form['fee']
        fee_coin = request.form['fee_coin']
        fund_address = request.form['fund_address']
        logo = request.form['logo']
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
                    cur.execute("INSERT INTO coin (coin_name,coin_symbol,coin_decimal,contract,coin_type,code,price,logo,platform,deposit,withdrew,status,swap,explorer,fund_address,fee_coin,fee)" 
                                 "VALUES(%s,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                 (coin_name,coin_symbol,coin_decimal,contract,coin_type,code,price,logo,platform,deposit,withdrew,status,swap,explorer,fund_address,fee_coin,fee ))
                    mysql.commit()
                    cur.close()
                    mysql.close()
                    return jsonify({"success":"Coin Added Successfully"}) 
                except:
                    cur.execute("INSERT INTO coin (coin_name,coin_symbol,coin_decimal,contract,coin_type,code,price,logo,platform,deposit,withdrew,status,swap,explorer,fund_address,fee_coin,fee)" 
                                 "VALUES(%s,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                 (coin_name,coin_symbol,coin_decimal,contract,coin_type,code,price,logo,platform,deposit,withdrew,status,swap,explorer,fund_address,fee_coin,fee ))
                    mysql.commit()
                    cur.close()
                    mysql.close()
                    return jsonify({"success":"Coin Added Successfully"})                         
            else:
                return jsonify({"error":"Admin access only"})   
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"})
    
@app.route("/update-ccoin", methods=['GET', 'POST'])
def updateccoin():
    if request.method == "POST":
        token = request.form['token']
        id = request.form['id']
        coin_name = request.form['coin_name']
        coin_symbol = request.form['coin_symbol']
        code = request.form['code']
        coin_type = request.form['coin_type']
        platform = request.form['platform']
        contract = request.form['contract']
        coin_decimal = request.form['coin_decimal']
        explorer = request.form['explorer']
        price = request.form['price']
        deposit = request.form['deposit']
        withdrew = request.form['withdrew']
        status = request.form['status']
        swap = request.form['swap']
        fee = request.form['fee']
        fee_coin = request.form['fee_coin']
        fund_address = request.form['fund_address']
        logo = request.form['logo']
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["uid"]
            uid = uid[:32]
            mysql = dbconnection()
            cur = mysql.cursor(dictionary=True,buffered=True)
            cur.execute("SELECT * FROM keystore WHERE uuid=%s",[uid])
            user = cur.fetchone()
            if user["type"]=="Admin":
                cur.execute("SELECT * FROM coin WHERE id=%s",[id])
                coin = cur.fetchone()
                #request.files['logo_img']
                try:   
                    cur.execute("UPDATE coin SET coin_name=%s,coin_symbol=%s,coin_decimal=%s,contract=%s,coin_type=%s,code=%s,price=%s,logo=%s,platform=%s,deposit=%s,withdrew=%s,status=%s,swap=%s,explorer=%s,fund_address=%s,fee_coin=%s,fee=%s WHERE id=%s", 
                                (coin_name,coin_symbol,coin_decimal,contract,coin_type,code,price,logo,platform,deposit,withdrew,status,swap,explorer,fund_address,fee_coin,fee, id ))
                    mysql.commit()
                    cur.close()
                    mysql.close()
                    return jsonify({"success":"Coin Updated Successfully"}) 
                except:
                    cur.execute("UPDATE coin SET coin_name=%s,coin_symbol=%s,coin_decimal=%s,contract=%s,coin_type=%s,code=%s,price=%s,logo=%s,platform=%s,deposit=%s,withdrew=%s,status=%s,swap=%s,explorer=%s,fund_address=%s,fee_coin=%s,fee=%s WHERE id=%s", 
                                (coin_name,coin_symbol,coin_decimal,contract,coin_type,code,price,logo,platform,deposit,withdrew,status,swap,explorer,fund_address,fee_coin,fee, id ))
                    mysql.commit()
                    cur.close()
                    mysql.close()
                    return jsonify({"success":"Coin Updated Successfully"})      
            else:
                return jsonify({"error":"Admin access only"})   
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"})    

@app.route("/delete-ccoin", methods=['GET', 'POST'])    
def deleteccoin():
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
                cur.execute("DELETE FROM coin WHERE id=%s", [id ])
                mysql.commit()

                cur.execute("DELETE FROM wallet WHERE coin_id=%s", [id])
                mysql.commit()
                cur.execute("DELETE FROM payments WHERE coin_id=%s", [id])
                cur.execute("DELETE FROM airdrop WHERE coin_raw_id=%s", [id ])
                cur.execute("DELETE FROM staketrx WHERE coin_raw_id=%s", [id ])
                cur.execute("DELETE FROM convertcoin WHERE fromid=%s or toid=%s", [id,id ])
                cur.execute("DELETE FROM airdropparticipate WHERE coin_raw_id=%s", [id ])
                mysql.commit()
                cur.close() 
                mysql.close()
                return jsonify({"success":"Coin Deleted Successfully"}) 
            else:
                return jsonify({"error":"Admin access only"})   
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"})

@app.route("/all-ccoin", methods=['GET', 'POST'])
def allccoin():   
    mysql = dbconnection()
    cur = mysql.cursor(dictionary=True,buffered=True)
    cur.execute("SELECT * FROM coin ORDER BY id DESC")
    coin = cur.fetchall()
    cur.close()
    mysql.close()
    if coin:
        return jsonify(coin)
    else:
        return([])

@app.route("/ccoin/<id>", methods=['GET', 'POST'])
def oneccoin(id):
    mysql = dbconnection()
    cur = mysql.cursor(dictionary=True,buffered=True)
    cur.execute("SELECT * FROM coin WHERE id=%s",[id])
    coin = cur.fetchall()
    cur.close()
    mysql.close()
    if coin:
        return jsonify(coin)
    else:
        return([])