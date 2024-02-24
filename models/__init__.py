from .account_model import User
from .settings_model import Setting
from .conversation_model import Conversation
from .conversation_model import Message



async def create_defaultdata():
    await settings_model.create_defultdata()
    await account_model.create_defaultdata()
