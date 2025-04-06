from fastapi import APIRouter
from admin.routes import admin

apirouter = APIRouter()

apirouter.include_router(admin.router, prefix="/admin")