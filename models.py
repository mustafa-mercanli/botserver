import redis
import json
r = redis.Redis()

class BotAlreadyExistErr(Exception):
    pass

class ValidationErr(Exception):
    pass

class NotCapableErr(Exception):
    pass


#This decorator function checks the bot has the intent. 
#If not doesnt allow to run this function
def check_capability(func):
    def wrapper(bot_instance):
        if func.__name__ in bot_instance.intents:
            return func(bot_instance)
        else:
            print("The bot is not capable of doing it")
            raise NotCapableErr("The bot is not capable of doing it")
    return wrapper


class Bot:
    VALIDATION_SCHEMA = {"intents":{"type":list,"allowed":["play_sound","tell_joke","disconnect"]},"url":{"type":str}}

    #This function makes validation of dict object to create proper bot instance
    def validate(params):
        for key in params:
            input = params[key]
            if key not in Bot.VALIDATION_SCHEMA.keys():
                raise ValidationErr("Unexpected param : %s" % key)
            
            expected_type = Bot.VALIDATION_SCHEMA[key]["type"]
            if not type(input) == expected_type:
                raise ValidationErr("Expected type for param %s -> %s" % (key,expected_type))
            
            alloweds = Bot.VALIDATION_SCHEMA[key].get("allowed")
            if alloweds:
                if set(input) - set(alloweds):
                    raise ValidationErr("Allowed items for param %s -> %s" % (key,",".join(alloweds)))

        return params

    name = None
    intents = None
    url = None

    current_instance = None


    #Id generation not allowed to client
    def set_id(self):
        import time
        self.id = int(time.time())

    def __init__(self,name :str,intents:list = [],url:str = ""):
        self.name = name
        self.intents = intents
        self.url = url
    
    
    #Simply convert bot object into json data
    def json(self):
        return {"id":self.id,"name":self.name,"intents":self.intents,"url":self.url}

    
    #when printing the bot object, write it as json
    def __str__(self):
        return json.dumps(self.json())


    #If you want to obtain an existing bot instance in redis, you can call this static method
    #It returns a bot instance
    def get(name:str):
        found = r.get(name)
        if found:
            jsn = json.loads(found)
            instance = Bot(name=jsn["name"],intents=jsn["intents"],url=jsn["url"])
            instance.id = jsn["id"]
            instance.current_instance = Bot(name=jsn["name"],intents=jsn["intents"],url=jsn["url"])
            instance.current_instance.id = jsn["id"]
            return instance


    #You can save a bot intsance using its save function.
    #Json data stored in redis database
    def save(self):
        if self.current_instance:#This is for an update operation
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


    #Delete bot instance in redis
    def delete(self):
        r.delete(self.name)
        print("Deleted object with id",self.id)
        self.id = None
        self.name = None
        self.intents = None
        self.url = None

    @check_capability
    def play_sound(self):
        print("Im playing a sound")
        return "Im playing a sound"

    @check_capability
    def tell_joke(self):
        print("Im telling a joke")
        return "Im telling a joke"
    
    @check_capability
    def disconnect(self):
        print("Disconnected")
        return "Disconnected"

    @check_capability
    def unexpected(self):
        pass
    
    #Flush the redis database
    def clear_bots():
        for key in r.keys():
            r.delete(key)

   

        
         
