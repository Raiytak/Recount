import redis

conn = redis.Redis()

conn.set('hello', 'world')

resp = conn.get("hello")
print(resp)