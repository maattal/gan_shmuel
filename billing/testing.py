import requests
import json

def test():

    finalResponse = "OK"

    host_url = "http://localhost:5000"

    if not requests.get(host_url).status_code == 200:
        finalResponse = "False"
        return finalResponse

    #POST/provider##########
    PARAMS = {'name':'Lenovo'}
    if not requests.post(host_url+"/provider", params=PARAMS).status_code in (200,500):
        finalResponse = "False"
        return finalResponse
    PARAMS = {'name':'eclipse'}
    if not requests.post(host_url+"/provider", params=PARAMS).status_code in (200,500):
        finalResponse = "False"
        return finalResponse
    #########################

    #PUT/provider############
    if not requests.put(host_url+"/provider/1", params=PARAMS).status_code in (200,500):
        print(finalResponse)
    PARAMS = {'name':'Asus'}     
    if not requests.put(host_url+"/provider/1", params=PARAMS).status_code in (200,500):
        print(finalResponse)
    #########################

    #POST /truck#############
    PARAMS = {'truckid':'55555','providerid':'2'}
    if not requests.post(host_url+"/truck", params=PARAMS).status_code in (200,500):
            finalResponse = "False"
            return finalResponse
    PARAMS = {'truckid':'55555','providerid':'80'}
    if not requests.post(host_url+"/truck", params=PARAMS).status_code in (200,500):
            finalResponse = "False"
            return finalResponse
    #########################

    
    print (finalResponse)
    return finalResponse
test()