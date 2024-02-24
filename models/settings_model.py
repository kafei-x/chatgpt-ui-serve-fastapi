from tortoise import fields
from models.base_model import IDbaseModel

class Setting(IDbaseModel):
    name = fields.CharField(max_length=50, unique=True, index=True, description="配置名")
    value = fields.BooleanField(default=False, description="配置值")

    class Meta:
        table = "chat_setting"
        description = "配置表"


async def create_defultdata():
    
    default_data = [
        {"name":"open_frugal_mode_control", "value": True},
        {"name":"open_registration", "value": True},
        {"name":"open_web_search", "value": True},
        {"name":"open_api_key_setting", "value": True},
    ]
    
    for data in default_data:
        await Setting.create(**data)