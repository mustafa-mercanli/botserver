from models import Bot,BotAlreadyExistErr,ValidationErr,NotCapableErr
from fastapi import FastAPI, Header,status,HTTPException,Request
from typing import Optional

from json.decoder import JSONDecodeError
import base64
import config

app = FastAPI()

basic_auth = "Basic "+base64.b64encode(f"{config.username}:{config.password}".encode()).decode()
token = config.token


#If neighter client sends basic authentication nor token authentication, raise authenticaion error
def authenticator(json_body,basic_auth_str):
    if not json_body.pop("token",None) == token and not basic_auth == basic_auth_str:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Wrong credentials")


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

    authenticator(body,authorization)

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


    authenticator(body,authorization)
        

    try:
        Bot.validate(body)
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

    authenticator(body,authorization)


    try:
        Bot.validate(body)
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

    authenticator(body,authorization)

    try:
        Bot.validate(body)
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

    authenticator(body,authorization)

    bot = Bot.get(name=bot_name)
    if not bot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Bot name not found")

    bot.delete()

    return {"result":"ok"}


@app.get("/bot/{bot_name}/{intent}")
async def intent_bot(bot_name,intent,request: Request,authorization: Optional[str] = Header(None)):
    try:
        body = await request.json()
    except:
        body = {}

    authenticator(body,authorization)

    bot = Bot.get(name=bot_name)
    if not bot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Bot name not found")

    try:
        result = getattr(bot,intent,bot.unexpected)()
    except NotCapableErr as e:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="Bot is not capable for doing that")

    return {"result":result}


@app.delete("/bot")
async def clear_bots(request: Request,authorization: Optional[str] = Header(None)):
    try:
        body = await request.json()
    except:
        body = {}

    authenticator(body,authorization)

    Bot.clear_bots()

    return {"result":"ok"}
