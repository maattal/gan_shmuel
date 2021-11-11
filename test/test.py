import os
import yagmail
import sys
import json

user=sys.argv[1]
billing_status=sys.argv[2]
weight_status=sys.argv[3]
branch=sys.argv[4]

def build_data():
    data={}
    data['tests']=[]
    data["tests"].append({
        'id' : 1,
        'name' : 'billing',
        'result' : billing_status
    })
    data["tests"].append({
        'id' : 2,
        'name' : 'weight',
        'result' : weight_status
    })

    with open('data.json','w+') as outfile:
        json.dump(data,outfile)



def send_email():
    if billing_status == "Ok" and weight_status == "Ok":
	    build_pass="test successfull , push successfull"
    else :
  	    build_pass=f"test failed, billing status: {billing_status} , weight status: {weight_status}, push failed"
    receiver = ['asaad.mosa@gmail.com','malki.attal@hotmail.fr','shaykllifalon@gmail.com']
    body = f"{build_pass}"
    filename = "report.html"

    yag = yagmail.SMTP("blueteamdevleap2021@gmail.com","Asaad2021!")
    yag.send(
        to=receiver,
        subject=f"CI test with html report from {user} for branch : {branch}",
        contents=body, 
        attachments=filename,
    )

build_data()
os.system("/usr/local/bin/py.test --html=report.html -s")
send_email()
