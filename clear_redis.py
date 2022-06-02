import redis
r = redis.Redis()

for key in r.keys():
    r.delete(key)