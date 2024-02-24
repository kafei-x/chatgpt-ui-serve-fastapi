from tortoise import fields
from tortoise.models import Model
from models.base_model import IDbaseModel, TimestampMixin
from core.Utils import en_password



class User(IDbaseModel):
    # unique 是否唯一 ,max—length 数据长度 ，index 表示是否建索引
    password = fields.CharField(max_length=300, description="密码")
    last_login = fields.DatetimeField(null=True, description="最后登录时间")
    is_superuser = fields.BooleanField(default=0, description="是否为超级管理员")
    username = fields.CharField(max_length=20, unique=True, index=True, description="用户名")
    last_name = fields.CharField(max_length=20, null=True, description="姓")
    email = fields.CharField(max_length=50, description="邮箱")
    is_staff = fields.BooleanField(default=0, description="是否为管理员")
    is_active = fields.BooleanField(default=1, description="是否激活")
    data_joined = fields.DatetimeField(auto_now_add=True, description="创建时间")
    first_name = fields.CharField(max_length=20, null=True, description="名")

    conversations: fields.ReverseRelation["Conversation"]
    messages: fields.ReverseRelation["Message"]

    class Meta:
        table = "auth_user"
        description = "用户信息表"


async def create_defaultdata():
    await User.create(username="admin", password=en_password("admin"), email="admin@qq.com", is_superuser=True)



# from models.conversation_model import Conversation, Message
