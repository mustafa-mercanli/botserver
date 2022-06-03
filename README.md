# Botserver Web Service
## Dependencies
* **Redis-server**: Bot instances are stored in Redis Database. 
For windows you can download and install redis-server from the link https://github.com/microsoftarchive/redis/releases/download/win-3.0.504/Redis-x64-3.0.504.msi 
* **Python 3.x**
## Installation
```
pip install fastapi
pip install uvicorn
pip install redis
pip install requests
pip install pytest
```
or
```
pip install -r required_modules.txt
```
## Usage
In project directory, just run like that
```
uvicorn server:app --port=8000
```

## Testcases
You can test the endpoint methods with pytest
```
pytest test_botserver.py
```

Every methods that endpoint supports(GET,POST,PUT,PATCH,DELETE) will be tested after running pytest. Test functions below:
* test_post(): Test adding new bot
* test_get(): Get a bot instance
* test_intent(): Test running bot intent
* test_put(): Test updating a bot instance
* test_patch(): Test partially updating a bot instance
* test_delete(): Test deleting bot instance

## Additional
Look for the inline comments to get additional informations. You can find the authentication credentials in **config.py**.

**Note**: You can easily import the **bostserver.postman_collection2.json** file as a **Postman** collection so that call the API methods

