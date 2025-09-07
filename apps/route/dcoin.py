from apps import *
from apps.db import dbconnection

def save_images(photo):
     hash_photo = secrets.token_urlsafe(10)
     _, file_extention = os.path.splitext(photo.filename)
     photo_name = hash_photo + file_extention
     #print(file_extention)
     if file_extention=="" or file_extention==None:
         return ""
     file_path = os.path.join(current_app.root_path, 'static/images', photo_name)
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


@app.route("/add-coin", methods=['GET', 'POST'])
def coinadd():
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
                    cur.execute("INSERT INTO dcoin (coin_name,coin_symbol,coin_decimal,contract,coin_type,code,price,logo,platform,deposit,withdrew,status,swap,explorer,fund_address,fee_coin,fee)" 
                                 "VALUES(%s,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                 (coin_name,coin_symbol,coin_decimal,contract,coin_type,code,price,logo,platform,deposit,withdrew,status,swap,explorer,fund_address,fee_coin,fee ))
                    mysql.commit()
                    cur.close()
                    mysql.close()
                    return jsonify({"success":"Coin Added Successfully"}) 
                except:
                    cur.execute("INSERT INTO dcoin (coin_name,coin_symbol,coin_decimal,contract,coin_type,code,price,logo,platform,deposit,withdrew,status,swap,explorer,fund_address,fee_coin,fee)" 
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
    
@app.route("/update-coin", methods=['GET', 'POST'])
def updatecoin():
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
                cur.execute("SELECT * FROM dcoin WHERE id=%s",[id])
                coin = cur.fetchone()
                #request.files['logo_img']
                try:   
                    cur.execute("UPDATE dcoin SET coin_name=%s,coin_symbol=%s,coin_decimal=%s,contract=%s,coin_type=%s,code=%s,price=%s,logo=%s,platform=%s,deposit=%s,withdrew=%s,status=%s,swap=%s,explorer=%s,fund_address=%s,fee_coin=%s,fee=%s WHERE id=%s", 
                                (coin_name,coin_symbol,coin_decimal,contract,coin_type,code,price,logo,platform,deposit,withdrew,status,swap,explorer,fund_address,fee_coin,fee, id ))
                    mysql.commit()
                    cur.close()
                    mysql.close()
                    return jsonify({"success":"Coin Updated Successfully"}) 
                except:
                    cur.execute("UPDATE dcoin SET coin_name=%s,coin_symbol=%s,coin_decimal=%s,contract=%s,coin_type=%s,code=%s,price=%s,logo=%s,platform=%s,deposit=%s,withdrew=%s,status=%s,swap=%s,explorer=%s,fund_address=%s,fee_coin=%s,fee=%s WHERE id=%s", 
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

@app.route("/delete-coin", methods=['GET', 'POST'])    
def deletecoin():
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
                cur.execute("DELETE FROM dcoin WHERE id=%s", [id ])
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

@app.route("/all-coin", methods=['GET', 'POST'])
def allcoin():   
    mysql = dbconnection()
    cur = mysql.cursor(dictionary=True,buffered=True)
    cur.execute("SELECT * FROM dcoin ORDER BY id ASC")
    coin = cur.fetchall()
    cur.close()
    mysql.close()
    if coin:
        return jsonify(coin)
    else:
        return([])

@app.route("/coin/<id>", methods=['GET', 'POST'])
def onecoin(id):
    mysql = dbconnection()
    cur = mysql.cursor(dictionary=True,buffered=True)
    cur.execute("SELECT * FROM dcoin WHERE id=%s",[id])
    coin = cur.fetchall()
    cur.close()
    mysql.close()
    if coin:
        return jsonify(coin)
    else:
        return([])

def getPrice():
    allcode=[]
    mysql = dbconnection()
    cur = mysql.cursor(dictionary=True,buffered=True)
    cur.execute("SELECT * FROM dcoin ORDER BY id DESC")
    coin = cur.fetchall()
    for i in coin:
        allcode.append(i["code"])
    #print(allcode)
    url = "https://api.livecoinwatch.com/coins/map"
    payload = json.dumps({
     "codes": allcode,
     "currency": "USD",
     "sort": "rank",
     "order": "ascending",
     "offset": 0,
     "limit": 0,
     "meta": False
    })
    #print(allcode)
    headers = {
      'content-type': 'application/json',
      'x-api-key': os.getenv('LIVECOINWATCH_API_KEY', '')
      }
    response = requests.request("POST", url, headers=headers, data=payload)
    dv = response.json()  
    mysql = dbconnection()
    for d in response.json():
        print(d)
        code = d["code"]
        rate = float(d["rate"])
        rate = "%.8f" % rate
        ch = float(d["delta"]["day"]-1)* 100
        change = "%.2f" % ch
        #print(change)
        cur = mysql.cursor(dictionary=True,buffered=True)
        cur.execute("UPDATE dcoin SET price=%s,day_change=%s WHERE code=%s", (rate,change,code ))
        cur.execute("UPDATE coin SET price=%s,day_change=%s WHERE code=%s", (rate,change,code ))
        mysql.commit()
        print("Price Updated")
    cur.close()   
    mysql.close()    
  
priceuptime = datetime.now()
@app.route("/coin-price", methods=['GET', 'POST'])
def pricecoin():
    currenttime = datetime.now()
    global priceuptime
    try:
        if currenttime>priceuptime:
            getPrice()
            priceuptime = datetime.now() + timedelta(minutes=1)
        else:
            print("Wait for next time to update price")     
    except:
        print("Price update error")   
        priceuptime = datetime.now() + timedelta(minutes=1)    
    return jsonify({"success":"price Updated"}) 