from fastapi import FastAPI
from fastapi.responses import FileResponse
import json
import vs

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
    
@app.get("/signup")
async def root(email: str, name: str,password : str):
    data = {
        "email": email,
        "name": name,
        "password": password
    }
    with open('users.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)
    vs.register()
    return FileResponse("base.png")

@app.get("/image")
async def root():
    return FileResponse("base.png")


@app.get("/login")
async def root(email: str,password : str):
   with open('users.json', 'r') as infile:
    data = json.load(infile)
    if (email == data['email'] and password == data['password']):
       return {"message": data['name']}
    else :
       return {"message": "Failed"}
    

@app.get("/pay")
async def root():
    filepath = vs.getImage()
    return FileResponse(filepath, filename=filepath[7:12])

