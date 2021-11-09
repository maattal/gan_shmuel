from flask import Flask,request, jsonify
import os,sys,json
import mysql.connector
from datetime import datetime

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
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



@app.route('/provider/<id>',methods = ['PUT'])
def update_name(id):
    try:
        new_name=request.args.get('name')
        conn = init_db()
        mycursor = conn.cursor()
        query = (f"UPDATE providers SET providername = '{new_name}' WHERE id = '{id}'")
        mycursor.execute(query)
        conn.commit()
    except:
        return "Name already exists"
    else:   
        return "OK"
       

@app.route('/provider',methods = ['POST'])
def creat_provider():
    try:
        pro_name=request.args.get('name')
        conn = init_db()
        mycursor = conn.cursor()
        query = (f"INSERT INTO providers (providername) VALUES ('{pro_name}')")
        mycursor.execute(query)
        conn.commit()
    except:
        return "Name already exists"    
    else:
        mycursor.execute(f"SELECT * FROM providers WHERE providername = '{pro_name}';")
        rows = mycursor.fetchmany(size=1)
        resp = jsonify(rows)
        resp.status_code = 200
        return resp

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





    
