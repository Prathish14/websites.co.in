from fastapi import APIRouter, Depends, Response, HTTPException
from fastapi_cache.decorator import cache
from model_handler.admin_handler import AdminHandler
from models.user import User
from fastapi.responses import JSONResponse
from authenticator.authentication import get_current_user
from database_connection.connection_maker import SQLSessionAsync
from cache_handler.redis_intializer import RedisManaged

router = APIRouter()
session_maker = SQLSessionAsync._get_session_maker()

@router.post("/ai/creative-suggestion", name="It gives ai based suggestion for website building")
async def get_ai_based_suggestion_for_website(user: User = Depends(get_current_user)):
    try:
        async with session_maker() as session:
            async with session.begin():
                RedisManaged.check_rate_limit_of_user(user_id=user.id)
                user_ai_credts= RedisManaged.get_user_ai_credits(user_id=user.id)

                if not user_ai_credts:
                    user_ai_credts = RedisManaged.set_user_ai_credits(user_id=user.id, ai_credits=user.ai_credits)
                
                if user_ai_credts <= 10:
                    message = f'User dont have suffeicient credits'
                    raise HTTPException(
                        status_code=200,
                        detail=message,
                    )

                
                #insert ai calling code here


                response1= await AdminHandler.get_the_user_details(user_id="12345")
                return Response(response1)
            
    except HTTPException as h: 
        return JSONResponse(content={"ok": False, "message": h.detail}, status_code=h.status_code)
    except Exception as e:
        return JSONResponse(content={"ok": False, "message": e.__str__()}, status_code=500)
    return JSONResponse(content={"ok": True, "message": "whatsapp_business profile created successfully."},status_code=200)

