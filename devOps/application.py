from flask import Flask,request
from flask.wrappers import JSONMixin
import os,subprocess
# #https://github.com/maattal/gan_shmuel.git 


NETWORK_NAME="blue_net"

#port assiments:

PORTS = {
    'PORT_CI':'8085',
    'WEIGHT_PORT_STAGING':'8082',
    'WEIGHT_PORT_MAIN':'8080',
    'BILLING_PORT_STAGING':'8081',
    'BILLING_PORT_MAIN':'8086',
    }


for port in PORTS:
    os.environ[port] = PORTS[port]

#create a network for DNS conection for api inside ci applications:

os.system(f"docker network create {NETWORK_NAME}")


# our git rep -> https://github.com/maattal/gan_shmuel.git 
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
        os.chdir("/app/gan_shmuel/billing")
        os.system("chmod +x test.py")
        billingResult=subprocess.check_output(['python3', './test.py'])
        os.chdir("/app")
        os.system("docker-compose -f weight/docker-compose.yml up -d --build")
        os.chdir("/app/gan_shmuel/weight")
        os.system("chmod +x test.py")
        weightResult=subprocess.check_output(['python3', './test.py'])
        os.chdir("/app")
        os.system("python3 gan_shmuel/test/test.py $USER $billingResult $weightResult")

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
    app.run(host="0.0.0.0",debug=True,port='8085',use_reloader=False)
