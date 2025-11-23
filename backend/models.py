# unknown if the name will stay the same

from tortoise import fields
from tortoise.models import Model

class Profile(Model):
    id = fields.IntField(primary_key=True)
    user_id = fields.IntField()
    name = fields.TextField()
    age = fields.IntField()
    gender = fields.TextField()
    sexuality = fields.TextField()