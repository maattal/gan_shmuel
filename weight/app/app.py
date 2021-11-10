from flask import Flask
from flask_restful import Api, Resource
import mysql.connector 
from flask import request,Response
import csv
from flask import jsonify
import os,sys,json
from datetime import datetime

app = Flask(__name__)
api = Api(app)  

def init():
    return mysql.connector.connect(
        host='db',
        database='db',
        user='root',
        password='root'
    )

@app.route("/health", methods=["GET"])
def get_health():
    return "ok"

@app.route("/", methods=["GET"])
def get():
    connect = init()
    cur = connect.cursor()
    cur.execute("SHOW TABLES;")
    rows = cur.fetchall()
    resp = jsonify(rows)
    resp.status_code = 200
    return resp

@app.route("/session/<id>", methods=["GET"])
def get_session(id):
    conn = init()
    mycursor = conn.cursor()
    mycursor.execute(f"SELECT * FROM sessions WHERE id='{id}'")
    check = mycursor.fetchall()
    content = {}
    if check != []:
        if check[0][1] != 'out':
            content = {'id': check[0][0], 'truck': check[0][6], 'bruto': check[0][4]}
        else:
            content = {'id': check[0][0], 'truck': check[0][6], 'bruto': check[0][4], 'truckTara': check[0][4]-check[0][5], 'neto': check[0][5]}
        return jsonify(content)
    return "none", 404

@app.route('/batch-weight',methods = ['POST'])
def get_batch_weight():
    conn = init()
    cursor = conn.cursor()
    file_name="/app/in/"+request.args.get('filename')
    l_csv = []

    if file_name[-4:] =='.csv':
        with open(file_name, 'r') as file:
            header = file.readline()[:-1].split(",")
            unit = header[1]
            for line in file:
                csv_js={}
                csv_js["id"]=line[:-1].split(",")[0]
                csv_js["weight"]=int(line[:-1].split(",")[1])
                csv_js["unit"]=unit[1:-1]
                l_csv.append(csv_js)
    else:
        try:
            with open(file_name, 'r') as file:
                data = file.read()
                l_csv = json.loads(data)
        except:
            return "error with file"
    q = "INSERT INTO containers (id,weight,unit) VALUES (%s,%s,%s) ; \n"
    for csv_j in l_csv:
        cursor.execute(q, [csv_j['id'],csv_j['weight'],csv_j['unit']])
    conn.commit()
    return "ok"

@app.route('/item/<id>',methods = ['GET'])
def get_item(id):
    connect = init()
    cur = connect.cursor(dictionary=True, buffered=True)
    fromTime = request.args.get('from') if request.args.get('from') else datetime.now().strftime("%Y%m%d000000")
    toTime = request.args.get('to') if request.args.get('to') else datetime.now().strftime("%Y%m%d%H%M%S")
    session = { 
        "id":int(id),
        "tara":0,
        "sessions":[]
    }

    query_truck = f"SELECT bruto,neto,id,date FROM sessions WHERE trucks_id='{id}' AND date BETWEEN '{fromTime}' AND '{toTime}';"
    #want to add a query_container
    cur.execute(query_truck)
    res=cur.fetchall()

    if not res: #error case 
        session["id"] = 404,
        session["tara"] = 'N/A'
    for ind in range(len(res)):
        session["tara"] += float(res[ind]["bruto"]) - float(res[ind]["neto"])
        session["sessions"].append(res[ind]["id"])

    return jsonify(session)

@app.route('/weight',methods = ['GET'])
def get_weight():
    connect = init()
    cur = connect.cursor(dictionary=True, buffered=True)
    fromTime = request.args.get('from') if request.args.get('from') else datetime.now().strftime("%Y%m%d000000")
    toTime = request.args.get('to') if request.args.get('to') else datetime.now().strftime("%Y%m%d%H%M%S")
    filter = request.args.get('filter') if request.args.get('filter') else None 

    query="SELECT id,direction,bruto,neto,products_id FROM sessions WHERE date BETWEEN '{0}' AND '{1}' AND direction = '{2}';"
    cur.execute(query.format(fromTime, toTime, filter))
    rows = cur.fetchall()
    return jsonify(rows)

# @app.route('/weight',methods = ['POST'])
# def post_weight():
#     pass

# @app.route('/unknown',methods = ['GET'])
# def get_unknown():
#     pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

