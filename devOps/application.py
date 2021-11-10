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
def down_up(branch):
        os.system("git fetch")
        os.system(f"git checkout {branch}")
        os.system("git pull")
        os.chdir("/app")
        os.system("docker-compose -f billing/docker-compose.yml down")
        os.system("docker-compose -f weight/docker-compose.yml down")

        os.system("docker-compose -f billing/docker-compose.yml up -d --build")
        os.system("docker-compose -f weight/docker-compose.yml up -d --build")

def build_fun(branch):
    if branch == 'staging':
        down_up(branch)
        return (f"working on {branch}aging auto diployment")
    elif branch == 'main':
        down_up(branch)
        return (f"working on {branch} auto diployment")
    else:
        return (f"on this {branch} no action!!")



if __name__== '__main__': 
    app.run(host="0.0.0.0",debug=True,port='8085') 


    
