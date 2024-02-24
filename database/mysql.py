# -*- coding:utf-8 -*-

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise, fields, run_async
import os
import models
from models import create_defaultdata
# from models import tables

# -----------------------数据库配置-----------------------------------
# 可实现多个数据库连接
DB_ORM_CONFIG = {
    "connections": {
        # "mysql": {
        #     "engine": "tortoise.backends.mysql",
        #     "credentials": {
        #         "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
        #         "user": os.getenv("MYSQL_USER", "root"),
        #         "password": os.getenv("MYSQL_PASSWORD", "kafei"),
        #         "port": int(os.getenv("MYSQL_PORT", 3303)),
        #         "database": os.getenv("MYSQL_DB", "chatgpt"),   # 需要主动建数据库
        #     }
        # },
        "sqlite": {
            "engine": "tortoise.backends.sqlite",
            "credentials": {
                "file_path": "db.sqlite3",
            }
        },

    },
    "apps": {
        # "mysql": {"models": ["models"], "default_connection": "mysql"},
        "sqlite": {"models": ["models"], "default_connection": "sqlite"},
    },
    "use_tz": False,
    "timezone": "Asia/Shanghai"
}


async def register_databases(app: FastAPI):
    
    # 注册数据库
    register_tortoise(
        app,
        config=DB_ORM_CONFIG,
        generate_schemas=False,      # 数据库自动创建表，如果表存在，就不再创建
        add_exception_handlers=False,
    )
    

if __name__ == "__main__":
    # run_async(clear_db())
    # run_async(init_db())
    pass


