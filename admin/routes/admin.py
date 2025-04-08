from fastapi import APIRouter, Depends, Response, HTTPException
from fastapi_cache.decorator import cache
from model_handler.admin_handler import AdminHandler
from models.user import User
from fastapi.responses import JSONResponse
from authenticator.authentication import get_current_user
from database_connection.connection_maker import SQLSessionAsync
from cache_handler.redis_intializer import RedisManaged
from services.gemeni_api_service import GeminiApiService
from admin.schemas.admin import RequestedInput

router = APIRouter()
session_maker = SQLSessionAsync._get_session_maker()

@router.post("/ai/creative-suggestion", name="It gives ai based suggestion for website building")
async def get_ai_based_suggestion_for_website(
    request_body: RequestedInput,
    user: User = Depends(get_current_user)
    ):
    try:
        async with session_maker() as session:
            async with session.begin():
                if not request_body.template_input and not request_body.layout_input and not request_body.content_input:
                    message = f'User need to specify either one of the three fields'
                    raise HTTPException(
                        status_code=200,
                        detail=message,
                    )
                
                RedisManaged.check_rate_limit_of_user(user_id=user.id)
                RedisManaged.check_ai_rate_limit()
                user_ai_credts= RedisManaged.get_user_ai_credits(user_id=user.id)

                if not user_ai_credts:
                    user_ai_credts = RedisManaged.set_user_ai_credits(user_id=user.id, ai_credits=user.ai_credits)
                
                if user_ai_credts < 10:
                    message = f'User dont have suffeicient credits'
                    raise HTTPException(
                        status_code=200,
                        detail=message,
                    )
                
                type_of_input = None
                user_request_string = None
                if request_body.template_input:
                    type_of_input = "template"
                    user_request_string = request_body.template_input
                elif request_body.layout_input:
                    type_of_input = "layout"
                    user_request_string = request_body.layout_input
                else:
                    type_of_input = "content"
                    user_request_string = request_body.content_input

                response = await GeminiApiService.get_response_from_gemini_flash_light(type_of_input=type_of_input, user_request_string=user_request_string)

                if response:
                    RedisManaged.decrement_user_ai_credits(user_id=user.id, decrment_value=10)
            
    except HTTPException as h: 
        return JSONResponse(content={"ok": False, "message": h.detail}, status_code=h.status_code)
    except Exception as e:
        return JSONResponse(content={"ok": False, "message": e.__str__()}, status_code=500)
    return JSONResponse(content={"ok": True, "type_of_suggestion": type_of_input, "data": response},status_code=200)

