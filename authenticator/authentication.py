from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from models.user import User
from model_handler.admin_handler import AdminHandlerSync, AdminHandler
from database_connection.connection_maker import SQLSession, SQLSessionAsync
session_maker = SQLSession._get_session_maker()
#session_maker = SQLSessionAsync._get_session_maker()

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        with session_maker() as session:
            with session.begin():
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                user_id: str = payload.get("user_id")
                user = AdminHandlerSync.get_user_from_id(session=session, user_id=user_id)
                if not user:
                    raise HTTPException(status_code=401, detail="Invalid user")
                return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
