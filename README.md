# Botserver Web Service
## Dependencies
* **Redis-server**: Bot instances are stored in Redis Database. 
For windows you can download and redis-server from the link https://github.com/microsoftarchive/redis/releases/download/win-3.0.504/Redis-x64-3.0.504.msi 
* **Python 3.x**
## Installation
```
pip install fastapi
pip install uvicorn
pip install redis
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
## Additional
You can find the authentication credentials in **config.py**

**Note**: You can easily import the **bostserver.postman_collection2.json** file as a **Postman** collection so that call the API methods



