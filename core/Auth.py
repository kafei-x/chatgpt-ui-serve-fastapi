# -*- coding:utf-8 -*-
"""
@Time : 2022/4/27 3:40 PM
@Author: binkuolo
@Des: JWT鉴权
"""
from datetime import timedelta, datetime
import jwt
from fastapi import HTTPException, Request, Depends
from fastapi.security import SecurityScopes
from fastapi.security.oauth2 import OAuth2PasswordBearer
from jwt import PyJWTError
from pydantic import ValidationError
from starlette import status
from config import settings
from models.account_model import User


# OAuth2 认证方案， tokenUrl="/token" 指定了用于获取访问令牌的端点 URL。
# auto_error=False ,自会获取token不会验证
OAuth2 = OAuth2PasswordBearer(tokenUrl=settings.SWAGGER_UI_OAUTH2_REDIRECT_URL, auto_error=False)


def create_access_token(data: dict):
    """
    创建token
    :param data: 加密数据
    :return: jwt
    """
    token_data = data.copy()
    # token超时时间
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    print(f"{expire=}")
    # 向jwt加入超时时间
    token_data.update({"exp": expire})
    # jwt加密
    jwt_token = jwt.encode(token_data, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    return jwt_token


async def get_current_user(req: Request, token=Depends(OAuth2)):
    """
    权限验证，会校验Token, 需要进行权限控制的接口。直接 Denpends 该函数即可
    :param token:
    :param req:
    :param security_scopes: 权限域
    :return:
    """
    # ----------------------------------------验证JWT token------------------------------------------------------------
    # print("enter get_current_user")
    token = req.cookies.get("auth")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="凭证已证过期",
            headers={"WWW-Authenticate": f"Bearer {token}"},
        )
    
    try:
        # token解密
        token_data = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        if token_data:
            user_id = token_data.get("user_id")
            user_name = token_data.get("user_name")
            exp = token_data.get("exp")
            print(datetime.fromtimestamp(exp))
    except jwt.ExpiredSignatureError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="凭证已证过期",
            headers={"WWW-Authenticate": f"Bearer {token}"},
        )

    except jwt.InvalidTokenError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效凭证",
            headers={"WWW-Authenticate": f"Bearer {token}"},
        )

    except (PyJWTError, ValidationError):

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效凭证",
            headers={"WWW-Authenticate": f"Bearer {token}"},
        )
    # ---------------------------------------验证权限-------------------------------------------------------------------

    # 查询用户是否真实有效、或者已经被禁用
    user = await User.get_or_none(id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
            headers={"WWW-Authenticate": f"Bearer {token}"},
        )

    

    return user_id
