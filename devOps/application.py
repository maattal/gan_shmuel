from flask import Flask,request
# #https://github.com/maattal/gan_shmuel.git 
app =Flask(__name__) 

print("blablabla")

@app.route('/', methods=['POST']) 
def hello_world(): 
    print("iv got a request") 
    return 200

if __name__== '__main__': app.run(host="0.0.0.0",debug=True) 
