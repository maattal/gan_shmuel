from flask import Flask,request
from flask.wrappers import JSONMixin
import os,subprocess

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
    return_string=build_fun(branch,commiter)
    return (return_string, 200, None)

#--------------------BUILD OF THE CONTAINERS------------

def down_up(branch,commiter):
        os.system("git fetch")
        os.system(f"git checkout {branch}")
        os.system("git pull")
        os.chdir("/app")
        os.system("docker-compose -f billing/docker-compose.yml --project-name \"stable_Billing\" down") 
        os.system("docker-compose -f weight/docker-compose.yml --project-name \"stable_Weight\" down")
        os.system("docker-compose -f billing/docker-compose.yml up -d --build")
        os.system("docker-compose -f weight/docker-compose.yml up -d --build")
        test_result= testing_sendMailReport(branch,commiter)
        os.system("docker-compose -f billing/docker-compose.yml down") 
        os.system("docker-compose -f weight/docker-compose.yml  down")
        if False:
            os.system("docker-compose -f billing/docker-compose.yml --project-name \"stable_Billing\" up -d --build")
            os.system("docker-compose -f weight/docker-compose.yml --project-name \"stable_Weight\" up -d --build")
            print("success test, push and report :)")
        else:
            os.system("docker-compose -f billing/docker-compose.yml --project-name \"stable_Billing\" up -d ")
            os.system("docker-compose -f weight/docker-compose.yml --project-name \"stable_Weight\" up -d ")
            #cancel the push theorithical 
            print("failure to test,don't push and report :(")


def testing_sendMailReport(branch,commiter):
    os.system("chmod +x billing/test.py")
    billingResult=subprocess.check_output(['python3', './billing/test.py']).decode("utf-8").strip()
    os.system("chmod +x weight/test.py")
    weightResult=subprocess.check_output(['python3', './weight/test.py']).decode("utf-8").strip() 
    os.chdir("/app")
    try:
        os.system(f"python3 /app/test/test.py {commiter} {billingResult} {weightResult}")
    except:
        print("failure to send mail")  

    if billingResult=="Ok" and weightResult=="Ok":
        return True
    return False

def build_fun(branch,commiter):
    if branch == 'staging':
        down_up(branch,commiter)
        return (f"working on {branch}aging auto diployment")
    elif branch == 'main':
        down_up(branch,commiter)
        return (f"working on {branch} auto diployment")
    else:
        return (f"on this {branch} no action!!")



if __name__== '__main__': 
    app.run(host="0.0.0.0",debug=True,port='8085',use_reloader=False) 


  
