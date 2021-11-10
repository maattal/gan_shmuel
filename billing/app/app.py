from flask import Flask,request, jsonify
import os,sys,json
import mysql.connector
from datetime import datetime
from openpyxl import  load_workbook



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
    try:
        pro_id=request.args.get('providerid')
        pro_lic=request.args.get('truckid')
        conn = init_db()
        mycursor = conn.cursor()
        query = (f"INSERT INTO trucks (truckid,providerid) VALUES ('{pro_lic}','{pro_id}')")
        mycursor.execute(query)
        conn.commit()
        return 'ok'
    except:
        return "ProviderID not Found"


@app.route('/health',methods = ['GET'])
def health():
    try:
        connect = init_db()  
        # mycursor = connect.cursor()  
        # mycursor.execute("show tables")
        # res = str(mycursor.fetchall())
    except:
        return "failed connecting to the database", 500
    else:
        return "WELCOME DATA CONNECTION WORKS" ,200


@app.route("/rates", methods=['POST'])
def upload_xl_data():
    filename="in/"+request.args.get('filename')

    connect = init_db()  
    cur = connect.cursor()  
    book = load_workbook(filename)
    sheet = book.active

    query = """REPLACE INTO products (product_name, rate, scope) VALUES (%s , %s, %s)"""

    for r in sheet.iter_rows(2, sheet.max_row):
        product_id = r[0].value
        rate = r[1].value
        scope = r[2].value
        values=(product_id,rate,scope)
        cur.execute(query,values)

    connect.commit()
    return "a"



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
    try:
        pro_id=request.args.get('providerid')
        pro_lic=request.args.get('truckid')
        conn = init_db()
        mycursor = conn.cursor()
        query = (f"INSERT INTO trucks (truckid,providerid) VALUES ('{pro_lic}','{pro_id}')")
        mycursor.execute(query)
        conn.commit()
        return 'ok'
    except:
        return "ProviderID not Found"
@app.route('/truck/<id>',methods = ['PUT'])
def put_truck_id():
    return 'ok'



@app.route('/truck/<id>', methods=['GET'])
def itemId(id):
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
    conn = init_db()
    cursor = conn.cursor()
    # ty:
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
            session["sessions"].append(rows[i])
    resp = jsonify(session)
    resp.status_code = 200
    return resp





if __name__ == '__main__':
    app.run(host="0.0.0.0",debug = False)





    
