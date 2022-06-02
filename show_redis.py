import redis

r = redis.Redis()

for key in r.keys():
    print(r[key])