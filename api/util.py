from fastapi import APIRouter, Request, Response, Depends
from core.Auth import get_current_user
from models import Conversation


router = APIRouter(prefix="")


@router.post("/gen_title/")
async def gen_title_byID(request: Request, user_id: int = Depends(get_current_user)):
    payload = await request.json()
    conversation_id = payload["conversationId"]

    if not conversation_id:
        return Response(status_code=404)
    
    conversation = await Conversation.get_or_none(id=conversation_id)

    if not conversation:
        return Response(status_code=404)
    
    return {"title": conversation.topic}