import json
from .. import redis_client

class CacheService:

    @staticmethod
    def set_json(key, value, ttl=300):
        redis_client.set(key, json.dumps(value), ex=ttl)

    @staticmethod
    def get_json(key):
        data = redis_client.get(key)
        return json.loads(data) if data else None

    @staticmethod
    def delete(key):
        redis_client.delete(key)
