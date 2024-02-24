from tortoise.models import Model
from tortoise import fields


# class AbstractModel(Model):
#     # 主键，当表里所有属性都没设置pk时，默认生成一个IntField类型 id 的主键
#     id = fields.UUIDField(pk=True)

#     class Meta:
#         # 抽象模型，不生成表
#         abstract = True




class IDbaseModel(Model):
    id = fields.IntField(pk=True, auto_increment=True, description="ID")

    class Meta:
        abstract = True


# 数据库表中添加时间字段
class TimestampMixin(Model):
    create_time = fields.DatetimeField(auto_now_add=True, description='创建时间')
    update_time = fields.DatetimeField(auto_now=True, description="更新时间")

    class Meta:
        abstract = True