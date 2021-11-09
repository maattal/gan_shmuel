from flask import Flask,request, jsonify , send_from_directory ,send_file
import os,sys,json
import mysql.connector
from datetime import datetime
from openpyxl import  load_workbook
import openpyxl as xl



app = Flask(__name__)
upload_folder = 'in/'
xlfile='rates.xlsx'


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
 return 'ok' ,200


@app.route("/rates", methods=['POST'])
def upload_xl_data():
    filename=upload_folder+request.args.get('filename')
    global xlfile
    xlfile = request.args.get('filename')
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


@app.route("/rates",methods=['GET'])
def download_file():
   return send_from_directory(upload_folder, xlfile,as_attachment=True)



@app.route('/truck/<id>',methods = ['PUT'])
def update_truckprovider(id):
    try:
        new_id = request.args.get('providerid')
        conn = init_db()
        mycursor = conn.cursor()
        query = (f"UPDATE trucks SET providerid = '{new_id}' WHERE id = '{id}'")
        mycursor.execute(query)
        conn.commit()
        return "OK"
    except:
        return "Invalid input"
 
@app.route('/bill/<id>',methods = ['GET'])
def show_bill():
    
    return


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug = False)
