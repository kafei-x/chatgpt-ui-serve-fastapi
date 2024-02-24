from fastapi import APIRouter, Depends, Response
from models import Conversation, User
from core.Auth import get_current_user
from llm import chatbot


router = APIRouter(prefix="/conversations")



@router.get("/{conversation_id}")
async def get_one_conversation(conversation_id: int, user_id: int = Depends(get_current_user)):
    """
    返回用户某个的对话
    """
    conversation = await Conversation.get_or_none(id=conversation_id)
    
    print(conversation)

    return conversation

@router.delete("/{conversation_id}/")
async def del_one_conversation(conversation_id: int, user_id: int = Depends(get_current_user)):
    """
    删除用户某个的对话
    """
    conversation = await Conversation.get_or_none(id=conversation_id)
    if conversation:
        await conversation.delete()

    chatbot.del_by_session_id(session_id=conversation_id)    
    


    return Response(status_code=204)
    

@router.get("/")
async def get_all_conversation(user_id: int = Depends(get_current_user)):
    """
    返回用户所有的对话
    """
    user = await User.get_or_none(id=user_id)
    conversations = []
    if user:
        conversations = await user.conversations

    return conversations