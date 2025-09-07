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
     file_path = os.path.join(current_app.root_path, 'static/images-blog', photo_name)
     photo.save(file_path)
     return photo_name

@app.route("/add-blog", methods=['GET', 'POST'])
def blogadd():
    if request.method == "POST":
        token = request.form['token']
        title = request.form['title']
        des = request.form['des']
        type = request.form['type']
        route = request.form['route']
        navigate = request.form['navigate']
        img = request.form['img']
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
                    cur.execute("INSERT INTO blog (title,des,img,type,route,navigate)" 
                                 "VALUES(%s,%s,%s,%s,%s,%s)",
                                 (title,des,img,type,route,navigate))
                    mysql.commit()
                    cur.close()
                    mysql.close()
                    return jsonify({"success":"Blog Added Successfully"}) 
                except:
                    cur.execute("INSERT INTO blog (title,des,img,type,route,navigate)" 
                                 "VALUES(%s,%s,%s,%s,%s,%s)",
                                 (title,des,img,type,route,navigate))
                    mysql.commit()
                    cur.close()
                    mysql.close()
                    return jsonify({"success":"Blog Added Successfully"})                       
            else:
                return jsonify({"error":"Admin access only"})   
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"})
    
@app.route("/update-blog", methods=['GET', 'POST'])
def blogupdate():
    if request.method == "POST":
        token = request.form['token']
        title = request.form['title']
        des = request.form['des']
        type = request.form['type']
        route = request.form['route']
        navigate = request.form['navigate']
        img = request.form['img']
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
                    cur.execute("UPDATE blog SET title=%s,des=%s,img=%s,type=%s,route=%s,navigate=%s WHERE id=%s", 
                                (title,des,img,type,route,navigate, id ))
                    mysql.commit()
                    cur.close()
                    mysql.close()
                    return jsonify({"success":"Blog Updated Successfully 1"})
                except:
                    cur.execute("UPDATE blog SET title=%s,des=%s,img=%s,type=%s,route=%s,navigate=%s WHERE id=%s", 
                                (title,des,img,type,route,navigate, id ))
                    mysql.commit()
                    cur.close()
                    mysql.close()
                    return jsonify({"success":"Blog Updated Successfully 0"}) 
            else:
                return jsonify({"error":"Admin access only"})   
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"})    

@app.route("/delete-blog", methods=['GET', 'POST'])
def deleteblog():
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
                cur.execute("DELETE FROM blog WHERE id=%s", [id ])
                mysql.commit()
                cur.close()
                mysql.close()
                return jsonify({"success":"Blog Deleted Successfully"})
            else:
                return jsonify({"error":"Admin access only"})   
        except:
            return jsonify({"error":"Invalid Token"})  
    else:    
        return jsonify({"error":"Get Method not allow"})    
    
@app.route("/all-blog", methods=['GET', 'POST'])
def allblog():
    mysql = dbconnection()
    cur = mysql.cursor(dictionary=True,buffered=True)
    cur.execute("SELECT * FROM blog ORDER BY id DESC")
    blog = cur.fetchall()
    cur.close()
    mysql.close()
    if blog:
        print(len(blog))
        return jsonify(blog)
    else:
        return({"error":"Query Failed"})

@app.route("/blog/<id>", methods=['GET', 'POST'])
def oneblog(id):
    mysql = dbconnection()
    cur = mysql.cursor(dictionary=True,buffered=True)
    cur.execute("SELECT * FROM blog WHERE id=%s",[id])
    blog = cur.fetchall()
    cur.close()
    mysql.close()
    if blog:
        print(len(blog))
        return jsonify(blog)
    else:
        return({"error":"Query Failed"})