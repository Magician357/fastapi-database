# from flask import Flask, request
from fastapi import FastAPI, Response, status
import json
import hashlib
# from time import time
from datetime import datetime

app = FastAPI()

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

@app.get('/')
def home():
    with open("database.json","r") as f: data=f.read()
    return f"this is a database. to add data, send a post request to the /set page with the key, value, and password in the query. to get data, send a get request to the /get page with the key in the query. to delete data, send a delete request to /del with the key and password in the query. eg getting a key would be sending a get request to http://127.0.0.1:8000/get?key=hello   {data}"

@app.post("/set", status_code=200)
def set(key: str, value:str, password: str, response: Response):
    if check_password(password):
        write_json(key,value)
        log(f"Data addition: ({key}:{value})")
        return {"status":200,"data_recieved":(key,value)}
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"status":401,"data_recieved":(key,value)}

@app.get("/get", status_code=200)
def get(key:str,response: Response):
    # if check_password(request.form['password']):
    with open("database.json","r") as f:
        data=json.load(f)
    if key not in data:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status":400,"key":key,"value":""}
    # log(f"Data got:")
    return {"status":200,"key":key,"value":data[key]}

@app.delete("/del", status_code=200)
def delete(key:str,password:str,response: Response):
    if check_password(password):
        # status=200
        response.status_code = status.HTTP_200_OK
        with open("database.json",'r') as file:
            file_data = json.load(file)
            if key not in file_data: 
                response.status_code = status.HTTP_400_BAD_REQUEST
                # status=400
            else: 
                log(f"Data deleted: ({key}:{file_data[key]})")
                file_data.pop(key)
        with open("database.json","w") as file:
            file.seek(0)
            json.dump(file_data, file, indent = 4)
        return {"status":response.status_code}
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"status":401}

@app.route("/encrypt/<data>")
def encrypt(data: str):
    hash_object = hashlib.sha384()
    hash_object.update(data.encode())
    return hash_object.hexdigest()

# if __name__ == "__main__":
    # app.run(debug=True)