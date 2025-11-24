# unknown if the name will stay the same

from tortoise import fields
from tortoise.models import Model

class Profile(Model):
    id = fields.IntField(primary_key=True)
    user_id = fields.IntField(unique=True)
    name = fields.TextField()
    pronouns = fields.TextField()
    age = fields.IntField()
    gender = fields.TextField()
    sexuality = fields.TextField()

# represents an auth with users discord bearer token, and a JWT token thats stored in the wev 
class Auth(Model):
    id = fields.IntField(primary_key=True)
    user_id = fields.IntField()
    access_token = fields.TextField()
    web_token = fields.TextField()
    # add jwt and other here