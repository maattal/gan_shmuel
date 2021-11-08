from flask import Flask
from flask_restful import Api, Resource
import mysql.connector
from flask import request,Response

app = Flask(__name__)
api = Api(app)  

def init():
    return mysql.connector.connect(
        host='db',
        database='weight',
        user='root',
        password='root'
    )

class Health(Resource):
    def get(self):
        try:
            init()
            return "ok",200
        except:
            return "internal server error",500
api.add_resource(Health,"/health")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

# @app.route("/health", methods=["GET"])
# def func1():
#     return "ok"
