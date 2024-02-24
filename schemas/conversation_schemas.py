from pydantic import BaseModel, Field


class Message(BaseModel):
    content: str = Field()
    message_type: int = Field()
    tool: str = Field()

class ConversationAdd(BaseModel):
    conversationId: int = Field()
    frequency_penalty: int = Field()
    frugalMode: bool = Field()
    max_tokens: int = Field()
    message: list[Message] = Field()
    name: str = Field(min_length=3, max_length=100)
    openaiApiKey: str = Field()
    presence_penalty:str = Field
    temperature: int = Field(description="随机率")
    top_p: int = Field()
    total_tokens: int = Field()
