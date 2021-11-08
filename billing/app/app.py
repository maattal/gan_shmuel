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

# @app.route('/provider/<pro_name>',methods = ['POST'])
# def creat_provider(pro_name):
#     conn = init_db()
#     mycursor = conn.cursor()
#     mycursor.execute("INSERT INTO 'Provider' ('name') VALUES (%s)")
#     return "ok" 


@app.route('/health',methods = ['GET'])
def health():
 return 'ok'




if __name__ == '__main__':
    app.run(host="0.0.0.0",debug = False)


@app.route('/truck/<id>', methods=['GET'])
def get_truck_id(id):
    now = datetime.now()
    time = now.strftime("%Y%m")
    test_id = id
    _from = request.args.get('from')
    _to = request.args.get('to')
    if not _to:
        _to = now.strftime("%Y%m%d%H%M%S")
        # _to=11111111111111
    if not _from:
        _from = time + '01000000'
        # _from=88888888888888
    connect = init_db()  
    cursor = connect.cursor() 
    # try:
    int_id=int(id)
    query=f"SELECT DISTINCT neto FROM sessions WHERE date=(SELECT MAX(date) FROM sessions WHERE trucks_id={int_id});"
    cursor.execute(query) 
    netoCursor = cursor.fetchall()
    query_sessions=f"SELECT id FROM sessions WHERE trucks_id={int_id} AND date BETWEEN {_from} AND {_to};"
    cursor.execute(query_sessions) 
    rows=[] 
    rows = cursor.fetchall()
    session={
    "id":0,
    "tara":0,
    }
    if not rows:
        session["id"] = 404,
        session["tara"] = 'N/A' 
    else:
        session = { 
        "id":int(test_id),
        "tara":netoCursor[0],
        "sessions":[]
        }  
        for i in range(0, len(rows)):
             session["sessions"].append(rows[i]["id"])
    resp = jsonify(session)
    resp.status_code = 200
    return resp
    # except:
    #     getContainerWeight=f"SELECT weight FROM containers WHERE id='{test_id}';"
    #     cursor.execute(getContainerWeight) 
    #     ContainerWeight = cursor.fetchall()
    #     #to fixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    #     query=f"SELECT sessions_id FROM containers_has_sessions WHERE containers_id='{test_id}' AND (SELECT date FROM sessions WHERE id=sessions_id) BETWEEN {_from} AND {_to};"
    #     cursor.execute(query)
    #     rows=[] 
    #     rows = cursor.fetchall()
    #     session={
    #     "id":0,
    #     "tara":0,
    #     }
    #     if not rows:
    #         session["id"] = 404,
    #         session["tara"] = 'N/A' 
    #     else:
    #         session = { 
    #         "id":test_id,
    #         "tara":ContainerWeight[0],
    #         "sessions":[]
    #         } 
    #         for i in range(0, len(rows)):
    #              session["sessions"].append(rows[i]["sessions_id"])
    #     resp = jsonify(session)
    #     resp.status_code = 200
    #     return resp
    
