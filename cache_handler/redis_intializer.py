from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import Redis
from fastapi import HTTPException

redis = Redis.from_url("redis://localhost:6379/0")

class RedisManaged:

    @staticmethod
    def check_rate_limit_of_user(user_id: str, max_count=5, expire=180):
        key = f"local:rate_limit_of_user:{user_id}"
        value = int(redis.incr(key, amount=1))

        if value == 1:
            redis.expire(key, expire)

        if value>max_count:
            message = f'rate limit reached user_id: {user_id},key: {key}, count: {value}'
            raise HTTPException(
                status_code=429,
                detail=message,
            )
        
        if not value:
            return 0
        
        return value
    
    @staticmethod
    def set_user_ai_credits(user_id: str, ai_credits: int):
        key = f"local:ai_credits_of_user:{user_id}"
        redis.set(name=key, value=ai_credits)
        return ai_credits
    
    @staticmethod
    def get_user_ai_credits(user_id: str):
        key = f"local:ai_credits_of_user:{user_id}"
        value = redis.get(name=key)
        return value

    @staticmethod
    def increment_user_ai_credits(user_id: str, incrment_value: int):
        key = f"local:ai_credits_of_user:{user_id}"
        value = redis.get(name=key)
        new_incremented_value = value + incrment_value
        redis.set(name=key, value=new_incremented_value)
        return new_incremented_value
    
    """@staticmethod
    def check_user_has_suffiecient_ai_credits(user_id: str):
        user_ai_credits = RedisManaged.get_user_ai_credits(user_id=user_id)

        if user_ai_credits <= 10:
            message = f'User dont have suffeicient credits'
            raise HTTPException(
                status_code=200,
                detail=message,
            )

"""
    
