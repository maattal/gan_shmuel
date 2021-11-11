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

#checks server status.
@app.route("/health", methods=["GET"])
def get_health():
    try:
        conn = init()
        mycursor = conn.cursor(dictionary=True, buffered=True)
        mycursor.execute("show tables")
        res = str(mycursor.fetchall())
    except:
        return "failed", 500
    else:
        return "connection-ok" ,200

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

#return info about given truck id between specific time-stamps, if not existing 404 will be returned.
@app.route('/item/<id>',methods = ['GET'])
def get_item(id):
    connect = init() #db connection
    cur = connect.cursor(dictionary=True, buffered=True)
    fromTime = request.args.get('from') if request.args.get('from') else datetime.now().strftime("%Y%m%d000000")
    toTime = request.args.get('to') if request.args.get('to') else datetime.now().strftime("%Y%m%d%H%M%S")
    
    try:
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
            session["tara"] = 'na'
        for ind in range(len(res)):
            session["tara"] += float(res[ind]["bruto"]) - float(res[ind]["neto"])
            session["sessions"].append(res[ind]["id"])

        return jsonify(session)
    except:
        getContainerWeight=f"SELECT weight FROM containers WHERE id='{id}';"
        cur.execute(getContainerWeight) 
        ContainerWeight = cur.fetchall()
        query=f"SELECT sessions_id FROM containers_has_sessions WHERE containers_id='{id}' AND (SELECT date FROM sessions WHERE id=sessions_id) BETWEEN {fromTime} AND {toTime};"
        cur.execute(query)
        rows=[] 
        rows = cur.fetchall()
        session={
        "id":0,
        "tara":0,
        }
        if not rows:
            session["id"] = 404,
            session["tara"] = 'N/A' 
        else:
            session = { 
            "id":id,
            "tara":ContainerWeight[0],
            "sessions":[]
            } 
            for i in range(0, len(rows)):
                 session["sessions"].append(rows[i]["sessions_id"])
        resp = jsonify(session)
        resp.status_code = 200
        return resp

#returns weight sessions between two time stamps.
@app.route('/weight',methods = ['GET'])
def get_weight():
    connect = init()
    cur = connect.cursor(dictionary=True, buffered=True)
    fromTime = request.args.get('from') if request.args.get('from') else datetime.now().strftime("%Y%m%d000000")
    toTime = request.args.get('to') if request.args.get('to') else datetime.now().strftime("%Y%m%d%H%M%S")
    filter = f"('{request.args.get('filter')}')" if request.args.get('filter') else "('in' , 'out' , 'none')" 
     
    query="""SELECT t1.id, direction, bruto, neto, product_name, GROUP_CONCAT(t3.containers_id) as containers 
    FROM sessions AS t1 JOIN products AS t2 ON t1.products_id = t2.id 
    JOIN containers_has_sessions as t3 ON t1.id = t3.sessions_id 
    WHERE t1.date BETWEEN '{0}' AND '{1}' AND direction IN {2} GROUP BY t3.sessions_id"""
    cur.execute(query.format(fromTime, toTime, filter))
    rows = cur.fetchall()
    return jsonify(rows)

@app.route('/weight',methods = ['POST'])
def post_weight():
    session_id=0
    conn = init() # set connection
    cursor = conn.cursor(dictionary=True, buffered=True)
    # set variables
    direction=request.args.get('direction')
    containers=request.args.get('containers')
    weight=request.args.get('weight')
    unit=request.args.get('unit')
    force=request.args.get('force')
    product=request.args.get('product')
    truck_id=request.args.get('truckid')
    date = datetime.now().strftime('%Y%m%d%H%M%S')
    
    cursor.execute(f"SELECT direction FROM sessions WHERE trucks_id = {truck_id} ORDER BY date desc limit 1")
    result=cursor.fetchall()
    last_direction=result[0]["direction"] if result else '' # last direction
    
    cursor.execute(f'SELECT weight from containers WHERE id = "{containers}"')
    container_weight=cursor.fetchall()
    container_weight=container_weight[0]["weight"] if container_weight else '' # container weight
    truck_weight = cursor.execute(f'SELECT weight from trucks WHERE truckid = "{truck_id}"')
    truck_weight=cursor.fetchall()
    truck_weight=truck_weight[0]["weight"] if truck_weight else '' #truck weight
    
    #conditions
    if last_direction == direction and force == 'False': #force=False, directions are equal. no need to overwrite.
        return f"Error direction for truck {truck_id}"
    
    elif last_direction == direction and force == 'True' : #force=True, overwrite.
        cursor.execute(f'UPDATE sessions SET bruto={weight} WHERE trucks_id={truck_id} ORDER BY date desc limit 1')
        conn.commit()
    
    elif direction == 'none' and last_direction == 'in': #last direction is 'in' and current direction is 'none'
        return f"Error direction for truck {truck_id}"

    elif direction == 'in' or direction == 'none': #current direction is 'in'/'none'
        new_session(str(direction), bool(force), date, float(weight), int(truck_id), str(product))
    
    elif direction == 'out':
        if last_direction != 'in': #current direction is 'out'. option1: last direction is not 'in' -> error.
            return f"Error direction for truck {truck_id}"
        #option2: last direction is 'in'. 
        cursor.execute(f'SELECT bruto FROM sessions WHERE trucks_id={truck_id} AND direction="in" ORDER BY date desc limit 1')
        ans = cursor.fetchall()
        bruto = ans[0]["bruto"]# bruto from 'in' session  
        neto=float(bruto)-float(container_weight)-float(truck_weight) # neto
        cursor.execute(f'UPDATE sessions SET neto={neto} WHERE trucks_id={truck_id} AND direction="in" ORDER BY date desc limit 1 ')
        conn.commit()
        cursor.execute(f'SELECT id FROM sessions WHERE trucks_id={truck_id} AND direction="in" ORDER BY date desc limit 1')
        result=cursor.fetchall()
        session_id=result[0]['id']
    
    if direction == 'in' or direction == 'none':
            data = {
                "id": session_id,
                "truck": truck_id,
                "bruto": weight,
            }
            return json.dumps(data)
    elif direction == 'out':
            data = {
                "id": session_id,
                "truck": truck_id,
                "bruto": weight,
                "truckTara": truck_weight,
                "neto": neto
            }
            return json.dumps(data)
    
def new_session(direction, force, date, weight, truck_id, product):
    conn = init() #set connection
    cursor = conn.cursor(dictionary=True, buffered=True)
    cursor.execute(f'SELECT id FROM products WHERE product_name="{product}"')
    product_id=cursor.fetchall()
    product_id=int(product_id[0]['id']) if product_id else '' #get product id
    allData=(direction, force, date, weight, truck_id, product_id)
    query = (f'INSERT into sessions (direction, f, date, bruto, trucks_id, products_id) VALUES (%s, %s, %s, %s, %s, %s)')
    cursor.execute(query , allData)
    conn.commit()#update the changes from INSERT.

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

