from tortoise.models import Model
from tortoise import fields
from models.base_model import IDbaseModel
from models.account_model import User


class Conversation(IDbaseModel):
    topic = fields.CharField(max_length=100, description="会话标题")
    create_at = fields.DatetimeField(auto_now_add=True, description="会话创建时间")

    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("sqlite.User", related_name='conversations',description="所属用户")
    messages: fields.ReverseRelation["Message"]

    class Meta:
        table = "chat_conversation"
        description = "会话表"


class Message(IDbaseModel):
    """message, is_bot, create_at, conversation_id, messages, tokens, message_type, user_id, is_disabled, embedding_message"""
    message = fields.TextField(description="消息内容")
    is_bot = fields.BooleanField(description="是否为机器人")
    create_at = fields.DatetimeField(auto_now_add=True, description="消息创建时间")
    conversation: fields.ForeignKeyRelation[Conversation] = fields.ForeignKeyField("sqlite.Conversation", related_name='messages', description="所属会话")
    messages = fields.TextField(default="", description="消息列表")
    tokens = fields.IntField(default=0, description="消息长度")
    message_type = fields.IntField(default=0, description="消息类型")
    user: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("sqlite.User", related_name='messages', description="所属用户")
    is_disabled = fields.BooleanField(default=False, description="是否禁用")
    embedding_message_doc = fields.JSONField(null=True, description="消息向量")

    class Meta:
        table = "chat_message"
        description = "消息表"
    
