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
def health():
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)