import click
import asyncio
from tortoise import run_async
from database.mysql import DB_ORM_CONFIG
from models import create_defaultdata
from tortoise import Tortoise

@click.group()
def main():
   pass


@main.command(help="create table and insert default data")
def init_db():
   """
   初始化数据库，建表，插入默认数据
   """
   async def do_init():
       await Tortoise.init(config=DB_ORM_CONFIG)
       await Tortoise.generate_schemas()
       await create_defaultdata()
   run_async(do_init())


@main.command(help="del all data in database")
def clear_db():
   """
   清空数据库
   """   
   async def do_clear():
       await Tortoise.init(config=DB_ORM_CONFIG)
       await Tortoise._drop_databases()
   run_async(do_clear())


if __name__ == '__main__':
    asyncio.run(main())