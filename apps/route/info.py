from apps import *
from apps.db import dbconnection
import os


@app.route("/add-info", methods=['GET', 'POST'])
def infoadd():
    if request.method == "POST":
        token = request.form['token']
        title = request.form['title']
        des = request.form['des']
        route = request.form['route']
        navigate = request.form['navigate']
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["uid"]
            uid = uid[:32]
            mysql = dbconnection()
            cur = mysql.cursor(dictionary=True,buffered=True)
            cur.execute("SELECT * FROM keystore WHERE uuid=%s",[uid])
            user = cur.fetchone()
            if user["type"]=="Admin":
                    cur.execute("INSERT INTO info (title,des,route,navigate)" 
                                 "VALUES(%s,%s,%s,%s)",
                                 (title,des,route,navigate))
                    mysql.commit()
                    cur.close()
                    mysql.close()
                    return jsonify({"success":"info Added Successfully"})                       
            else:
                return jsonify({"error":"Admin access only"})   
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"})
    
@app.route("/update-info", methods=['GET', 'POST'])
def infoupdate():
    if request.method == "POST":
        token = request.form['token']
        title = request.form['title']
        des = request.form['des']
        route = request.form['route']
        navigate = request.form['navigate']
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
                    cur.execute("UPDATE info SET title=%s,des=%s,route=%s,navigate=%s WHERE id=%s", (title,des,route,navigate,id ))
                    mysql.commit()
                    cur.close()
                    mysql.close()
                    return jsonify({"success":"info Updated Successfully "}) 
            else:
                return jsonify({"error":"Admin access only"})   
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"})    

@app.route("/delete-info", methods=['GET', 'POST'])
def deleteinfo():
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
                cur.execute("DELETE FROM info WHERE id=%s", [id ])
                mysql.commit()
                cur.close()
                mysql.close()
                return jsonify({"success":"info Deleted Successfully"})
            else:
                return jsonify({"error":"Admin access only"})   
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"})    
    
@app.route("/all-info", methods=['GET', 'POST'])
def allinfo():
    mysql = dbconnection()
    cur = mysql.cursor(dictionary=True,buffered=True)
    cur.execute("SELECT * FROM info ORDER BY id DESC")
    info = cur.fetchall()
    cur.close()
    mysql.close()
    if info:
        print(len(info))
        return jsonify(info)
    else:
        return({"error":"Query Failed"})

@app.route("/info/<id>", methods=['GET', 'POST'])
def oneinfo(id):
    mysql = dbconnection()
    cur = mysql.cursor(dictionary=True,buffered=True)
    cur.execute("SELECT * FROM info WHERE id=%s",[id])
    info = cur.fetchall()
    cur.close()
    mysql.close()
    if info:
        print(len(info))
        return jsonify(info)
    else:
        return({"error":"Query Failed"})