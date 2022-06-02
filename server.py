from sqlite3 import paramstyle
from models import Bot,BotAlreadyExistErr,ValidationErr
from fastapi import FastAPI, Header,status,HTTPException,Request,Depends
from typing import Optional

from json.decoder import JSONDecodeError
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import base64

app = FastAPI()

basic_auth = "Basic "+base64.b64encode(b"admin:admin").decode()
token = "sup3rs3cr3t"

security = HTTPBasic()

@app.get("/")
async def root():
    return {"message":"welcome"}

@app.get("/bot/")
async def bot():
    return {"usage": "/bot/<sample-bot-name>","allowed_methods":["GET","POST","PUT","PATCH","DELETE"]}


@app.get("/bot/{bot_name}")
async def get_bot(bot_name,request: Request,authorization: Optional[str] = Header(None)):
    try:
        body = await request.json()
    except:
        body = {}

    if not basic_auth == authorization and not body.get("token") == token :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Wrong credentials")

    bot = Bot.get(name=bot_name)
    if not bot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Bot name not found")

    return bot.json()
    

@app.post("/bot/{bot_name}")
async def post_bot(bot_name,request: Request,authorization: Optional[str] = Header(None)):
    try:
        body = await request.json()
    except JSONDecodeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Bad json body")
    
    print(body)


    if not basic_auth == authorization and not body.get("token") == token :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Wrong credentials")
        

    try:
        body = Bot.validate(body)
    except ValidationErr as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))


    new_bot = Bot(name=bot_name,**body)
    try:
        new_bot.save()  
        return new_bot.json()
    except BotAlreadyExistErr as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=str(e))

    return new_bot.json()

@app.put("/bot/{bot_name}")
async def put_bot(bot_name,request: Request,authorization: Optional[str] = Header(None)):
    try:
        body = await request.json()
    except JSONDecodeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Bad json body")
    print(body)

    if not basic_auth == authorization and not body.get("token") == token :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Wrong credentials")


    try:
        body = Bot.validate(body)
    except ValidationErr as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

    current_bot = Bot.get(name=bot_name)
    if not current_bot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Bot name not found")
    
    current_bot.intents = []
    current_bot.url = ""
    for key in body:
        setattr(current_bot,key,body[key])
    
    current_bot.save()

    return current_bot.json()

@app.patch("/bot/{bot_name}")
async def patch_bot(bot_name,request: Request,authorization: Optional[str] = Header(None)):
    try:
        body = await request.json()
    except JSONDecodeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Bad json body")
    print(body)

    if not basic_auth == authorization and not body.get("token") == token :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Wrong credentials")

    try:
        body = Bot.validate(body)
    except ValidationErr as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

    current_bot = Bot.get(name=bot_name)
    if not current_bot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Bot name not found")

    for key in body:
        setattr(current_bot,key,body[key])
    
    current_bot.save()

    return current_bot.json()

@app.delete("/bot/{bot_name}")
async def delete_bot(bot_name,request: Request,authorization: Optional[str] = Header(None)):
    try:
        body = await request.json()
    except JSONDecodeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Bad json body")
    print(body)

    if not basic_auth == authorization and not body.get("token") == token :
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Wrong credentials")

    bot = Bot.get(name=bot_name)
    if not bot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Bot name not found")

    bot.delete()

    return {"result":"ok"}




