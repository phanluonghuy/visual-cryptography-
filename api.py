from fastapi import FastAPI
from fastapi.responses import FileResponse
import json
import vs
import os

def lock_user():
    with open('users.json', 'r') as infile:
        data = json.load(infile)
        data['lock'] = True
    with open('users.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)


app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
    
@app.get("/signup")
async def root(email: str, name: str,hint: str, password : str):
    data = {
        "email": email,
        "name": name,
        "password": password,
        "lock": False
    }
    with open('users.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)
    # print(hint)
    vs.register(hint)
 
    return FileResponse("base.png")

@app.get("/image")
async def root():
    return FileResponse("base.png")


@app.get("/login")
async def root(email: str,password : str):
   with open('users.json', 'r') as infile:
    data = json.load(infile)
    if (email == data['email'] and password == data['password']):
       if data['lock'] == True:
           return {"message": "Account is lock"}
       return {"message": data['name']}
    else :
       return {"message": "Failed"}
    

@app.get("/pay")
async def root():
    filepath = vs.getImage()
    return FileResponse(filepath, filename=filepath[7:12])

@app.get("/payPishing")
async def root():
        # Phần chính
    image_folder = "pishing"
    # shutil.rmtree(image_folder)
    # shutil.rmtree("/"+image_folder)
    for filename in os.listdir(image_folder):
        filepath = os.path.join(image_folder, filename)
    return FileResponse(filepath, filename=filepath[7:12])


@app.get("/lock")
async def root():
    lock_user()
    return {"message": "Account is lock"}
