from fastapi import APIRouter

from .endpoint import passkey

route = APIRouter()

route.include_router(passkey.route, prefix="/passkey")