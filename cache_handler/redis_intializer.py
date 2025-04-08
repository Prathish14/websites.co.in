from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from redis import Redis
from fastapi import HTTPException
import os

redis_connection_string = os.environ.get("REDIS_CONNECTION_STRING")
redis = Redis.from_url(redis_connection_string)

class RedisManaged:

    @staticmethod
    def check_rate_limit_of_user(user_id: str, max_count=5, expire=60):
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
        if not value:
            return None
        return int(value.decode())

    @staticmethod
    def decrement_user_ai_credits(user_id: str, decrment_value: int):
        key = f"local:ai_credits_of_user:{user_id}"
        value = redis.get(name=key)
        new_incremented_value = int(value.decode()) - decrment_value
        redis.set(name=key, value=new_incremented_value)
        return new_incremented_value
    
    @staticmethod
    def check_ai_rate_limit():
        key1 = f"local:ai_rate_checker:Flash-Lite:RPM" #30		
        key2 = f"local:ai_rate_checker:Flash-Lite:TPM" #1000000
        key3 = f"local:ai_rate_checker:Flash-Lite:RPD" #1500

        value1 = redis.get(name=key1)
        value2 = redis.get(name=key2)
        value3 = redis.get(name=key3)

        if value1 and int(value1.decode()) > 30:
            message = f'rate limit reached, call after 1 min'
            raise HTTPException(
                status_code=429,
                detail=message,
            )
        
        if value2 and int(value2.decode()) > 1000000:
            message = f'rate limit reached, call after 1 min'
            raise HTTPException(
                status_code=429,
                detail=message,
            )

        if value3 and int(value3.decode()) > 1500:
            message = f'rate limit reached, call after a day'
            raise HTTPException(
                status_code=429,
                detail=message,
            )
    
    @staticmethod
    def set_ai_rate_limit(rpm: int = None, tpm: int = None, rpd: int = None):
        key1 = f"local:ai_rate_checker:Flash-Lite:RPM" #30		
        key2 = f"local:ai_rate_checker:Flash-Lite:TPM" #1000000
        key3 = f"local:ai_rate_checker:Flash-Lite:RPD" #1500

        if rpm:
            value1 = redis.get(name=key1)
            if value1 is None:
                value1 = int(redis.incr(key1, amount=rpm))
                redis.expire(key1, 60)

            else:
                if int(value1.decode())+rpm > 30:
                    message = f'rate limit reached, call after 1 min'
                    raise HTTPException(
                        status_code=429,
                        detail=message,
                    )
                redis.incr(key1, amount=rpm)
        
        if tpm:
            value2 = redis.get(name=key2)
            if value2 is None:
                value2 = int(redis.incr(key2, amount=tpm))
                redis.expire(key2, 60)
            else:
                if int(value2.decode())+tpm > 1000000:
                    message = f'rate limit reached, call after 1 min'
                    raise HTTPException(
                        status_code=429,
                        detail=message,
                    )
                redis.incr(key2, amount=tpm)


        if rpd:
            value3 = redis.get(name=key3)
            if value3 is None:
                value3 = int(redis.incr(key3, amount=rpd))
                redis.expire(key3, 86400)
            else:
                if int(value3.decode())+rpd > 1500:
                    message = f'rate limit reached, call after a day'
                    raise HTTPException(
                        status_code=429,
                        detail=message,
                    )
                redis.incr(key3, amount=rpd)