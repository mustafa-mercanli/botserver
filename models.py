import redis
import json
r = redis.Redis()

class BotAlreadyExistErr(Exception):
    pass

class ValidationErr(Exception):
    pass


class Bot:
    VALIDATION_SCHEMA = {"intents":list,"url":str}

    def validate(params):
        for key in params:
            if key not in Bot.VALIDATION_SCHEMA.keys():
                raise ValidationErr("Unexpected param : %s" % key)
            
            expected_type = Bot.VALIDATION_SCHEMA[key]
            if not type(params[key]) == expected_type:
                raise ValidationErr("Expected type for param %s -> %s" % (key,expected_type))

        return True

    name = None
    intents = None
    url = None

    current_instance = None


    def set_id(self):
        import time
        self.id = int(time.time())

    def __init__(self,name :str,intents:list = [],url:str = ""):
        self.name = name
        self.intents = intents
        self.url = url
    
    
    def json(self):
        return {"id":self.id,"name":self.name,"intents":self.intents,"url":self.url}

    
    def __str__(self):
        return json.dumps(self.json())


    def get(name:str):
        found = r.get(name)
        if found:
            jsn = json.loads(found)
            instance = Bot(name=jsn["name"],intents=jsn["intents"],url=jsn["url"])
            instance.id = jsn["id"]
            instance.current_instance = Bot(name=jsn["name"],intents=jsn["intents"],url=jsn["url"])
            instance.current_instance.id = jsn["id"]
            return instance

    def save(self):
        if self.current_instance:
            new_instance = self.json()
            new_instance.update(id=self.current_instance.id)
            if self.current_instance.name == self.name:
                r.set(self.name,json.dumps(new_instance))
                print("Updated existing object with id",self.id)
                return
            else:
                found = Bot.get(name=self.name)
                if found:
                    raise BotAlreadyExistErr("Please change the bot name")
                r.delete(self.current_instance.name)
                r.set(self.name,json.dumps(new_instance))
                print("Updated existing object with id %s and new name %s" % (self.id,self.name))
                return

        self.set_id()
        found = Bot.get(name=self.name)
        if found:
            raise BotAlreadyExistErr("Please change the bot name")
        
        r.set(self.name,json.dumps(self.json()))
        print("Saved new object with id",self.id)

    def delete(self):
        r.delete(self.name)
        print("Deleted object with id",self.id)
        self.id = None
        self.name = None
        self.intents = None
        self.url = None
   

        
         
