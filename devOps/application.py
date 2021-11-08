from flask import Flask,request
from flask.wrappers import JSONMixin
import os
# #https://github.com/maattal/gan_shmuel.git 
app =Flask(__name__) 
#--------------------WEBHOOK-----------------------
@app.route('/') 
def home():
    return ("hello webhook",200)

@app.route('/', methods=['POST']) 
def post_request(): 
    json_str=request.json
    branch=list(json_str['ref'].split("/"))[2]
    commiter=json_str['pusher']['name']
    # return_string=f"this is a request from {commiter}, from the branch {branch}"
    return_string=build_fun(branch)
    return (return_string, 200, None)

#--------------------BUILD OF THE CONTAINERS------------
def build_fun(branch):
    os.system("docker-compose down")
    if branch == 'staging':
        os.system("git fetch")
        os.system("git checkout staging")
        os.system("git pull")
        os.system("docker-compose -f billing/docker-compose.yml up")
        os.system("docker-compose -f weight/docker-compose.yml up")
#      os.system(f"docker-compose -f docker-composeStaging.yml --build")
        return ("working on staging auto diployment")
    elif branch == 'main':
        os.system("git fetch")
        os.system("git checkout main")
        os.system("git pull")
        os.system("docker-compose -f billing/docker-compose.yml up")
        os.system("docker-compose -f weight/docker-compose.yml up")
        #os.system(f"docker-compose -f docker-composeMain.yml --build")
        return ("working on master auto diployment")
    else:
        return (f"on this {branch} no action!!")


if __name__== '__main__': 
    app.run(host="0.0.0.0",debug=True,port='8085') 
