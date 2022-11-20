from flask import Flask,render_template,request,jsonify
import pickle
import config
import json
import numpy as np
from flask_mysqldb import MySQL
app = Flask(__name__)
# Will take user input >> HTML1 
# pip install flask_mysqldb
# PREDICTION AND USER >> DATABASE SQL
# HTML2 >> OUTPUT 
############################## MYSQL CONFIGURATION STEP####################
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "9876543210"
app.config["MYSQL_DB"] = "API_FOR_BOSTON"
mysql = MySQL(app)

with open(config.MODEL_FILE_PATH,"rb") as f:
    model = pickle.load(f)
with open(config.SCALING_FILE_PATH,"rb") as file:
    std_scalar = pickle.load(file)
with open(config.JSON_FILE_PATH,"r") as file:
    json_data = json.load(file)
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict1",methods = ["GET","POST"])
def predict():
    data = request.form
    test_array = np.zeros(13)
    test_array[0] = int(data['CRIM'])
    a = test_array[0]
    test_array[1] = int(data['ZN'])
    b = test_array[1]
    test_array[2] = int(data['INDUS'])
    c = test_array[2]
    test_array[3] = int(data['CHAS'])
    d = test_array[3]
    test_array[4] = int(data['NOX'])
    e = test_array[4]
    test_array[5] = int(data['RM'])
    f = test_array[5]
    test_array[6] = int(data['AGE'])
    g = test_array[6]
    test_array[7] = int(data['DIS'])
    h = test_array[7]
    test_array[8] = int(data['RAD'])
    i = test_array[8]
    test_array[9] = int(data['TAX'])
    j = test_array[9]
    test_array[10] = int(data['PTRATIO'])
    k = test_array[10]
    test_array[11] = int(data['B'])
    l = test_array[11]
    test_array[12] = int(data['LSTAT'])
    m = test_array[12]
    std_array = std_scalar.transform([test_array])
    # print(std_scalar)
    z = model.predict(std_array)
    z1 = np.round(z[0],2)
    cursor = mysql.connection.cursor()
    query = 'CREATE TABLE IF NOT EXISTS Evening_batch_house(CRIM VARCHAR(20),ZN VARCHAR(20),INDUS VARCHAR(20),CHAS VARCHAR(20),NOX VARCHAR(20),RM VARCHAR(20),AGE VARCHAR(20),DIS VARCHAR(20),RAD VARCHAR(20),TAX VARCHAR(20),PTRATIO VARCHAR(20),B VARCHAR(20),LSTAT VARCHAR(20),PRICE VARCHAR(20))'
    cursor.execute(query)
    cursor.execute('INSERT INTO Evening_batch_house(CRIM,ZN,INDUS,CHAS,NOX,RM,AGE,DIS,RAD,TAX,PTRATIO,B,LSTAT,PRICE) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(a,b,c,d,e,f,g,h,i,j,k,l,m,z1))

    mysql.connection.commit()
    cursor.close()

    return render_template("index1.html",z1=z1)

if __name__ =="__main__":
    app.run(host="0.0.0.0",port=config.PORT_NUMBER)
