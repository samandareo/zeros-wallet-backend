from apps import *
from apps.db import dbconnection

@app.route("/quiz/get", methods=['GET', 'POST'])
def quizget():
    mysql = dbconnection()
    cur = mysql.cursor(dictionary=True,buffered=True)
    cur.execute("SELECT * FROM quiz WHERE id=1")
    data = cur.fetchone()
    cur.close()
    mysql.close()
    if data:
        return jsonify(data)
    else:
        return jsonify({})

@app.route("/quiz/update", methods=['GET', 'POST'])
def quizup():
    if request.method == "POST":
        token = request.form['token']
        title = request.form['title']
        ques = request.form['ques']
        answer = request.form['answer']
        reward = request.form['reward']
        nexttime = datetime.now() + timedelta(hours=24)
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["uid"]
            uid = uid[:32]
            mysql = dbconnection()
            cur = mysql.cursor(dictionary=True,buffered=True)
            cur.execute("SELECT * FROM keystore WHERE uuid=%s",[uid])
            user = cur.fetchone()
            if user["type"]=="Admin":
                query=( title,ques,answer,reward,nexttime)
                cur.execute("UPDATE quiz SET title=%s,ques=%s,answer=%s,reward=%s,counttime=%s WHERE id=1",query)
                cur.execute("UPDATE keystore SET quiz=%s WHERE quiz=%s",("No","Yes"))
                mysql.commit()
                cur.close()
                mysql.close()
                return jsonify({"success":"Quiz updated successfully"}) 
            else:
                return jsonify({"error":"Admin access only"})   
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"}) 
    
@app.route("/quiz/check", methods=['GET', 'POST'])
def quizcheck():
    mysql = dbconnection()
    cur = mysql.cursor(dictionary=True,buffered=True)
    cur.execute("SELECT * FROM quiz WHERE id=1")
    data = cur.fetchone()
    danswer = data["answer"]
    reward = data["reward"]
    counttime = datetime.strptime(data["counttime"],"%Y-%m-%d %H:%M:%S.%f") 
    print(counttime,"Count Time")
    if request.method == "POST":
        token = request.form['token']
        answer = request.form['answer']
        currenttime = datetime.now()
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["uid"]
            uid = uid[:32]
            cur.execute("SELECT * FROM keystore WHERE uuid=%s",[uid])
            user = cur.fetchone()
            quiz = user["quiz"]
            id = user["id"]
            print(quiz,"Quiz")
            if quiz=="No":
                if danswer==answer and counttime>currenttime:
                    cur.execute("UPDATE wallet SET balance=balance + %s WHERE uid=%s and coin_id=%s",(reward ,id,"4"))
                    cur.execute("INSERT INTO payments (uid,coin_id,type,amount)" "VALUES(%s,%s,%s,%s)",(id,"4","Quiz",reward ))
                    cur.execute("UPDATE keystore SET quiz=%s WHERE id=%s",("Yes",id))
                    mysql.commit()
                    cur.close()
                    mysql.close()
                    return jsonify({"success":"Congratulations , your answer correct you have earned ZEROS Token"})  
                else:
                    cur.execute("UPDATE keystore SET quiz=%s WHERE id=%s",("Yes",id))
                    mysql.commit()
                    cur.close()
                    mysql.close()
                    return jsonify({"error":"Wrong answer try tomorrow"})  
            else:
                return jsonify({"error":"Something wrong try tomorrow"})      
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"})     
    
@app.route("/quiz/my", methods=['GET', 'POST'])
def quizmy():
    mysql = dbconnection()
    cur = mysql.cursor(dictionary=True,buffered=True)
    if request.method == "POST":
        token = request.form['token']
        try:
            decoded = jwt.decode(token, signing_key, algorithms=['HS512', 'HS256'])
            uid = decoded["uid"]
            uid = uid[:32]
            cur.execute("SELECT * FROM keystore WHERE uuid=%s",[uid])
            user = cur.fetchone()
            quiz = user["quiz"]
            return jsonify({"success":"Query success","quiz":quiz})       
        except:
            return jsonify({"error":"Invalid Token","quiz":"No"})  
    else:    
        return jsonify({"error":"Get Method not allow"})         