# unknown if the name will stay the same

from enum import Enum
from tortoise import fields
from tortoise.models import Model

class EventType(str, Enum):
    Note = 'Note'
    Warning = 'Warning'
    Mute = 'Mute'
    Kick = 'Kick'
    Ban = 'Ban'
    Timeout = 'Timeout'

class Profile(Model):
    id = fields.IntField(primary_key=True)
    user_id = fields.BigIntField(unique=True)
    name = fields.TextField()
    pronouns = fields.TextField()
    age = fields.IntField()
    gender = fields.TextField()
    sexuality = fields.TextField()
    bio = fields.TextField()

# represents an auth with users discord bearer token, and a JWT token thats stored in the wev 
class Auth(Model):
    id = fields.IntField(primary_key=True)
    user_id = fields.BigIntField()
    access_token = fields.TextField()
    web_token = fields.TextField()
    token_type = fields.TextField()
    # add jwt and other here

class User(Model):
    user_id = fields.BigIntField(primary_key=True)
    is_banned = fields.BooleanField(default=False)
    moderation_events_received: fields.ReverseRelation["ModerationEvents"]
    moderation_events_issued: fields.ReverseRelation["ModerationEvents"]
    moderation_events_edited: fields.ReverseRelation["ModerationEvents"]
  
    class Meta:
        table = "users"

class ModerationEvents(Model):
    id = fields.IntField(primary_key=True, generated=True)
    issued_at = fields.DatetimeField(auto_now_add=True)
    issued_by = fields.ForeignKeyField('models.User', related_name='moderation_events_issued', on_delete=fields.CASCADE)
    reason = fields.TextField(null=True)
    edit_reason = fields.TextField(null=True)
    warned_user = fields.ForeignKeyField('models.User', related_name='moderation_events_received', on_delete=fields.CASCADE)
    event_type = fields.CharEnumField(EventType)
    last_edited_by = fields.ForeignKeyField('models.User', related_name='moderation_events_edited', null=True, on_delete=fields.CASCADE)
    last_edited_at = fields.DatetimeField(null=True)
    class Meta:
        table = "moderation_events"

