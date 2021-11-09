from flask import Flask
from flask_restful import Api, Resource
import mysql.connector 
from flask import request,Response
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)