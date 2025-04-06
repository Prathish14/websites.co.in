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


engine = create_engine(
    f'postgresql://postgres.qfeyjfwcxufgbmltgfkn:McFykkr?Ex~tRn8@aws-0-ap-south-1.pooler.supabase.com:5432/postgres', echo="debug")

UserBase.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://localhost:6379/0")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


application = FastAPI(lifespan=lifespan)

def get_application() -> FastAPI:
    application.include_router(apirouter)
    return application


app = get_application()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)