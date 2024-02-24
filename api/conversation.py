from fastapi import APIRouter, Depends, Request
from schemas import conversation_schemas
from models import Conversation, Message, User
from core.Auth import get_current_user
from llm.chatbot import chain_with_message_history
from fastapi.responses import StreamingResponse
from datetime import datetime
import json
router = APIRouter(prefix="/conversation")



def sse_pack(event, data):
    # Format data as an SSE message
    packet = "event: %s\n" % event
    packet += "data: %s\n" % json.dumps(data)
    packet += "\n"
    return packet


@router.post("/")
async def do_conversation(request: Request, user_id: int = Depends(get_current_user)):

    async def generate_data():

        message = await Message.create(message="hello",messages=[{'role': 'system', 'content': 'You are a helpful assistant.'}, {'role': 'user', 'content': human_input}],
                                       conversation_id=session_id, user=user, is_bot=False)
        completion_text = ""
        yield sse_pack("userMessageId", {"userMessageId": message.id})


        async for s in chain_with_message_history.astream(
            {"input": human_input},
            {"configurable": {"session_id": session_id}}
        ):
            completion_text += s.content
            yield sse_pack("message", {"content": s.content})

        # yield sse_pack("message", {"content": completion_text})

        # print(222)
        ai_msg = await Message.create(message=completion_text,messages=[],
                                      conversation_id=session_id, user=user, is_bot=True)
        # print(session_id, ai_msg.id)
        yield sse_pack("done", {
                'messageId': ai_msg.id,
                'conversationId': session_id,
                'newDocId': None,
            })

    # print("enter create_conversation")
    payload  = await request.json()
    content = payload["message"][0]["content"]
    session_id = payload["conversationId"]
    user = await User.get_or_none(id=user_id)
    # print(user.id)
    if not session_id:
        session =  await Conversation.create(topic=content, user=user)
        session_id = session.id
    
    human_input = content

    response = StreamingResponse(generate_data(), media_type="text/event-stream")
    response.headers["content-type"] = "text/event-stream"
    # print("over")
    return response


# @router.post("/")
# async def del_conversation(request: Request, user_id: int = Depends(get_current_user)):


@router.post("/stream")
async def stream_response(request: Request, user_id: int = Depends(get_current_user)):
    async def generate_data():
        yield sse_pack("userMessageId", {"userMessageId": 1})

        for i in range(100):
            yield sse_pack(
                "message", 
                {"content": i}
            )

        yield sse_pack("done", {
                'messageId': 1,
                'conversationId': 2,
                'newDocId': 0,
            })
    response = StreamingResponse(generate_data())
    response.headers["content-type"] = "text/event-stream"
    return response