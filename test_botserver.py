import pytest
import requests
from requests.auth import HTTPBasicAuth
import base64
import json

endpoint = "http://127.0.0.1:8000/bot"
username = "admin"
password = "admin"
basic_auth = "Basic "+base64.b64encode(f"{username}:{password}".encode()).decode()
token = "sup3rs3cr3t"

class ConflictErr(Exception):
    pass

class WrongInput(Exception):
    pass

class InternalServerErr(Exception):
    pass

class AuthenticationErr(Exception):
    pass

class MethodNotAllowedErr(Exception):
    pass

class BotNotFoundErr(Exception):
    pass



@pytest.fixture(scope="module")
def added_bots():
    return []


@pytest.mark.usefixtures("added_bots")
class TestBotServer:
    response_schema = {"id":{"type":int},"name":{"type":str},"intents":{"type":list,"allowed":["play_sound","tell_joke","disconnect"]},"url":{"type":str}}


    def test_clear_bots(self):
        headers = {"Authorization":basic_auth}
        requests.delete(endpoint,headers=headers)
        

    @pytest.mark.parametrize("auth_type,secret,name,intents,url", [
                                                  pytest.param("basic_auth","WrongCredentials","skip_basic_auth", "","", marks=pytest.mark.xfail(raises=AuthenticationErr)),
                                                  pytest.param("token","WrongCredentials","skip_token","","", marks=pytest.mark.xfail(raises=AuthenticationErr)),
                                                  ("basic_auth",basic_auth,"bot_for_basic_auth_test",[],""),
                                                  ("token",token,"bot_for_token_test",[],""),
                                                  ("basic_auth",basic_auth,"bot1",["play_sound","tell_joke","disconnect"],"bot1.com"),
                                                  pytest.param("basic_auth",basic_auth,"bot1", [],"", marks=pytest.mark.xfail(raises=ConflictErr)),
                                                  pytest.param("basic_auth",basic_auth,"bot2", ["unkown_intent"],"bot3.com", marks=pytest.mark.xfail(raises=WrongInput)),
                                                            ])
    def test_post(self,added_bots,auth_type,secret,name,intents,url):
        body = {"intents":intents,"url":url}
        req_url = endpoint+"/"+name
        if auth_type == "basic_auth":
            headers = {"Authorization":secret}
            resp = requests.post(req_url,json=body,headers=headers)
        else:
            body.update(token=secret)
            resp = requests.post(req_url,json=body) 
        if not resp.ok:
            if resp.status_code == 401:
                raise AuthenticationErr(json.dumps(resp.json()))
            elif resp.status_code == 400:
                raise WrongInput(json.dumps(resp.json()))
            elif resp.status_code == 404:
                raise BotNotFoundErr(json.dumps(resp.json()))
            elif resp.status_code == 409:
                raise ConflictErr(json.dumps(resp.json()))
            elif resp.status_code == 405:
                raise MethodNotAllowedErr(json.dumps(resp.json()))
            else:
                raise InternalServerErr(resp.content.decode())
        
        added_bots.append(name)
    

    @pytest.mark.parametrize("auth_type,secret,name", [
                                                        pytest.param("basic_auth","WrongCredentials","skip_basic_auth", marks=pytest.mark.xfail(raises=AuthenticationErr)),
                                                        pytest.param("token","WrongCredentials","skip_token", marks=pytest.mark.xfail(raises=AuthenticationErr)),
                                                        ("basic_auth",basic_auth,"bot_for_basic_auth_test"),
                                                        ("basic_auth",basic_auth,"bot_for_token_test"),
                                                        pytest.param("basic_auth",basic_auth,"not_exists",marks=pytest.mark.xfail(raises=BotNotFoundErr))
                                                            ])
    def test_get(self,added_bots,auth_type,secret,name):
        body = {}
        req_url = endpoint+"/"+name
        if auth_type == "basic_auth":
            headers = {"Authorization":secret}
            resp = requests.get(req_url,json=body,headers=headers)
        else:
            body.update(token=secret)
            resp = requests.get(req_url,json=body) 

        if not resp.ok:
            if resp.status_code == 401:
                raise AuthenticationErr(json.dumps(resp.json()))
            elif resp.status_code == 400:
                raise WrongInput(json.dumps(resp.json()))
            elif resp.status_code == 404:
                raise BotNotFoundErr(json.dumps(resp.json()))
            elif resp.status_code == 409:
                raise ConflictErr(json.dumps(resp.json()))
            elif resp.status_code == 405:
                raise MethodNotAllowedErr(json.dumps(resp.json()))
            else:
                raise InternalServerErr(resp.content.decode())

    
            

