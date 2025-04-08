from fastapi_cache.decorator import cache
from cache_handler.key_builder import key_builder
from sqlalchemy import select
from models.user import User

class AdminHandler:
    @staticmethod
    @cache(expire=600, key_builder=key_builder)
    async def get_user_from_id(session, user_id: str):
        query = select(User).\
        filter(User.id == user_id).limit(1)
        result = await session.execute(query)
        user_obj = result.first()
        return user_obj

class AdminHandlerSync:
    @staticmethod
    def get_user_from_id(session, user_id: str):
        query = select(User.id, User.email, User.mobile_number, User.name, User.plan, User.period, User.plan_end_date, User.plan_start_date, User.ai_credits).\
        filter(User.id == user_id).limit(1)
        result = session.execute(query)
        user_obj = result.first()
        return user_obj