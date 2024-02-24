from fastapi import APIRouter, Depends, Response, Request
from schemas import account_schemas
from models.account_model import User
from datetime import datetime, timedelta, timezone
from core.Auth import create_access_token, get_current_user
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config import settings
from core.Utils import en_password, check_password



router = APIRouter(prefix="/account")


@router.post("/registration/")
async def registration(account: account_schemas.AccountAdd):
    if errmsg := account.validate_passwords():
        return errmsg
    
    if errmsg := await account.validate_account_not_exist():
        return errmsg
    
    password_enc = en_password(account.password1)

    await User.create(username=account.username, password=password_enc, email=account.email)
    
    return {
        # "access_token": "",
        # "refresh_token": "",
        "user": {
            "username": account.username,
            "email": account.email,
            "first_name": "",
            "last_name": ""
        },
        "email_verification_required": "none"
    }

@router.post("/unregistration/")
async def unregistration(request: Request, user_id: int = Depends(get_current_user)):
    get_user = await User.get_or_none(id=user_id)
    if not get_user:
        return Response(status_code=404, content="user not found")
    
    await get_user.delete()

    response = Response(status_code=204)
    response.delete_cookie(key="auth")
    
    return response

@router.post("/login/")
async def login(account: account_schemas.AccountLogin, response: Response):
    get_user = await User.get_or_none(username=account.username)
    if not get_user:
        return {"non_field_errors":["Unable to log in with provided credentials."]}
    
    if not check_password(account.password, get_user.password):
        return {"non_field_errors":["Unable to log in with provided credentials."]}
    

    jwt_data = {
        "user_id": str(get_user.id),
        "user_name": get_user.username
    }
    jwt_token = create_access_token(data=jwt_data)
    data = {"token": jwt_token, "expires_in": settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60}

    utc_now = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    local_now = utc_now.astimezone()

    # Convert local_now to UTC using usegmt=False
    utc_from_local = local_now.astimezone(timezone.utc)

    response.set_cookie(key="auth", value=jwt_token, max_age=86400, 
                        expires=utc_from_local,
                        httponly=True)  # 设置 Cookie

    
    get_user.last_login = datetime.now()
    await get_user.save()

    return {
        "access_token": jwt_token,
        "refresh_token": "",
        "user": {
            "username": get_user.username,
            "email": get_user.email,
            "first_name": "",
            "last_name": ""
        }
    }


@router.post("/logout/")
async def logout(request: Request, user_id: int = Depends(get_current_user)):
    """
    用户退出
    """
    response = Response(status_code=200)
    response.delete_cookie(key="auth")
    return response




@router.post("/oath2")
async def oath2(login_form: OAuth2PasswordRequestForm = Depends()):
    """
    doc 测试接口， jwt校验的本质是，服务器生成有一个有限时间的token，服务器在请求头中携带此token进行请求
    """
    print(222)
    get_user = await User.get_or_none(username=login_form.username)

    jwt_data = {
        "user_id": str(get_user.id),
        "user_name": get_user.username
    }
    jwt_token = create_access_token(data=jwt_data)

    # 字段需要固定
    return {"access_token": jwt_token, "token_type": "bearer"}



@router.get("/user/")
async def get_userinfo(request: Request, user_id: int = Depends(get_current_user)):
    get_user = await User.get_or_none(id=user_id)
    
    if not get_user:
        raise Response(status_code=404, content="user not found")

    return {
        "username": get_user.username,
        "email": get_user.email,
        "phone_number": ""
    }

@router.post("/password/change/")
async def change_password(request: Request, user_id: int = Depends(get_current_user)):
    payload = await request.json()
    old_password = payload.get("old_password")
    new_password1 = payload.get("new_password1")
    new_password2 = payload.get("new_password2")

    if new_password1 != new_password2:
        return Response(status_code=400, content="password not match")
    
    get_user = await User.get_or_none(id=user_id)
    if not get_user:
        return Response(status_code=404, content="user not found")
    
    if check_password(old_password, get_user.password):
        get_user.password = en_password(new_password1)
        await get_user.save()
    
    return {'detail': ('New password has been saved.')}
    

