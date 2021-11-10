import os
import yagmail
import sys
import json

user=sys.argv[1]
billing_status=sys.argv[2]
weight_status=sys.argv[3]

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
    receiver = ['asaad.mosa@gmail.com','malki.attal@hotmail.fr','shaykllifalon@gmail.com']
    body = "hi, report from your CI server"
    filename = "report.html"

    yag = yagmail.SMTP("blueteamdevleap2021@gmail.com")
    yag.send(
        to=receiver,
        subject="CI test with html report",
        contents=body, 
        attachments=filename,
    )

build_data()
os.system("/home/%s/.local/bin/py.test --html=report.html -s" % user)
send_email()
