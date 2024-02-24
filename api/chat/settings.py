
from fastapi import APIRouter
from models.settings_model import Setting
from models import settings_model
from schemas import settings_schemas

router = APIRouter(prefix="/settings")


@router.get("/")
async def get_settings():
    return await Setting.all()

@router.post("/")
async def set_default_settings():
    """
    initial settings, if settings exist, do nothing
    """
 
    if await Setting.all().count():
        return "settins exist"

    await settings_model.create_defultdata()

    return "settings created success"

@router.put("/")
async def update_settings(setting_list: list[settings_schemas.Settings]):
    """
    update settings
    """
    
    for setting in setting_list:
        await Setting.filter(name=setting["name"]).update(value=setting["value"])

    return "update success"
    
