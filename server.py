from models import Bot,BotAlreadyExistErr,ValidationErr
from fastapi import FastAPI,status,HTTPException,Request
from json.decoder import JSONDecodeError

app = FastAPI()

@app.get("/")
async def root():
    return {"message":"welcome"}

@app.get("/bot/")
async def bot():
    return {"usage": "/bot/<sample-bot-name>","allowed_methods":["GET","POST","PUT","PATCH","DELETE"]}


@app.get("/bot/{bot_name}")
async def get_bot(bot_name):
    bot = Bot.get(name=bot_name)
    if not bot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Bot name not found")

    return bot.json()
    

@app.post("/bot/{bot_name}")
async def post_bot(request: Request,bot_name):
    try:
        body = await request.json()
    except JSONDecodeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Bad json body")
        
        
    print(body)

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
async def put_bot(request: Request,bot_name):
    try:
        body = await request.json()
    except JSONDecodeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Bad json body")
    print(body)

    try:
        Bot.validate(body)
    except ValidationErr as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

    current_bot = Bot.get(name=bot_name)
    if not current_bot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    current_bot.intents = []
    current_bot.url = ""
    for key in body:
        setattr(current_bot,key,body[key])
    
    current_bot.save()

    return current_bot.json()

@app.patch("/bot/{bot_name}")
async def patch_bot(request: Request,bot_name):
    try:
        body = await request.json()
    except JSONDecodeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Bad json body")
    print(body)

    try:
        Bot.validate(body)
    except ValidationErr as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))

    current_bot = Bot.get(name=bot_name)
    if not current_bot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    for key in body:
        setattr(current_bot,key,body[key])
    
    current_bot.save()

    return current_bot.json()

@app.delete("/bot/{bot_name}")
async def put_bot(bot_name):
    bot = Bot.get(name=bot_name)
    if not bot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    bot.delete()

    return {"result":"ok"}




