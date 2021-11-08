from flask import Flask,request
# #https://github.com/maattal/gan_shmuel.git 
app =Flask(__name__) 

@app.route('/') 
def home():
    return "hi",200

@app.route('/', methods=['POST']) 
def hello_world(): 
    print("ive got something")
    print(request.json) 
    return ("this is webhook", 200, None)


if __name__== '__main__': 
    app.run(host="0.0.0.0",debug=True,port='8085') 
