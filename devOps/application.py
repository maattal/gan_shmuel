from flask import Flask,request
from flask.wrappers import JSONMixin
# #https://github.com/maattal/gan_shmuel.git 
app =Flask(__name__) 

@app.route('/') 
def home():
    return ("hello webhook",200)

@app.route('/', methods=['POST']) 
def post_request(): 
    json_str=request.json
    branch=list(json_str['ref'].split("/"))
    commiter=json_str['pusher']['name']
    print(branch[2])
    print(commiter)
    return ("this is a request from {commiter}, from the branch {branch}", 200, None)


if __name__== '__main__': 
    app.run(host="0.0.0.0",debug=True,port='8085') 
