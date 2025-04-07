from fastapi import FastAPI
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from fastapi_cache import FastAPICache
from routes.apiroutes import apirouter
from fastapi_cache.backends.redis import RedisBackend
from sqlalchemy import create_engine
from models.user import UserBase

from redis import asyncio as aioredis
import uvicorn
import os

redis_connection_string = os.environ.get("REDIS_CONNECTION_STRING")
database_connection_string_sync = os.environ.get("DATABASE_CONNECTION_STRING_SYNC")


engine = create_engine(
    database_connection_string_sync, echo="debug")

#UserBase.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(redis_connection_string)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


application = FastAPI(lifespan=lifespan)

def get_application() -> FastAPI:
    application.include_router(apirouter)
    return application


app = get_application()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)