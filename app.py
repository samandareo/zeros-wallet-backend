from apps import app

@app.route("/")
def hello():
    return "Api"

if __name__ == "__main__":
    app.run(port=5000,host='0.0.0.0',debug=True, use_reloader=True,threaded= True)
	#SELECT * FROM `payments` WHERE payments.type='Task' and DATE(payments.created_at)=CURDATE();
    #DELETE FROM `payments` WHERE type='Referral Bonus';



