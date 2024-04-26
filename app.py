from flask import Flask, request
import json
import hashlib
# from time import time
from datetime import datetime

app = Flask(__name__)

password = "1ea36d6cf235d71982e8a63706bce9f446eccc4027821321be869cb9c79d0cacb8f3f6cf65a4434f25d755bae2e8465d"

# function to add to JSON
def write_json(key, value, filename='database.json'):
    with open(filename,'r+') as file:
        file_data = json.load(file)
        file_data[key]=value
        file.seek(0)
        json.dump(file_data, file, indent = 4)

def log(text):
    with open("log.txt","a") as f:
        f.write(f"\n{datetime.now()} {text}")

def check_password(text):
    return encrypt(text) == password

@app.route('/')
def home():
    with open("database.json","r") as f: data=f.read()
    return data

@app.route("/set",methods=["POST","GET"])
def set():
    if request.method == "POST":
        if check_password(request.form['password']):
            write_json(request.form['key'],request.form['value'])
            log(f"Data addition: ({request.form['key']}:{request.form['value']})")
            return {"status":200,"data_recieved":(request.form['key'],request.form['value'])}
        else:
            return {"status":401,"data_recieved":(request.form['key'],request.form['value'])}
    else:
        return {"status":400,"data_recieved":()}

@app.route("/get",methods=["GET"])
def get():
    # if check_password(request.form['password']):
    key=request.form['key']
    with open("database.json","r") as f:
        data=json.load(f)
    if key not in data:
        return {"status":400,"key":key,"value":""}
    # log(f"Data got:")
    return {"status":200,"key":key,"value":data[request.form['key']]}

@app.route("/del",methods=["DELETE","GET"])
def delete():
    if check_password(request.form['password']):
        status=200
        with open("database.json",'r') as file:
            key =request.form['key']
            file_data = json.load(file)
            if key not in file_data: 
                status=400
            else: 
                log(f"Data deleted: ({key}:{file_data[key]})")
                file_data.pop(key)
        with open("database.json","w") as file:
            file.seek(0)
            json.dump(file_data, file, indent = 4)
        return {"status":status}
    else:
        return {"status":401}

@app.route("/encrypt/<data>")
def encrypt(data: str):
    hash_object = hashlib.sha384()
    hash_object.update(data.encode())
    return hash_object.hexdigest()

if __name__ == "__main__":
    app.run(debug=True)