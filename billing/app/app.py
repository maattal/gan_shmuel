from flask import Flask,request
import os,sys,json
import mysql.connector

app = Flask(__name__)

#db contenction
def init_db():
    return mysql.connector.connect(
        host='db',
        database='billdb',
        user='host',
        password='pass'
    )

@app.route('/',methods = ['GET'])
def index():
    return 'ko'

@app.route('/health',methods = ['GET'])
def health():
 return 'ok'




if __name__ == '__main__':
    app.run(host="0.0.0.0",debug = False)





