from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import NullPool

database_connection_string_sync = os.environ.get("DATABASE_CONNECTION_STRING_SYNC")
database_connection_string_async = os.environ.get("DATABASE_CONNECTION_STRING_ASYNC")


class SQLSession:
    _session_maker = None
    _engine = None
    
    @staticmethod
    def _get_session_maker():
        if not SQLSession._session_maker:
            SQLSession._engine = create_engine(
                database_connection_string_sync,
                poolclass=NullPool)
            SQLSession._session_maker = sessionmaker(SQLSession._engine)
        return SQLSession._session_maker

class SQLSessionAsync:
    _session_maker = None
    _engine = None

    @staticmethod
    def _get_session_maker():
        if not SQLSessionAsync._session_maker:
            SQLSessionAsync._engine = create_async_engine(
                database_connection_string_async, echo=False, pool_size=100, max_overflow=0)

            SQLSessionAsync._session_maker = sessionmaker(SQLSessionAsync._engine, expire_on_commit=False,
                                                          class_=AsyncSession)
        return SQLSessionAsync._session_maker