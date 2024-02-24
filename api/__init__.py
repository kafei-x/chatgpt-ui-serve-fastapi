from fastapi import APIRouter, Request, Response
from models import Conversation

from . import chat
from . import account
from . import conversation
from . import util

api_router = APIRouter(prefix="/api")

api_router.include_router(account.router)
api_router.include_router(chat.router)
api_router.include_router(conversation.router)
api_router.include_router(util.router)

