from fastapi import APIRouter
from models import Message, Conversation
from . import settings
from . import conversations
router = APIRouter(prefix="/chat")

router.include_router(settings.router)
router.include_router(conversations.router)

@router.get("/prompts/")
async def get_prompts(): 
    return []


@router.get("/embedding_document/")
async def get_embedding_document():
    return []


@router.get("/messages/")
async def get_messages_by_id(conversationId: int):

    msgs = []

    conversation = await Conversation.get_or_none(id=conversationId)
    if conversation:
        msgs = await conversation.messages

    return msgs







