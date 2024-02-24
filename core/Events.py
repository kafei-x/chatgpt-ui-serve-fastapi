# -*- coding:utf-8 -*-
"""
@Des: fastapi事件监听
"""

from typing import Callable
from fastapi import FastAPI
from database.mysql import register_databases

# app启动的回调函数
def startup(app: FastAPI) -> Callable:
    """
    FastApi 启动完成事件
    :param app: FastAPI
    :return: start_app
    """
    async def app_start() -> None:
        # APP启动完成后触发
        print("fastapi已启动")
        # 注册数据库
        await register_databases(app)
        
    return app_start

# app停止的回调函数
def stopping(app: FastAPI) -> Callable:
    """
    FastApi 停止事件
    :param app: FastAPI
    :return: stop_app
    """
    async def stop_app() -> None:
        # APP停止时触发
        print("fastapi已停止")


    return stop_app

    

