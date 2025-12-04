import datetime
from enum import Enum
from typing import Annotated
from contextlib import asynccontextmanager
from fastapi import FastAPI, Header, Response
from fastapi.middleware.cors import CORSMiddleware
from tortoise.exceptions import DoesNotExist
from pydantic import BaseModel
from database import init_db, close_db
from models import ModerationEvents, Profile, Auth, User, EventType
import httpx
import secrets
import random
import os

CLIENT_TOKEN = os.environ.get("CLIENT_TOKEN")
CLIENT_ID = 1442284848109846598
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")


class RouteHeaders(BaseModel):
    Authorization: str


class ProfileBase(BaseModel):
    name: str
    age: int
    gender: str
    gender_specified: str | None = None
    sexuality: str
    bio: str


class DiscordExchange(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    scope: str

    model_config = {"populate_by_name": True}


class DiscordProfile(BaseModel):
    id: str
    username: str
    global_name: str
    avatar: str
    email: str


class WarningEdit(BaseModel):
    reason: str | None = None
    edited_by: int


class ModerationEventFetchType(str, Enum):
    ALL = "all"
    RECEIVED = "received"
    ISSUED = "issued"
    EDITED = "edited"


class EventFetchType(str, Enum):
    NOTE = "Note"
    WARNING = "Warning"
    MUTE = "Mute"
    KICK = "Kick"
    BAN = "Ban"
    TIMEOUT = "Timeout"
    ALL = "All"


class ModerationEventFetchFilters(BaseModel):
    event_type: EventFetchType = EventFetchType.ALL
    issued_before: datetime.datetime | None = None
    issued_after: datetime.datetime | None = None
    fetch_type: ModerationEventFetchType = ModerationEventFetchType.RECEIVED


class ModerationEventCreate(BaseModel):
    issued_by: int
    reason: str | None = None
    event_type: EventType


class ModerationEventEdit(BaseModel):
    reason: str | None = None
    edited_by: int


# this just defines the lifespan on the app, like an event, so this runs on startup, then yeilds to shutdown.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()


async def exchange_code(code):
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://localhost:3000/authorize",
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://discord.com/api/v10/oauth2/token", data=data, headers=headers
        )
        data: dict = response.json()
        if not data.get("access_token"):
            return data
        print(data)
        return DiscordExchange(**data)


async def get_discord_profile(access_token) -> DiscordProfile:
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Bearer {access_token}",
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://discord.com/api/v10/users/@me", headers=headers
        )
        data: dict = response.json()
        profile = DiscordProfile(**data)
        return profile


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # allow all HTTP methods
    allow_headers=["*"],  # allow all headers
)

# this is just an example, may not be offical
# @app.post('/profile/create')
# async def profile_create(headers:Annotated[RouteHeaders, Header()], profile:ProfileBase):
#     # we would call tortoise orm to create a profile if one does not exists already

#     # would need to verify headers
#     existing = await Profile.get_or_none(user_id=profile.user_id)
#     if existing:
#         return {"success": False, "message": "profile already exists", "profile": existing}

#     new_profile = await Profile.create(
#         user_id = profile.user_id,
#         name = profile.name,
#         age = profile.age,
#         gender = profile.gender,
#         sexuality = profile.sexuality
#     )

#     print(new_profile.id)
#     return {"success": True, "profile": profile}


@app.get("/authorize")
async def authorize(code):
    exchange_data: DiscordExchange | dict = await exchange_code(code)
    if type(exchange_data) != DiscordExchange:
        return {"success": False, "message": f"exchange failed! dump: {exchange_data}"}
    # use the data to get a user profile
    profile = await get_discord_profile(exchange_data.access_token)
    web_token = secrets.token_urlsafe(32)
    await Auth.update_or_create(
        user_id=profile.id,
        access_token=exchange_data.access_token,
        web_token=web_token,
        token_type=exchange_data.token_type,
    )
    return {"success": True, "profile": profile.model_dump(), "web_token": web_token}


@app.get("/authorization")
async def check_authorization(token):
    try:
        auth = await Auth.get(web_token=token)
    except DoesNotExist:
        return {"success": False, "message": "invalid token"}
    profile = await get_discord_profile(auth.access_token)
    return {"success": True, "profile": profile.model_dump()}


@app.post("/profile/create")
async def profile_create(
    headers: Annotated[RouteHeaders, Header()], profile: ProfileBase
):
    print(headers)
    print(profile)
    return {"success": True}


@app.get(
    "/moderation/events/{user_id}",
    response_model=ModerationEventFetchFilters,
    summary="Fetch moderation events tied to a user.",
    description="Fetch moderation events for a user with optional filters for event type,  date range.",
    responses={
        200: {"description": "Successful Response",
              "content": {"application/json": {
                    "example": {
                        "success": True,
                        "events": [
                            {
                                "issued_at": "2024-01-01T12:00:00Z",
                                "issued_by": 123456789012345678,
                                "reason": "Inappropriate behavior",
                                "last_edited_by": 987654321098765432,
                                "last_edited_at": "2024-01-02T15:30:00Z",
                                "event_type": "Warning",
                                "id": 1
                            },
                            {
                                "issued_at": "2024-02-15T09:45:00Z",
                                "issued_by": 123456789012345678,
                                "reason": "Spamming",
                                "last_edited_by": None,
                                "last_edited_at": None,
                                "event_type": "Mute",
                                "id": 2
                            }
                        ]
                    }
              }}},
        404: {"description": "User Not Found",
              "content": {"application/json": {
                  "example": {
                      "success": False,
                      "message": "User not found"
                  }
              }}},
    }
)
async def fetch_warnings(
    user_id: int,
    filters: ModerationEventFetchFilters,
    headers: Annotated[RouteHeaders, Header()],
    response: Response,
):
    # TODO: Bot Authorization Check Here
    print(headers)
    try:
        user = await User.get(user_id=user_id)

        query = user.moderation_events_received

        if filters.fetch_type == ModerationEventFetchType.RECEIVED:
            query = query.filter(warned_user=user)
        elif filters.fetch_type == ModerationEventFetchType.ISSUED:
            query = query.filter(issued_by=user)
        elif filters.fetch_type == ModerationEventFetchType.EDITED:
            query = query.filter(last_edited_by=user)

        if filters.event_type != EventFetchType.ALL:
            query = query.filter(event_type=filters.event_type.value)

        if filters.issued_before:
            query = query.filter(issued_at__lt=filters.issued_before)

        if filters.issued_after:
            query = query.filter(issued_at__gt=filters.issued_after)

        events = (
            await query.order_by("-issued_at")
            .select_related("issued_by", "last_edited_by")
            .all()
        )

    except DoesNotExist:
        response.status_code = 404
        return {"success": False, "message": "User not found"}

    else:
        return {
            "success": True,
            "events": [
                {
                    "issued_at": event.issued_at,
                    "issued_by": event.issued_by.user_id,
                    "reason": event.reason,
                    "last_edited_by": event.last_edited_by.user_id
                    if event.last_edited_by
                    else None,
                    "last_edited_at": event.last_edited_at
                    if event.last_edited_at
                    else None,
                    "event_type": event.event_type.value,
                    "id": event.id,
                }
                for event in events
            ],
        }


@app.post("/moderation/events/{user_id}",
          response_model=ModerationEventCreate,
          summary="Issue a moderation event to a user.",
          description="Issue a moderation event (e.g., warning, mute) to a user.",
            responses={
                200: {"description": "Successful Response",
                        "content": {"application/json": {
                            "example": {
                                "success": True,
                                "event_id": 1
                            }
                        }}},
              
            }
            )
async def issue_warning(
    user_id: int,
    event: ModerationEventCreate,
    headers: Annotated[RouteHeaders, Header()],
    response: Response,
):
    # TODO: Bot Authorization Check Here

    print(user_id)
    issued_by_id = event.issued_by
    reason = event.reason
    user_, _ = await User.get_or_create(user_id=user_id)
    issued_by_, _ = await User.get_or_create(user_id=issued_by_id)
    event_ = await ModerationEvents.create(
        warned_user=user_,
        issued_by=issued_by_,
        event_type=event.event_type,
        reason=reason,
    )
    return {"success": True, "event_id": event_.id}


@app.patch("/moderation/events/{event_id}",
           summary="Edit a moderation event.",
           description="Edit the reason for a moderation event.",
           responses={
               200: {"description": "Successful Response",
                      "content": {"application/json": {
                          "example": {
                              "success": True
                          }
                      }}},
               404: {"description": "Event Not Found",
                      "content": {"application/json": {
                          "example": {
                              "success": False,
                              "message": "Invalid Moderation Event ID"
                          }
                      }}},
           }
           )
async def edit_warning(
    event_id: int,
    event: ModerationEventEdit,
    headers: Annotated[RouteHeaders, Header()],
    response: Response,
):
    # TODO: Bot Authorization Check Here
    print(headers)
    try:
        event_ = await ModerationEvents.get(id=event_id)
        event_.reason = event.reason
        event_.last_edited_by, _ = await User.get_or_create(user_id=event.edited_by)
        event_.last_edited_at = datetime.datetime.now()
        await event_.save()

        return {"success": True}
    except DoesNotExist:
        response.status_code = 404
        return {"success": False, "message": "Invalid Moderation Event ID"}


@app.delete("/moderation/events/{event_id}",
            summary="Delete a moderation event.",
           description="Delete a moderation event by its ID.",
           responses={
               200: {"description": "Successful Response",
                      "content": {"application/json": {
                          "example": {
                              "success": True
                          }
                      }}},
               404: {"description": "Event Not Found",
                      "content": {"application/json": {
                          "example": {
                              "success": False,
                              "message": "Invalid Moderation Event ID"
                          }
                      }}},
           }
           )
async def delete_warning(
    event_id: int, headers: Annotated[RouteHeaders, Header()], response: Response
):
    # TODO: Bot Authorization Check Here
    print(headers)

    try:
        event_ = await ModerationEvents.get(id=event_id)
        await event_.delete()
        return {"success": True}
    except DoesNotExist:
        response.status_code = 404
        return {"success": False, "message": "Invalid Moderation Event ID"}
