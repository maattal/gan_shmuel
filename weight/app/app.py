from flask import Flask, request, jsonify
from flask_restful import Api
from datetime import datetime
import mysql.connector 
import json


app = Flask(__name__)
api = Api(app)  

#initialize connection to data base.
def init():
    return mysql.connector.connect(
        host='db',
        database='db',
        user='root',
        password='root'
    )

#checks server status.
@app.route("/health", methods=["GET"])
def get_health():
    return "ok"

#loads tables from database.
@app.route("/", methods=["GET"])
def get():
    connect = init() #connects to the db
    cur = connect.cursor()
    cur.execute("SHOW TABLES;")
    rows = cur.fetchall()
    resp = jsonify(rows)
    resp.status_code = 200
    return resp

#returns documentation for specific session by id.
@app.route("/session/<id>", methods=["GET"])
def get_session(id):
    conn = init() # connection to db
    mycursor = conn.cursor()
    mycursor.execute(f"SELECT * FROM sessions WHERE id='{id}'") #access all of the session data by id.
    check = mycursor.fetchall()
    content = {}
    if check != []:
        if check[0][1] != 'out': #if not out
            content = {'id': check[0][0], 'truck': check[0][6], 'bruto': check[0][4]}
        else: # if out
            content = {'id': check[0][0], 'truck': check[0][6], 'bruto': check[0][4], 'truckTara': check[0][4]-check[0][5], 'neto': check[0][5]}
        return jsonify(content)
    return "none", 404 #not existing

#posts weights of new containers, reads from a given(csv/json) file
@app.route('/batch-weight',methods = ['POST'])
def get_batch_weight():
    conn = init() # connection to db
    cursor = conn.cursor()
    file_name="/app/in/"+request.args.get('filename') #file path.
    l_csv = []

    if file_name[-4:] =='.csv': #csv
        with open(file_name, 'r') as file:
            header = file.readline()[:-1].split(",")
            unit = header[1]
            for line in file:
                csv_js={}
                csv_js["id"]=line[:-1].split(",")[0]
                csv_js["weight"]=int(line[:-1].split(",")[1])
                csv_js["unit"]=unit[1:-1]
                l_csv.append(csv_js)
    else: #json
        try:
            with open(file_name, 'r') as file:
                data = file.read()
                l_csv = json.loads(data)
        except: #error
            return "error with file"

    q = "INSERT INTO containers (id,weight,unit) VALUES (%s,%s,%s) ; \n" #appends to 'containers' values from the file.
    for csv_j in l_csv:
        cursor.execute(q, [csv_j['id'],csv_j['weight'],csv_j['unit']])
    conn.commit() #updates the db.
    return "ok"

#return info about given truck id between specific time-stamps, if not existing 404 will be returned.
@app.route('/item/<id>',methods = ['GET'])
def get_item(id):
    connect = init() #db connection
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

#returns weight sessions between two time stamps.
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
    if not rows: return "not existing."
    return jsonify(rows)

#returns list of id's for all containers with an unknown weight.
@app.route('/unknown',methods = ['GET'])
def get_unknown():
    conn = init()
    cur = conn.cursor()
    cur.execute("SELECT id FROM containers WHERE weight IS NULL")
    rows = cur.fetchall()

    if not rows:
	    return "No missing weights found in data base"
    return str(list(map(lambda x: str(x[0]), rows)))

# @app.route('/weight',methods = ['POST'])
# def post_weight():
#     pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

