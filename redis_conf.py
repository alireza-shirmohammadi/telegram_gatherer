import redis

r = redis.StrictRedis(host='localhost', port=6379, db=0)

def redis_cli(key,value):
    r.set(key, value)

def redis_get(key):
    return r.get(key)