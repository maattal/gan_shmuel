from flask import Flask,request, jsonify
import os,sys,json
import mysql.connector
from datetime import datetime

app = Flask(__name__)


# db contenction
def init_db():
    return mysql.connector.connect(
        host='db',
        database='db',
        user='root',
        password='root'
    )


@app.route('/',methods = ['GET'])
def index():
    # return 'ko'
    connect = init_db()  
    cur = connect.cursor()  
    cur.execute("SHOW TABLES;")
    rows = cur.fetchall()
    resp = jsonify(rows)
    resp.status_code = 200
    return resp
    # connect.close()



@app.route('/truck',methods = ['POST'])
def creat_truck():
    pro_id=request.args.get('providerid')
    pro_lic=request.args.get('truckid')
    conn = init_db()
    mycursor = conn.cursor()
    query = (f"INSERT INTO trucks (truckid,providerid) VALUES ('{pro_lic}','{pro_id}')")
    mycursor.execute(query)
   # query = (f"INSERT INTO trucks (truckid) VALUES ('{pro_lic}')")
  #  mycursor.execute(query)
    conn.commit()
    return 'ok'


@app.route('/health',methods = ['GET'])
def health():
 return 'ok'




if __name__ == '__main__':
    app.run(host="0.0.0.0",debug = False)





    
