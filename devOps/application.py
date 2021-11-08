from flask import Flask,request
from flask.wrappers import JSONMixin
# #https://github.com/maattal/gan_shmuel.git 
app =Flask(__name__) 

@app.route('/') 
def home():
    return ("hello webhook",200)

@app.route('/', methods=['POST']) 
def post_request(): 
    print(request.json) 
    dict_data=JSONMixin.loads(request.json)
    print(dict_data)
    return ("this is a request post from github webhook", 200, None)


if __name__== '__main__': 
    app.run(host="0.0.0.0",debug=True,port='8085') 
