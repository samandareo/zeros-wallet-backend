from apps import *
from apps.db import dbconnection
from apps.route.wallet import walletcreate
import os


@app.route("/createwallet", methods=['GET', 'POST'])
def createwallet():
    if request.method == "GET":
        return jsonify({"error":"Get method not allow"})
    
    mysql = dbconnection()
    cur = mysql.cursor(dictionary=True,buffered=True)
    
    #Keystore Acc
    uid = str(uuid.uuid4().hex)
    print(uid[-2:])
    print(uid[:32])
    client_host = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    print(client_host)

    kg = blocksmith.KeyGenerator()
    key = kg.generate_key()
    address = blocksmith.EthereumWallet.generate_address(key)
    checksum_address = blocksmith.EthereumWallet.checksum_address(address)
    ethkey1pass = cryptocode.encrypt(str(key),privatepass)
    print("Eth Key : ",key)
    print("Eth address : ",checksum_address)
    new_account = Keypair()
    solkey1pass = cryptocode.encrypt(str(new_account.private_key),privatepass)
    solkey1 = new_account.private_key
    solaadd= new_account.public_key
    print("Sol Private Key : ",solkey1)
    print("Sol Address : ",solaadd)
    
    print("uid : ",uid)
    passw = generate_password_hash(uid+uid[-2:]) 
    print("Password : ",passw)
    print(check_password_hash(passw,uid+uid[-2:]))

    #Account
    key2 = kg.generate_key()
    address2 = blocksmith.EthereumWallet.generate_address(key2)
    checksum_address2 = blocksmith.EthereumWallet.checksum_address(address2)
    ethkey2pass = cryptocode.encrypt(str(key2),privatepass)
    print("Eth Key 2 : ",key2)
    print("Eth Address 2 : ",checksum_address2)
    new_account2 = Keypair()
    solkey2 = new_account2.private_key
    soladdress2 = new_account2.public_key
    print("Sol Private Key 2 : ",solkey2)
    print("Sol Address 2 : ",soladdress2)
    solkey2pass = cryptocode.encrypt(str(new_account2.private_key),privatepass)

    refcode = uid[:10]

    try:
        mysql.autocommit = True
        mysql.start_transaction()  
        cur.execute("INSERT INTO keystore (uuid,key1, solkey,password,ethaddress,soladdress,rip,lip,refcode)" "VALUES(%s,%s, %s,%s,%s,%s,%s,%s,%s)",
                            (uid,str(ethkey1pass),str(solkey1pass),passw,str(checksum_address),str(solaadd),client_host,client_host,refcode ))
        mysql.commit()
        user_id = cur.lastrowid
        print("Last ID :",user_id)
        cur.execute("INSERT INTO acc (uuid,user_id, solkey,ethkey,eth_address,sol_address,rip,lip)" "VALUES(%s,%s, %s,%s,%s,%s,%s,%s)",
                            (uid,user_id,str(solkey2pass),str(ethkey2pass),str(checksum_address2),str(soladdress2),client_host,client_host ))
        mysql.commit()

        message = {
              'uid': uid+uid[-2:],
              "user_id":user_id,
              "usertype":"User",
              "refcode":refcode,
              "key1":str(key),
              "solkey1":str(solkey1),
              "ethaddress1":str(checksum_address),
              "soladdress1":str(solaadd),
              "key2":str(key2),
              "solkey2":str(solkey1),
              "ethaddress2":str(checksum_address2),
              "soladdress2":str(soladdress2),
              "iss":"",
              "iat": datetime.now(tz=timezone.utc),
              "exp": datetime.now(tz=timezone.utc) + timedelta(days=365)
              }
        encoded_jwt = jwt.encode(message,signing_key, algorithm='HS256')#.decode('utf-8')

        return jsonify({"success":"Successfully Login","token":encoded_jwt})
    
    except mysql.connector.Error as error:
        mysql.rollback()    
        print("Wallet RollBack") 
        return jsonify({"error":"Not Login"})

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        mysql = dbconnection()
        cur = mysql.cursor(dictionary=True,buffered=True)
        uid = request.form['uid']
        cur.execute("SELECT * FROM keystore WHERE uuid=%s",[uid[:32]])
        data = cur.fetchone()

        cur.execute("SELECT * FROM acc WHERE uuid=%s",[uid[:32]])
        data1 = cur.fetchone()

        if data:
            if check_password_hash(data['password'], uid):
                message = {
                    'uid': uid,
                    "user_id":data['id'],
                    "usertype":data['type'],
                    "refcode":data["refcode"],
                    "key1":str(cryptocode.decrypt(data["key1"],privatepass)),
                    "solkey1":str(cryptocode.decrypt(data["solkey"],privatepass)),
                    "ethaddress1":str(data["ethaddress"]),
                    "soladdress1":str(data["soladdress"]),
                    "key2":str(cryptocode.decrypt(data1["ethkey"],privatepass)),
                    "solkey2":str(cryptocode.decrypt(data1["solkey"],privatepass)),
                    "ethaddress2":str(data1["eth_address"]),
                    "soladdress2":str(data1["sol_address"]),
                    "iss":"",
                    "iat": datetime.now(tz=timezone.utc),
                    "exp": datetime.now(tz=timezone.utc) + timedelta(days=365)
                }
                encoded_jwt = jwt.encode(message,signing_key, algorithm='HS256')#.decode('utf-8')   
                return jsonify({"success":"Successfully Login","token":encoded_jwt})
            else:
                return jsonify({"error":"Invalid key"})
        else:
             return jsonify({"error":"Invalid key"})
    
    else:
        return jsonify({"error":"Get method not allow"})