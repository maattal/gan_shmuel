import requests
import json

def test():

    finalResponse = "OK"

    host_url = "http://localhost:8081"

    if not requests.get(host_url).status_code == 200:
        finalResponse = "False"
        return finalResponse

    #POST/provider ##########
    PARAMS = {'name':'Lenovo'}
    if not requests.post(host_url+"/provider", params=PARAMS).status_code == 200:
        finalResponse = "False"
        return finalResponse
    PARAMS = {'name':'eclipse'}
    if not requests.post(host_url+"/provider", params=PARAMS).status_code == 200:
        finalResponse = "False"
        return finalResponse
    #########################

    #PUT/provider ###########
    if not requests.put(host_url+"/provider/1", params=PARAMS).status_code == 200:
        finalResponse = "False"
        return finalResponse
    PARAMS = {'name':'Asus'}     
    if not requests.put(host_url+"/provider/1", params=PARAMS).status_code == 200:
        finalResponse = "False"
        return finalResponse
    #########################

    #POST /truck ############
    PARAMS = {'truckid':'55555','providerid':'2'}
    if not requests.post(host_url+"/truck", params=PARAMS).status_code == 200:
        finalResponse = "False"
        return finalResponse
    PARAMS = {'truckid':'55555','providerid':'80'}
    if not requests.post(host_url+"/truck", params=PARAMS).status_code == 200:
        finalResponse = "False"
        return finalResponse
    #########################

    #PUT/truck ##############
    PARAMS = {'providerid':'4'}     
    if not requests.put(host_url+"/truck/77777", params=PARAMS).status_code == 200:
        finalResponse = "False"
        return finalResponse
    PARAMS = {'providerid':'4'}     
    if not requests.put(host_url+"/truck/79979", params=PARAMS).status_code == 200:
        finalResponse = "False"
        return finalResponse
    #########################

    #GET/truck ##############
    PARAMS = {'from':'201508011600000','to':'202108011600000'}
    if not requests.get(host_url+"/truck/1", params=PARAMS).status_code == 200:
        finalResponse = "False"
        return finalResponse
    #########################

    #POST/rates #############
    PARAMS = {'filename':'rates.xlsx'}
    if not requests.post(host_url+"/rates", params=PARAMS).status_code == 200:
        finalResponse = "False"
        return finalResponse
    #########################

    #GET/rates ##############
    if not requests.get(host_url+"/rates").status_code == 200:
        finalResponse = "False"
        return finalResponse
    #########################

    #GET/bill ###############
    if not requests.get(host_url+"/bill/3").status_code == 200:
        finalResponse = "False"
        return finalResponse
    #########################

    print (finalResponse)
    return finalResponse
test()